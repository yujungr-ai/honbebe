# 오류 수정 가이드

## 발견된 문제

### 1. 포트 충돌 (Errno 10048)
**증상**: 서버 시작 시 "각 소켓 주소는 하나만 사용할 수 있습니다" 에러

**원인**: 포트 8000이 이미 다른 프로세스에서 사용 중

**해결 방법**:
```powershell
# 1. 실행 중인 Python 프로세스 확인
Get-Process python -ErrorAction SilentlyContinue

# 2. 포트 8000을 사용하는 프로세스 종료
$processId = (netstat -ano | findstr :8000 | Select-String "LISTENING").ToString().Split()[-1]
Stop-Process -Id $processId -Force

# 또는 모든 Python 프로세스 종료
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 3. 서버 재시작
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. "File is not a zip file" 에러
**증상**: API 호출 시 "File is not a zip file" 에러 발생

**원인**: 
- `zipfile.ZipFile()` 생성 시 예외가 제대로 처리되지 않음
- ZIP 파일이 아닌 응답을 처리하는 로직에 문제

**수정 필요 사항**:
1. `zipfile.is_zipfile()` 사용하여 ZIP 파일 여부 사전 확인
2. 예외 처리 범위 확대
3. 더 안전한 XML 감지 로직
