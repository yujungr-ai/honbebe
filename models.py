"""
API 요청/응답 데이터 모델
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CompanyInfo(BaseModel):
    """회사 정보"""
    corp_code: str = Field(..., description="고유번호 (8자리)")
    corp_name: str = Field(..., description="정식 회사명")
    stock_code: Optional[str] = Field(None, description="종목코드 (6자리)")


class PeriodInfo(BaseModel):
    """보고서 기간 정보"""
    year: int = Field(..., description="사업연도")
    report_code: str = Field(..., description="보고서 코드")
    report_name: str = Field(..., description="보고서명")
    fs_div: str = Field(..., description="재무제표 구분 (CFS/OFS)")
    fs_name: str = Field(..., description="재무제표명")


class ComponentAmount(BaseModel):
    """EBITDA 구성 요소"""
    label: str = Field(..., description="계정명")
    amount: float = Field(..., description="금액")
    currency: str = Field(default="KRW", description="통화")


class EBITDAComponents(BaseModel):
    """EBITDA 계산 구성요소"""
    operating_income: ComponentAmount = Field(..., description="영업이익")
    depreciation: ComponentAmount = Field(..., description="감가상각비")
    amortization: ComponentAmount = Field(..., description="무형자산상각비")


class EBITDAResult(BaseModel):
    """EBITDA 계산 결과"""
    total: float = Field(..., description="총 EBITDA")
    currency: str = Field(default="KRW", description="통화")
    basis: str = Field(..., description="계산 기준 (당기금액/누적금액)")


class SourceInfo(BaseModel):
    """데이터 출처 정보"""
    rcept_no: Optional[str] = Field(None, description="접수번호")
    fetched_at: datetime = Field(..., description="조회 시각")
    cached: bool = Field(default=False, description="캐시 사용 여부")


class EBITDAResponse(BaseModel):
    """EBITDA API 응답"""
    company: CompanyInfo = Field(..., description="회사 정보")
    period: PeriodInfo = Field(..., description="보고서 기간")
    components: EBITDAComponents = Field(..., description="EBITDA 구성요소")
    ebitda: EBITDAResult = Field(..., description="EBITDA 계산 결과")
    source: SourceInfo = Field(..., description="데이터 출처")
    warnings: List[str] = Field(default_factory=list, description="경고 메시지")


class ErrorResponse(BaseModel):
    """에러 응답"""
    error: str = Field(..., description="에러 코드")
    message: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="상세 설명")


# 내부 데이터 모델
class FinancialAccount(BaseModel):
    """재무제표 계정"""
    account_nm: str
    thstrm_amount: Optional[str] = None
    thstrm_add_amount: Optional[str] = None
    sj_div: str
    currency: str = "KRW"
