"""
OPENDART API 클라이언트
"""
import httpx
import asyncio
from typing import Dict, Any, Optional
from app.config import settings
from app.utils.rate_limiter import RateLimiter, ExponentialBackoff


class DartAPIError(Exception):
    """DART API 에러"""
    
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class DartClient:
    """OPENDART API 클라이언트"""
    
    # DART API 에러 코드 매핑
    ERROR_MESSAGES = {
        "000": "정상 응답",
        "010": "등록되지 않은 API 키입니다.",
        "011": "사용할 수 없는 API 키입니다. (기간 만료 등)",
        "013": "요청하신 데이터가 존재하지 않습니다.",
        "020": "요청 제한을 초과하였습니다. 잠시 후 다시 시도해주세요.",
        "100": "필드의 부적절한 값입니다.",
        "800": "원활한 공시서비스를 위하여 접속이 차단되었습니다.",
    }
    
    def __init__(self):
        self.api_key = settings.dart_api_key
        self.base_url = settings.dart_base_url
        self.rate_limiter = RateLimiter(
            max_calls=settings.rate_limit_per_second,
            time_window=1.0
        )
        self.backoff = ExponentialBackoff(max_retries=3)
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """HTTP 클라이언트 인스턴스 반환"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                limits=httpx.Limits(max_keepalive_connections=10)
            )
        return self._client
    
    async def close(self):
        """클라이언트 종료"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
    
    def _get_user_friendly_message(self, code: str) -> str:
        """사용자 친화적 에러 메시지 반환"""
        return self.ERROR_MESSAGES.get(code, f"알 수 없는 에러 (코드: {code})")
    
    async def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        response_type: str = "json"
    ) -> Any:
        """
        DART API 요청 실행
        
        Args:
            endpoint: API 엔드포인트
            params: 요청 파라미터
            response_type: 응답 타입 ('json' 또는 'binary')
        
        Returns:
            API 응답 데이터
        
        Raises:
            DartAPIError: API 에러 발생 시
        """
        # Rate limiting
        await self.rate_limiter.acquire()
        
        # API 키 추가
        params["crtfc_key"] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        client = await self._get_client()
        
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            if response_type == "binary":
                content = response.content
                
                # 빈 응답 체크
                if not content:
                    raise DartAPIError(
                        "EMPTY_RESPONSE",
                        "API 응답이 비어있습니다."
                    )
                
                # binary 응답이 JSON 에러일 수 있으므로 확인
                if content.startswith(b'{'):
                    try:
                        import json
                        error_data = json.loads(content.decode('utf-8'))
                        status = error_data.get("status", "UNKNOWN")
                        message = self._get_user_friendly_message(status) if status in self.ERROR_MESSAGES else error_data.get("message", "알 수 없는 에러")
                        raise DartAPIError(status, message)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        pass  # 실제 binary 데이터인 경우
                
                # XML 응답일 수도 있음 (<?xml 또는 <로 시작)
                if content.startswith(b'<?xml') or content.strip().startswith(b'<'):
                    # XML은 그대로 반환 (corp_resolver에서 처리)
                    return content
                
                return content
            
            # JSON 응답 처리
            data = response.json()
            
            # 에러 체크
            status = data.get("status")
            if status and status != "000":
                message = self._get_user_friendly_message(status)
                raise DartAPIError(status, message)
            
            return data
            
        except httpx.HTTPStatusError as e:
            raise DartAPIError(
                "HTTP_ERROR",
                f"HTTP 에러 발생: {e.response.status_code}"
            )
        except httpx.RequestError as e:
            raise DartAPIError(
                "NETWORK_ERROR",
                f"네트워크 에러 발생: {str(e)}"
            )
    
    async def get_corp_code_xml(self) -> bytes:
        """
        고유번호(corpCode.xml) 다운로드
        
        Returns:
            ZIP 바이너리 데이터
        """
        return await self._make_request(
            "corpCode.xml",
            {},
            response_type="binary"
        )
    
    async def get_financial_statements(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        fs_div: str = "CFS"
    ) -> Dict[str, Any]:
        """
        단일회사 전체 재무제표 조회
        
        Args:
            corp_code: 고유번호 (8자리)
            bsns_year: 사업연도 (YYYY)
            reprt_code: 보고서 코드 (11011/11012/11013/11014)
            fs_div: 재무제표 구분 (CFS: 연결, OFS: 개별)
        
        Returns:
            재무제표 데이터
        """
        async def _fetch():
            return await self._make_request(
                "fnlttSinglAcntAll.json",
                {
                    "corp_code": corp_code,
                    "bsns_year": bsns_year,
                    "reprt_code": reprt_code,
                    "fs_div": fs_div
                }
            )
        
        # 재시도 로직 적용
        return await self.backoff.retry_with_backoff(_fetch)


# 싱글톤 인스턴스
dart_client = DartClient()
