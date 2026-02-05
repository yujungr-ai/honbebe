# 🚀 빠른 시작 가이드

## 1. API 키 발급

1. [OPENDART 홈페이지](https://opendart.fss.or.kr/) 접속
2. 회원가입 및 로그인
3. `인증키 신청/관리` 메뉴에서 API 키 발급
4. 40자리 API 키 확인

## 2. 환경 설정

`.env` 파일을 열고 API 키를 입력하세요:

```bash
# .env 파일 편집
vim .env

# 또는
nano .env
```

```env
DART_API_KEY=your_actual_40_character_api_key_here
```

## 3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 4. 서버 실행

### 개발 모드 (자동 리로드)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프로덕션 모드 (멀티 워커)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

서버가 실행되면 다음 URL에서 확인할 수 있습니다:
- API 문서: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Root: http://localhost:8000/

## 5. API 테스트

### 웹 브라우저로 테스트

http://localhost:8000/docs 에 접속하여 Swagger UI로 테스트

### cURL로 테스트

```bash
# 삼성전자 2024년 3분기 연결 EBITDA
curl "http://localhost:8000/api/v1/ebitda?company=005930&year=2024&report_code=11014&fs_div=CFS" | jq '.'

# 현대자동차 2023년 사업보고서 개별 EBITDA
curl "http://localhost:8000/api/v1/ebitda?company=현대자동차&year=2023&report_code=11011&fs_div=OFS" | jq '.'

# SK하이닉스 2024년 반기 연결 EBITDA
curl "http://localhost:8000/api/v1/ebitda?company=000660&year=2024&report_code=11012" | jq '.'
```

### 테스트 스크립트 실행

```bash
# jq 설치 필요 (JSON 포매터)
# Ubuntu/Debian: sudo apt-get install jq
# macOS: brew install jq

./test_api.sh
```

## 6. Python으로 API 호출

```python
import requests

# API 엔드포인트
url = "http://localhost:8000/api/v1/ebitda"

# 요청 파라미터
params = {
    "company": "005930",  # 삼성전자
    "year": 2024,
    "report_code": "11014",  # 3분기
    "fs_div": "CFS"  # 연결
}

# API 호출
response = requests.get(url, params=params)

# 결과 출력
if response.status_code == 200:
    data = response.json()
    
    print(f"회사: {data['company']['corp_name']}")
    print(f"EBITDA: {data['ebitda']['total']:,.0f} {data['ebitda']['currency']}")
    print(f"영업이익: {data['components']['operating_income']['amount']:,.0f}")
    print(f"감가상각비: {data['components']['depreciation']['amount']:,.0f}")
    print(f"무형자산상각비: {data['components']['amortization']['amount']:,.0f}")
else:
    print(f"에러: {response.json()}")
```

## 7. 응답 예시

```json
{
  "company": {
    "corp_code": "00126380",
    "corp_name": "삼성전자",
    "stock_code": "005930"
  },
  "period": {
    "year": 2024,
    "report_code": "11014",
    "report_name": "3분기보고서",
    "fs_div": "CFS",
    "fs_name": "연결재무제표"
  },
  "components": {
    "operating_income": {
      "label": "영업이익",
      "amount": 10500000000000,
      "currency": "KRW"
    },
    "depreciation": {
      "label": "감가상각비",
      "amount": 3500000000000,
      "currency": "KRW"
    },
    "amortization": {
      "label": "무형자산상각비",
      "amount": 500000000000,
      "currency": "KRW"
    }
  },
  "ebitda": {
    "total": 14500000000000,
    "currency": "KRW",
    "basis": "누적금액"
  },
  "source": {
    "rcept_no": "20241114000000",
    "fetched_at": "2026-02-05T06:30:00Z",
    "cached": false
  },
  "warnings": [
    "ℹ️ 3분기보고서의 누적금액 기준으로 계산되었습니다. 단일 분기 실적이 필요한 경우 이전 분기 데이터를 차감해야 합니다."
  ]
}
```

## 8. 트러블슈팅

### "등록되지 않은 API 키" 에러

- `.env` 파일에 올바른 API 키가 입력되었는지 확인
- API 키가 40자리인지 확인
- 서버를 재시작했는지 확인

### "요청 제한 초과" 에러

- OPENDART API는 일일 요청 제한이 있습니다
- 캐시된 데이터를 사용하면 API 호출 없이 응답합니다
- `RATE_LIMIT_PER_SECOND` 값을 낮춰보세요

### "데이터가 존재하지 않음" 에러

- 해당 연도/분기의 보고서가 제출되지 않았을 수 있습니다
- 보고서 코드가 올바른지 확인하세요
- 상장 전 데이터는 조회할 수 없습니다

### 캐시 초기화

```bash
# 캐시 디렉토리 삭제
rm -rf data/cache/*

# 서버 재시작
```

## 9. 프로덕션 배포

### Docker 배포 (권장)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 환경변수 설정

프로덕션 환경에서는 `.env` 파일 대신 환경변수를 직접 설정하는 것이 권장됩니다:

```bash
export DART_API_KEY=your_api_key
export CACHE_DIR=/var/cache/ebitda-api
export RATE_LIMIT_PER_SECOND=5
```

## 10. 모니터링

### 로그 확인

```bash
# 실시간 로그
tail -f /var/log/ebitda-api.log

# 최근 100줄
tail -n 100 /var/log/ebitda-api.log
```

### 헬스 체크

```bash
curl http://localhost:8000/api/v1/health
```

## 11. 지원

- 이슈: GitHub Issues
- 문서: http://localhost:8000/docs
- OPENDART 가이드: https://opendart.fss.or.kr/guide/main.do
