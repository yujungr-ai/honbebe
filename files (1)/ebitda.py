"""
EBITDA API 엔드포인트
"""
from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from app.models import EBITDAResponse, ErrorResponse, CompanyInfo, PeriodInfo, EBITDAComponents, ComponentAmount, EBITDAResult, SourceInfo
from app.services.corp_resolver import corp_resolver
from app.services.ebitda_calculator import ebitda_calculator
from app.services.dart_client import DartAPIError


router = APIRouter(prefix="/api/v1", tags=["EBITDA"])


@router.get(
    "/ebitda",
    response_model=EBITDAResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="EBITDA 계산",
    description="""
    OPENDART API를 활용하여 기업의 EBITDA를 계산합니다.
    
    **EBITDA 계산식:**
    ```
    EBITDA = 영업이익 + 감가상각비 + 무형자산상각비
    ```
    
    **보고서 코드:**
    - `11011`: 사업보고서 (연간)
    - `11012`: 반기보고서
    - `11013`: 1분기보고서
    - `11014`: 3분기보고서
    
    **재무제표 구분:**
    - `CFS`: 연결재무제표 (기본값)
    - `OFS`: 개별재무제표
    """
)
async def get_ebitda(
    company: str = Query(
        ...,
        description="회사명 또는 종목코드 (예: '삼성전자', '005930')",
        examples=["삼성전자", "005930"]
    ),
    year: int = Query(
        ...,
        description="사업연도 (예: 2024)",
        ge=2015,
        le=2030
    ),
    report_code: str = Query(
        ...,
        description="보고서 코드",
        pattern="^(11011|11012|11013|11014)$"
    ),
    fs_div: str = Query(
        "CFS",
        description="재무제표 구분 (CFS: 연결, OFS: 개별)",
        pattern="^(CFS|OFS)$"
    )
):
    """EBITDA 계산 API"""
    
    try:
        # 1. 회사명/종목코드 → corp_code 변환
        corp_info = await corp_resolver.resolve(company)
        
        # 2. EBITDA 계산
        result = await ebitda_calculator.calculate_ebitda(
            corp_code=corp_info["corp_code"],
            year=year,
            report_code=report_code,
            fs_div=fs_div
        )
        
        # 3. 응답 구성
        response = EBITDAResponse(
            company=CompanyInfo(
                corp_code=corp_info["corp_code"],
                corp_name=corp_info["corp_name"],
                stock_code=corp_info.get("stock_code")
            ),
            period=PeriodInfo(
                year=year,
                report_code=report_code,
                report_name=result.get("report_name", ""),
                fs_div=fs_div,
                fs_name="연결재무제표" if fs_div == "CFS" else "개별재무제표"
            ),
            components=EBITDAComponents(
                operating_income=ComponentAmount(
                    label=result["components"]["operating_income"]["label"],
                    amount=result["components"]["operating_income"]["amount"],
                    currency=result["currency"]
                ),
                depreciation=ComponentAmount(
                    label=result["components"]["depreciation"]["label"],
                    amount=result["components"]["depreciation"]["amount"],
                    currency=result["currency"]
                ),
                amortization=ComponentAmount(
                    label=result["components"]["amortization"]["label"],
                    amount=result["components"]["amortization"]["amount"],
                    currency=result["currency"]
                )
            ),
            ebitda=EBITDAResult(
                total=result["ebitda_total"],
                currency=result["currency"],
                basis=result["basis"]
            ),
            source=SourceInfo(
                rcept_no=result.get("rcept_no"),
                fetched_at=datetime.now(),
                cached=result.get("from_cache", False)
            ),
            warnings=result.get("warnings", [])
        )
        
        return response
    
    except DartAPIError as e:
        # DART API 에러 처리
        status_code = 404 if e.code in ["NOT_FOUND", "013"] else 500
        
        if e.code == "020":
            status_code = 429
        
        raise HTTPException(
            status_code=status_code,
            detail={
                "error": e.code,
                "message": e.message,
                "detail": "OPENDART API 에러가 발생했습니다."
            }
        )
    
    except Exception as e:
        # 기타 에러 처리
        raise HTTPException(
            status_code=500,
            detail={
                "error": "INTERNAL_ERROR",
                "message": str(e),
                "detail": "서버 내부 에러가 발생했습니다."
            }
        )


@router.get("/health", summary="헬스 체크")
async def health_check():
    """API 서버 상태 확인"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }
