"""
애플리케이션 설정 관리
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """환경변수 기반 설정"""
    
    # OPENDART API
    dart_api_key: str = "572a0cb38976a78595028b1506ba9d5fa1d6122e"
    
    # 캐시 설정
    cache_dir: Path = Path("./data/cache")
    cache_expiry_days: int = 30
    
    # Rate Limiting
    rate_limit_per_second: int = 5
    
    # 로깅
    log_level: str = "INFO"
    
    # OPENDART API 엔드포인트
    dart_base_url: str = "https://opendart.fss.or.kr/api"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 싱글톤 인스턴스
settings = Settings()

# 캐시 디렉토리 생성
settings.cache_dir.mkdir(parents=True, exist_ok=True)
