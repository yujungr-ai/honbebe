"""
Rate Limiting 유틸리티
"""
import asyncio
import time
from collections import deque
from typing import Optional


class RateLimiter:
    """토큰 버킷 알고리즘 기반 Rate Limiter"""
    
    def __init__(self, max_calls: int, time_window: float = 1.0):
        """
        Args:
            max_calls: 시간 윈도우 내 최대 호출 수
            time_window: 시간 윈도우 (초)
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: deque = deque()
        self._lock = asyncio.Lock()
    
    async def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Rate limit 토큰 획득
        
        Args:
            timeout: 최대 대기 시간 (초), None이면 무한 대기
        
        Returns:
            토큰 획득 성공 여부
        """
        start_time = time.time()
        
        async with self._lock:
            while True:
                now = time.time()
                
                # 시간 윈도우 밖의 호출 기록 제거
                while self.calls and self.calls[0] <= now - self.time_window:
                    self.calls.popleft()
                
                # 토큰이 남아있으면 즉시 반환
                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return True
                
                # 타임아웃 체크
                if timeout is not None and (now - start_time) >= timeout:
                    return False
                
                # 다음 토큰이 사용 가능할 때까지 대기
                sleep_time = self.calls[0] + self.time_window - now
                if sleep_time > 0:
                    await asyncio.sleep(min(sleep_time, 0.1))


class ExponentialBackoff:
    """지수 백오프 재시도 전략"""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def get_delay(self, retry_count: int) -> float:
        """
        현재 재시도 횟수에 대한 대기 시간 계산
        
        Args:
            retry_count: 현재 재시도 횟수 (0부터 시작)
        
        Returns:
            대기 시간 (초)
        """
        delay = min(self.base_delay * (2 ** retry_count), self.max_delay)
        return delay
    
    async def retry_with_backoff(self, func, *args, **kwargs):
        """
        지수 백오프를 적용하여 함수 재시도
        
        Args:
            func: 실행할 함수
            *args, **kwargs: 함수 인자
        
        Returns:
            함수 실행 결과
        
        Raises:
            마지막 시도의 예외
        """
        last_exception = None
        
        for retry in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if retry < self.max_retries - 1:
                    delay = self.get_delay(retry)
                    await asyncio.sleep(delay)
        
        raise last_exception
