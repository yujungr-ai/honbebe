"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.routers import ebitda
from app.services.dart_client import dart_client
from app.utils.cache import cache_manager
from app.config import settings
import json


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시
    print("=" * 60)
    print("OPENDART EBITDA Calculator API 시작")
    print("=" * 60)
    
    # 캐시 초기화
    await cache_manager.initialize()
    print("캐시 시스템 초기화 완료")
    
    # corp_code 매핑 사전 로드 (선택사항)
    # await corp_resolver.load_mapping()
    
    yield
    
    # 종료 시
    print("\n애플리케이션 종료 중...")
    await dart_client.close()
    print("DART API 클라이언트 종료 완료")


# FastAPI 앱 생성
app = FastAPI(
    title="OPENDART EBITDA Calculator API",
    description="""
    OPENDART API를 활용하여 기업의 EBITDA를 계산하는 백엔드 서비스입니다.
    
    ## 주요 기능
    
    * 🏢 **회사 검색**: 회사명 또는 종목코드로 기업 조회
    * 📊 **EBITDA 계산**: 영업이익 + 감가상각비 + 무형자산상각비
    * 💾 **자동 캐싱**: 재무정보 자동 캐싱으로 빠른 응답
    * 🔒 **Rate Limiting**: API 호출 제한 자동 관리
    * ⚠️ **에러 처리**: 사용자 친화적 에러 메시지
    
    ## 데이터 출처
    
    [금융감독원 전자공시시스템 (OPENDART)](https://opendart.fss.or.kr/)
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 한글 인코딩을 위한 JSONResponse 커스텀
class UTF8JSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

# 기본 응답 클래스 설정
app.default_response_class = UTF8JSONResponse

# 라우터 등록
app.include_router(ebitda.router)


@app.get("/", tags=["Root"])
async def root():
    """루트 엔드포인트"""
    return {
        "message": "OPENDART EBITDA Calculator API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
