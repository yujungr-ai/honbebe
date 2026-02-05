"""
EBITDA 계산 서비스
"""
from typing import Dict, Any, List, Tuple, Optional
from app.services.financial_service import financial_service
from app.services.dart_client import DartAPIError
from app.models import FinancialAccount


class EBITDACalculator:
    """EBITDA 계산 로직"""
    
    # 계정 검색 키워드
    OPERATING_INCOME_KEYWORDS = [
        "영업이익", "영업이익(손실)", "영업손익"
    ]
    
    DEPRECIATION_KEYWORDS = [
        "감가상각비", "유형자산상각비", "유형자산감가상각비"
    ]
    
    AMORTIZATION_KEYWORDS = [
        "무형자산상각비", "무형자산감가상각비"
    ]
    
    # 통합 감가상각 키워드 (감가+무형 통합)
    COMBINED_DEPRECIATION_KEYWORDS = [
        "감가상각비및무형자산상각비",
        "감가상각비 및 무형자산상각비",
        "감가ㆍ상각비"
    ]
    
    async def calculate_ebitda(
        self,
        corp_code: str,
        year: int,
        report_code: str,
        fs_div: str = "CFS"
    ) -> Dict[str, Any]:
        """
        EBITDA 계산
        
        Args:
            corp_code: 고유번호
            year: 사업연도
            report_code: 보고서 코드
            fs_div: 재무제표 구분
        
        Returns:
            EBITDA 계산 결과
        """
        # 재무정보 조회
        financial_data = await financial_service.get_financial_data(
            corp_code, year, report_code, fs_div
        )
        
        accounts = financial_data["accounts"]
        
        # 손익계산서(IS)에서 영업이익 추출
        is_accounts = financial_service.extract_accounts_by_sj_div(accounts, "IS")
        operating_income = self._find_operating_income(is_accounts)
        
        # 현금흐름표(CF)에서 감가상각비 추출
        cf_accounts = financial_service.extract_accounts_by_sj_div(accounts, "CF")
        depreciation, amortization = self._find_depreciation_amortization(cf_accounts)
        
        # 당기/누적 판단
        use_cumulative = self._should_use_cumulative(report_code)
        amount_field = "thstrm_add_amount" if use_cumulative else "thstrm_amount"
        
        # 금액 추출
        op_amount = self._parse_amount(
            getattr(operating_income, amount_field) if operating_income else None
        )
        dep_amount = self._parse_amount(
            getattr(depreciation, amount_field) if depreciation else None
        )
        amort_amount = self._parse_amount(
            getattr(amortization, amount_field) if amortization else None
        )
        
        # EBITDA 계산
        ebitda_total = op_amount + dep_amount + amort_amount
        
        # 경고 메시지 생성
        warnings = self._generate_warnings(
            operating_income,
            depreciation,
            amortization,
            use_cumulative,
            report_code
        )
        
        return {
            "components": {
                "operating_income": {
                    "label": operating_income.account_nm if operating_income else "영업이익",
                    "amount": op_amount,
                    "found": operating_income is not None
                },
                "depreciation": {
                    "label": depreciation.account_nm if depreciation else "감가상각비",
                    "amount": dep_amount,
                    "found": depreciation is not None
                },
                "amortization": {
                    "label": amortization.account_nm if amortization else "무형자산상각비",
                    "amount": amort_amount,
                    "found": amortization is not None
                }
            },
            "ebitda_total": ebitda_total,
            "currency": "KRW",
            "basis": "누적금액" if use_cumulative else "당기금액",
            "rcept_no": financial_data.get("rcept_no"),
            "from_cache": financial_data.get("_from_cache", False),
            "warnings": warnings,
            "report_name": financial_data.get("report_name", "")
        }
    
    def _find_operating_income(
        self,
        accounts: List[FinancialAccount]
    ) -> Optional[FinancialAccount]:
        """영업이익 계정 검색"""
        return financial_service.find_account_by_keywords(
            accounts,
            self.OPERATING_INCOME_KEYWORDS
        )
    
    def _find_depreciation_amortization(
        self,
        accounts: List[FinancialAccount]
    ) -> Tuple[Optional[FinancialAccount], Optional[FinancialAccount]]:
        """
        감가상각비 및 무형자산상각비 검색
        
        Returns:
            (감가상각비, 무형자산상각비) 튜플
        """
        # 통합 계정 우선 검색
        combined = financial_service.find_account_by_keywords(
            accounts,
            self.COMBINED_DEPRECIATION_KEYWORDS
        )
        
        if combined:
            # 통합 계정이 있으면 둘 다 같은 계정 반환
            return (combined, combined)
        
        # 개별 계정 검색
        depreciation = financial_service.find_account_by_keywords(
            accounts,
            self.DEPRECIATION_KEYWORDS
        )
        
        amortization = financial_service.find_account_by_keywords(
            accounts,
            self.AMORTIZATION_KEYWORDS
        )
        
        return (depreciation, amortization)
    
    def _parse_amount(self, amount_str: Optional[str]) -> float:
        """금액 문자열을 숫자로 변환"""
        if not amount_str:
            return 0.0
        
        try:
            # 쉼표 제거 후 변환
            return float(amount_str.replace(",", ""))
        except (ValueError, AttributeError):
            return 0.0
    
    def _should_use_cumulative(self, report_code: str) -> bool:
        """
        누적금액 사용 여부 판단
        
        사업보고서(11011)는 연간이므로 당기금액 사용
        분기/반기는 누적금액이 일반적
        """
        return report_code != "11011"
    
    def _generate_warnings(
        self,
        operating_income: Optional[FinancialAccount],
        depreciation: Optional[FinancialAccount],
        amortization: Optional[FinancialAccount],
        use_cumulative: bool,
        report_code: str
    ) -> List[str]:
        """경고 메시지 생성"""
        warnings = []
        
        # 계정 누락 경고
        if not operating_income:
            warnings.append(
                "⚠️ 영업이익 계정을 찾을 수 없습니다. "
                "EBITDA 계산이 정확하지 않을 수 있습니다."
            )
        
        if not depreciation:
            warnings.append(
                "⚠️ 감가상각비 계정을 찾을 수 없습니다. "
                "현금흐름표에 해당 항목이 없는지 확인해주세요."
            )
        
        if not amortization:
            # 통합 계정일 수 있으므로 약한 경고
            if depreciation and "무형자산" not in depreciation.account_nm:
                warnings.append(
                    "ℹ️ 무형자산상각비가 별도 계정으로 존재하지 않습니다. "
                    "감가상각비에 포함되어 있을 수 있습니다."
                )
        
        # 누적/당기 안내
        if use_cumulative:
            report_name = financial_service.REPORT_NAMES.get(report_code, "")
            warnings.append(
                f"ℹ️ {report_name}의 누적금액 기준으로 계산되었습니다. "
                "단일 분기 실적이 필요한 경우 이전 분기 데이터를 차감해야 합니다."
            )
        else:
            warnings.append(
                "ℹ️ 당기금액 기준으로 계산되었습니다 (연간 실적)."
            )
        
        return warnings


# 싱글톤 인스턴스
ebitda_calculator = EBITDACalculator()
