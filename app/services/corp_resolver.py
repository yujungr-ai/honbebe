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
        """corpCode.xml 다운로드 및 추출 (ZIP 또는 직접 XML 지원)"""
        print("[CorpResolver] corpCode.xml 다운로드 중...")
        
        import json
        
        try:
            # 데이터 다운로드
            response_data = await dart_client.get_corp_code_xml()
            
            # 1. JSON 에러 응답 확인
            if response_data.startswith(b'{'):
                try:
                    error_data = json.loads(response_data.decode('utf-8'))
                    error_msg = error_data.get('message', '알 수 없는 에러')
                    raise DartAPIError(
                        error_data.get('status', 'UNKNOWN'),
                        f"corpCode.xml 다운로드 실패: {error_msg}"
                    )
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass  # JSON이 아닐 수 있음
            
            # 2. ZIP 파일인 경우 (ZIP 파일은 PK로 시작하고 zipfile로 확인)
            xml_data = None
            # ZIP 파일 여부를 안전하게 확인
            is_zip = False
            if response_data.startswith(b'PK'):
                try:
                    # zipfile.is_zipfile()로 실제 ZIP 파일인지 확인
                    zip_buffer = io.BytesIO(response_data)
                    is_zip = zipfile.is_zipfile(zip_buffer)
                except Exception:
                    is_zip = False
            
            if is_zip:
                try:
                    # ZIP 압축 해제 시도
                    zip_buffer = io.BytesIO(response_data)
                    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                        # CORPCODE.xml 또는 corpCode.xml 파일명 시도
                        xml_filename = None
                        for name in ["CORPCODE.xml", "corpCode.xml", "CORPCODE.XML"]:
                            if name in zip_file.namelist():
                                xml_filename = name
                                break
                        
                        if xml_filename:
                            xml_data = zip_file.read(xml_filename)
                            print(f"[CorpResolver] ZIP에서 {xml_filename} 추출 완료")
                        else:
                            # ZIP 내 파일 목록 출력
                            available_files = ", ".join(zip_file.namelist())
                            raise DartAPIError(
                                "INVALID_RESPONSE",
                                f"ZIP 파일에 XML 파일이 없습니다. 포함된 파일: {available_files}"
                            )
                except (zipfile.BadZipFile, zipfile.LargeZipFile, ValueError, OSError) as e:
                    # ZIP 파싱 실패 - XML로 처리 시도
                    print(f"[CorpResolver] ZIP 파싱 실패 (응답이 ZIP이 아닐 수 있음): {type(e).__name__} - {str(e)}")
                    xml_data = None  # XML로 처리하도록 계속 진행
                except Exception as e:
                    # 모든 예외를 잡아서 XML로 처리 시도
                    print(f"[CorpResolver] ZIP 처리 중 예외 발생 ({type(e).__name__}): {str(e)}")
                    xml_data = None
            
            # 3. 직접 XML인 경우 (<?xml 또는 <로 시작)
            if xml_data is None:
                xml_start_markers = [b'<?xml', b'<result', b'<list', b'<corpCode', b'<corp_code', b'<']
                response_stripped = response_data.strip()
                is_xml = any(response_stripped.startswith(marker) for marker in xml_start_markers)
                
                # XML로 보이지만 확실하지 않은 경우, XML 파싱 시도
                if not is_xml and len(response_data) > 0:
                    # 첫 100바이트에 '<' 문자가 있으면 XML일 가능성
                    try:
                        first_bytes = response_data[:100]
                        if b'<' in first_bytes:
                            # lxml로 파싱 시도하여 XML인지 확인
                            try:
                                etree.fromstring(response_data)
                                is_xml = True
                                print("[CorpResolver] XML 파싱으로 형식 확인됨")
                            except etree.XMLSyntaxError:
                                pass  # XML이 아님
                    except Exception:
                        pass
                
                if is_xml:
                    # 직접 XML 데이터로 저장
                    xml_data = response_data
                    print("[CorpResolver] 직접 XML 형식으로 저장")
                else:
                    # XML도 아닌 경우 에러
                    # 응답의 처음 200바이트만 확인용으로 출력
                    try:
                        preview = response_data[:200].decode('utf-8', errors='replace')
                    except:
                        preview = str(response_data[:50])
                    raise DartAPIError(
                        "INVALID_RESPONSE",
                        f"corpCode.xml 응답 형식을 확인할 수 없습니다. "
                        f"응답 시작 부분: {preview[:100]}..."
                    )
            
            # XML 데이터 저장
            if xml_data:
                self.cache_file.write_bytes(xml_data)
                print(f"[CorpResolver] corpCode.xml 저장 완료: {self.cache_file}")
            else:
                raise DartAPIError(
                    "INVALID_RESPONSE",
                    "corpCode.xml 파일을 저장할 수 없습니다."
                )
            
        except DartAPIError:
            # DartAPIError는 그대로 전파
            raise
        except Exception as e:
            raise DartAPIError(
                "DOWNLOAD_ERROR",
                f"corpCode.xml 다운로드 중 오류 발생: {str(e)}"
            )
    
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
