"""
재무정보 조회 서비스
"""
from typing import Dict, List, Any, Optional
from app.services.dart_client import dart_client, DartAPIError
from app.utils.cache import cache_manager
from app.models import FinancialAccount


class FinancialService:
    """재무정보 조회 서비스"""
    
    # 보고서 코드 매핑
    REPORT_NAMES = {
        "11011": "사업보고서",
        "11012": "반기보고서",
        "11013": "1분기보고서",
        "11014": "3분기보고서"
    }
    
    # 재무제표 구분 매핑
    FS_DIV_NAMES = {
        "CFS": "연결재무제표",
        "OFS": "개별재무제표"
    }
    
    async def get_financial_data(
        self,
        corp_code: str,
        year: int,
        report_code: str,
        fs_div: str = "CFS",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        재무정보 조회 (캐싱 적용)
        
        Args:
            corp_code: 고유번호 (8자리)
            year: 사업연도
            report_code: 보고서 코드
            fs_div: 재무제표 구분
            use_cache: 캐시 사용 여부
        
        Returns:
            재무정보 데이터
        """
        # 캐시 키 생성 인자
        cache_key_args = (corp_code, year, report_code, fs_div)
        
        # 캐시 확인
        if use_cache:
            cached_data = await cache_manager.get(*cache_key_args)
            if cached_data:
                cached_data["_from_cache"] = True
                return cached_data
        
        # API 호출
        try:
            response = await dart_client.get_financial_statements(
                corp_code=corp_code,
                bsns_year=str(year),
                reprt_code=report_code,
                fs_div=fs_div
            )
        except DartAPIError as e:
            if e.code == "013":
                raise DartAPIError(
                    "013",
                    f"{year}년 {self.REPORT_NAMES.get(report_code, report_code)} "
                    f"({self.FS_DIV_NAMES.get(fs_div, fs_div)})에 대한 "
                    f"재무정보가 존재하지 않습니다."
                )
            raise
        
        # 응답 검증
        if "list" not in response:
            raise DartAPIError(
                "INVALID_RESPONSE",
                "재무정보 데이터가 올바르지 않습니다."
            )
        
        # 데이터 정리
        cleaned_data = {
            "corp_code": corp_code,
            "year": year,
            "report_code": report_code,
            "fs_div": fs_div,
            "report_name": self.REPORT_NAMES.get(report_code, report_code),
            "fs_name": self.FS_DIV_NAMES.get(fs_div, fs_div),
            "rcept_no": response.get("rcept_no"),
            "accounts": response["list"],
            "_from_cache": False
        }
        
        # 캐시 저장
        await cache_manager.set(cleaned_data, *cache_key_args)
        
        return cleaned_data
    
    def extract_accounts_by_sj_div(
        self,
        accounts: List[Dict[str, Any]],
        sj_div: str
    ) -> List[FinancialAccount]:
        """
        재무제표 구분별 계정 추출
        
        Args:
            accounts: 전체 계정 리스트
            sj_div: 재무제표 구분 (BS/IS/CF 등)
        
        Returns:
            필터링된 계정 리스트
        """
        filtered = []
        
        for acc in accounts:
            if acc.get("sj_div") == sj_div:
                filtered.append(FinancialAccount(
                    account_nm=acc.get("account_nm", ""),
                    thstrm_amount=acc.get("thstrm_amount"),
                    thstrm_add_amount=acc.get("thstrm_add_amount"),
                    sj_div=acc.get("sj_div", ""),
                    currency=acc.get("currency", "KRW")
                ))
        
        return filtered
    
    def find_account_by_keywords(
        self,
        accounts: List[FinancialAccount],
        keywords: List[str]
    ) -> Optional[FinancialAccount]:
        """
        키워드로 계정 검색
        
        Args:
            accounts: 계정 리스트
            keywords: 검색 키워드 리스트
        
        Returns:
            매칭된 계정 또는 None
        """
        for account in accounts:
            account_name_lower = account.account_nm.lower()
            
            for keyword in keywords:
                if keyword.lower() in account_name_lower:
                    return account
        
        return None


# 싱글톤 인스턴스
financial_service = FinancialService()
