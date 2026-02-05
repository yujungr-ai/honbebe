"""
SQLite 기반 캐싱 시스템
"""
import aiosqlite
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Any
from app.config import settings


class CacheManager:
    """SQLite 기반 캐시 관리자"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or settings.cache_dir / "cache.db"
        self._initialized = False
    
    async def initialize(self):
        """캐시 데이터베이스 초기화"""
        if self._initialized:
            return
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                )
            """)
            
            # 인덱스 생성
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at 
                ON cache(expires_at)
            """)
            
            await db.commit()
        
        self._initialized = True
    
    def _generate_key(self, *args, **kwargs) -> str:
        """캐시 키 생성"""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    async def get(self, *args, **kwargs) -> Optional[Any]:
        """
        캐시에서 데이터 조회
        
        Args:
            *args, **kwargs: 캐시 키 생성에 사용될 인자
        
        Returns:
            캐시된 데이터 또는 None
        """
        await self.initialize()
        
        key = self._generate_key(*args, **kwargs)
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT value, expires_at FROM cache WHERE key = ?",
                (key,)
            ) as cursor:
                row = await cursor.fetchone()
                
                if not row:
                    return None
                
                value_json, expires_at_str = row
                expires_at = datetime.fromisoformat(expires_at_str)
                
                # 만료된 캐시는 삭제
                if expires_at < datetime.now():
                    await db.execute("DELETE FROM cache WHERE key = ?", (key,))
                    await db.commit()
                    return None
                
                return json.loads(value_json)
    
    async def set(
        self,
        value: Any,
        *args,
        ttl_days: Optional[int] = None,
        **kwargs
    ):
        """
        캐시에 데이터 저장
        
        Args:
            value: 저장할 데이터
            *args, **kwargs: 캐시 키 생성에 사용될 인자
            ttl_days: 캐시 유효 기간 (일), None이면 설정 값 사용
        """
        await self.initialize()
        
        key = self._generate_key(*args, **kwargs)
        value_json = json.dumps(value)
        
        created_at = datetime.now()
        ttl = ttl_days if ttl_days is not None else settings.cache_expiry_days
        expires_at = created_at + timedelta(days=ttl)
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO cache (key, value, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (
                key,
                value_json,
                created_at.isoformat(),
                expires_at.isoformat()
            ))
            await db.commit()
    
    async def delete(self, *args, **kwargs):
        """캐시에서 데이터 삭제"""
        await self.initialize()
        
        key = self._generate_key(*args, **kwargs)
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM cache WHERE key = ?", (key,))
            await db.commit()
    
    async def cleanup_expired(self):
        """만료된 캐시 정리"""
        await self.initialize()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM cache WHERE expires_at < ?",
                (datetime.now().isoformat(),)
            )
            await db.commit()


# 싱글톤 인스턴스
cache_manager = CacheManager()
