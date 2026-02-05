"""
corp_code 매핑 서비스 (corpCode.xml 처리)
"""
import zipfile
import io
from typing import Optional, Dict
from lxml import etree
from pathlib import Path
from datetime import datetime, timedelta
from app.config import settings
from app.services.dart_client import dart_client, DartAPIError


class CorpResolver:
    """회사명/종목코드 → corp_code 매핑 서비스"""
    
    def __init__(self):
        self.cache_file = settings.cache_dir / "corp_code.xml"
        self.mapping: Optional[Dict[str, Dict[str, str]]] = None
        self._cache_expiry_days = 30
    
    def _is_cache_valid(self) -> bool:
        """캐시 파일 유효성 검사"""
        if not self.cache_file.exists():
            return False
        
        # 파일 수정 시간 확인
        mtime = datetime.fromtimestamp(self.cache_file.stat().st_mtime)
        age = datetime.now() - mtime
        
        return age < timedelta(days=self._cache_expiry_days)
    
    async def _download_and_extract(self):
        """corpCode.xml 다운로드 및 추출"""
        print("[CorpResolver] corpCode.xml 다운로드 중...")
        
        # ZIP 파일 다운로드
        zip_data = await dart_client.get_corp_code_xml()
        
        # ZIP 압축 해제
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
            # CORPCODE.xml 추출
            xml_data = zip_file.read("CORPCODE.xml")
            
            # 캐시 파일로 저장
            self.cache_file.write_bytes(xml_data)
        
        print(f"[CorpResolver] corpCode.xml 저장 완료: {self.cache_file}")
    
    def _parse_xml(self) -> Dict[str, Dict[str, str]]:
        """
        XML 파싱 및 매핑 딕셔너리 생성
        
        Returns:
            {
                "corp_name": {...},
                "stock_code": {...}
            }
        """
        mapping = {
            "corp_name": {},
            "stock_code": {}
        }
        
        # XML 파싱
        tree = etree.parse(str(self.cache_file))
        root = tree.getroot()
        
        for company in root.findall("list"):
            corp_code = company.findtext("corp_code", "").strip()
            corp_name = company.findtext("corp_name", "").strip()
            stock_code = company.findtext("stock_code", "").strip()
            modify_date = company.findtext("modify_date", "").strip()
            
            if not corp_code:
                continue
            
            corp_data = {
                "corp_code": corp_code,
                "corp_name": corp_name,
                "stock_code": stock_code if stock_code else None,
                "modify_date": modify_date
            }
            
            # 회사명으로 매핑
            if corp_name:
                mapping["corp_name"][corp_name.lower()] = corp_data
            
            # 종목코드로 매핑 (상장사만)
            if stock_code:
                mapping["stock_code"][stock_code] = corp_data
        
        return mapping
    
    async def load_mapping(self, force_reload: bool = False):
        """
        매핑 데이터 로드
        
        Args:
            force_reload: 강제 재다운로드 여부
        """
        if self.mapping and not force_reload:
            return
        
        # 캐시 유효성 검사
        if force_reload or not self._is_cache_valid():
            await self._download_and_extract()
        
        # XML 파싱
        self.mapping = self._parse_xml()
        
        print(f"[CorpResolver] 매핑 완료: "
              f"회사명 {len(self.mapping['corp_name'])}개, "
              f"종목코드 {len(self.mapping['stock_code'])}개")
    
    async def resolve(self, query: str) -> Dict[str, str]:
        """
        회사명 또는 종목코드로 corp_code 검색
        
        Args:
            query: 회사명 또는 종목코드
        
        Returns:
            회사 정보 딕셔너리
        
        Raises:
            DartAPIError: 회사를 찾을 수 없는 경우
        """
        # 매핑 로드
        await self.load_mapping()
        
        # 종목코드로 검색 (숫자 6자리)
        if query.isdigit() and len(query) == 6:
            corp_data = self.mapping["stock_code"].get(query)
            if corp_data:
                return corp_data
        
        # 회사명으로 검색 (대소문자 무시)
        corp_data = self.mapping["corp_name"].get(query.lower())
        if corp_data:
            return corp_data
        
        # 부분 일치 검색 (회사명)
        query_lower = query.lower()
        for name, data in self.mapping["corp_name"].items():
            if query_lower in name or name in query_lower:
                return data
        
        # 찾지 못함
        raise DartAPIError(
            "NOT_FOUND",
            f"'{query}'에 해당하는 회사를 찾을 수 없습니다. "
            "정확한 회사명 또는 6자리 종목코드를 입력해주세요."
        )


# 싱글톤 인스턴스
corp_resolver = CorpResolver()
