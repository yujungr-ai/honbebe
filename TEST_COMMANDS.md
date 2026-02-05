# API 테스트 가이드

## 서버 실행

### 방법 1: 터미널에서 직접 실행
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 방법 2: 백그라운드 실행 (PowerShell)
```powershell
Start-Process python -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000" -WindowStyle Hidden
```

## 테스트 명령어

### 1. 헬스 체크
```powershell
# PowerShell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/health" -UseBasicParsing | Select-Object -ExpandProperty Content

# 또는 간단하게
curl http://127.0.0.1:8000/api/v1/health
```

### 2. API 문서 확인
브라우저에서 다음 URL을 열어주세요:
```
http://127.0.0.1:8000/docs
```

### 3. EBITDA 계산 API 테스트

#### 예시 1: 삼성전자 2023년 사업보고서 (연간)
```powershell
# PowerShell
$uri = "http://127.0.0.1:8000/api/v1/ebitda?company=005930&year=2023&report_code=11011&fs_div=CFS"
$response = Invoke-WebRequest -Uri $uri -UseBasicParsing
$json = $response.Content | ConvertFrom-Json
$json | ConvertTo-Json -Depth 5

# 또는 간단한 출력
Write-Host "회사: $($json.company.corp_name) ($($json.company.stock_code))"
Write-Host "EBITDA: $([math]::Round($json.ebitda.total/1000000000000, 2))조원"
Write-Host "영업이익: $([math]::Round($json.components.operating_income.amount/1000000000000, 2))조원"
```

#### 예시 2: 삼성전자 2024년 3분기보고서
```powershell
$uri = "http://127.0.0.1:8000/api/v1/ebitda?company=삼성전자&year=2024&report_code=11014&fs_div=CFS"
Invoke-WebRequest -Uri $uri -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

#### 예시 3: 현대자동차 2023년 사업보고서 (개별재무제표)
```powershell
$uri = "http://127.0.0.1:8000/api/v1/ebitda?company=현대자동차&year=2023&report_code=11011&fs_div=OFS"
Invoke-WebRequest -Uri $uri -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

#### 예시 4: SK하이닉스 2024년 반기보고서
```powershell
$uri = "http://127.0.0.1:8000/api/v1/ebitda?company=000660&year=2024&report_code=11012"
Invoke-WebRequest -Uri $uri -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

### 4. curl 사용 (Windows 10/11)
```bash
# 헬스 체크
curl http://127.0.0.1:8000/api/v1/health

# EBITDA 계산
curl "http://127.0.0.1:8000/api/v1/ebitda?company=005930&year=2023&report_code=11011&fs_div=CFS"
```

### 5. Python으로 테스트
```python
import requests
import json

# 헬스 체크
response = requests.get("http://127.0.0.1:8000/api/v1/health")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# EBITDA 계산
params = {
    "company": "005930",  # 삼성전자
    "year": 2023,
    "report_code": "11011",  # 사업보고서
    "fs_div": "CFS"  # 연결재무제표
}
response = requests.get("http://127.0.0.1:8000/api/v1/ebitda", params=params)
data = response.json()

print(f"회사: {data['company']['corp_name']} ({data['company']['stock_code']})")
print(f"EBITDA: {data['ebitda']['total']/1000000000000:.2f}조원")
print(f"영업이익: {data['components']['operating_income']['amount']/1000000000000:.2f}조원")
print(f"감가상각비: {data['components']['depreciation']['amount']/1000000000000:.2f}조원")
print(f"무형자산상각비: {data['components']['amortization']['amount']/1000000000000:.2f}조원")
```

## 보고서 코드 설명

- `11011`: 사업보고서 (연간)
- `11012`: 반기보고서
- `11013`: 1분기보고서
- `11014`: 3분기보고서

## 재무제표 구분

- `CFS`: 연결재무제표 (기본값)
- `OFS`: 개별재무제표

## 빠른 테스트 스크립트

PowerShell에서 다음 스크립트를 실행하세요:

```powershell
# 테스트 함수 정의
function Test-EBITDA {
    param(
        [string]$Company,
        [int]$Year,
        [string]$ReportCode = "11011",
        [string]$FsDiv = "CFS"
    )
    
    $uri = "http://127.0.0.1:8000/api/v1/ebitda?company=$Company&year=$Year&report_code=$ReportCode&fs_div=$FsDiv"
    
    try {
        $response = Invoke-WebRequest -Uri $uri -UseBasicParsing
        $json = $response.Content | ConvertFrom-Json
        
        Write-Host "=== EBITDA 계산 결과 ===" -ForegroundColor Green
        Write-Host "회사: $($json.company.corp_name) ($($json.company.stock_code))"
        Write-Host "기간: $($json.period.year)년 $($json.period.report_name)"
        Write-Host "EBITDA: $([math]::Round($json.ebitda.total/1000000000000, 2))조원"
        Write-Host "영업이익: $([math]::Round($json.components.operating_income.amount/1000000000000, 2))조원"
        Write-Host "감가상각비: $([math]::Round($json.components.depreciation.amount/1000000000000, 2))조원"
        Write-Host "무형자산상각비: $([math]::Round($json.components.amortization.amount/1000000000000, 2))조원"
        Write-Host "계산 기준: $($json.ebitda.basis)"
        
        if ($json.warnings.Count -gt 0) {
            Write-Host "`n경고:" -ForegroundColor Yellow
            $json.warnings | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
        }
    }
    catch {
        Write-Host "에러 발생: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.ErrorDetails.Message) {
            $errorJson = $_.ErrorDetails.Message | ConvertFrom-Json
            Write-Host "에러 코드: $($errorJson.detail.error)" -ForegroundColor Red
            Write-Host "메시지: $($errorJson.detail.message)" -ForegroundColor Red
        }
    }
}

# 사용 예시
Test-EBITDA -Company "005930" -Year 2023 -ReportCode "11011" -FsDiv "CFS"
Test-EBITDA -Company "삼성전자" -Year 2024 -ReportCode "11014"
Test-EBITDA -Company "현대자동차" -Year 2023 -ReportCode "11011" -FsDiv "OFS"
```

## 에러 확인

서버가 실행 중인지 확인:
```powershell
Get-Process python -ErrorAction SilentlyContinue
```

서버 로그 확인:
서버를 실행한 터미널 창에서 로그를 확인할 수 있습니다.

## 포트 확인

다른 프로세스가 8000 포트를 사용 중인지 확인:
```powershell
netstat -ano | findstr :8000
```
