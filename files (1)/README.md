# OPENDART EBITDA Calculator API

OPENDART API를 활용하여 기업의 EBITDA를 계산하는 FastAPI 백엔드

## 📁 프로젝트 구조

```
ebitda-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션 엔트리포인트
│   ├── config.py               # 설정 관리 (환경변수)
│   ├── models.py               # Pydantic 모델 정의
│   ├── services/
│   │   ├── __init__.py
│   │   ├── dart_client.py      # OPENDART API 클라이언트
│   │   ├── corp_resolver.py    # corp_code 매핑 서비스
│   │   ├── financial_service.py # 재무정보 조회 서비스
│   │   └── ebitda_calculator.py # EBITDA 계산 로직
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cache.py            # 캐싱 유틸리티
│   │   └── rate_limiter.py     # Rate limiting
│   └── routers/
│       ├── __init__.py
│       └── ebitda.py           # EBITDA API 엔드포인트
├── data/
│   └── cache/                  # 캐시 데이터 저장
├── .env                        # 환경변수 (API KEY)
├── .env.example                # 환경변수 템플릿
├── requirements.txt            # Python 의존성
└── README.md                   # 이 파일
```

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일 편집:

```
DART_API_KEY=your_api_key_here
CACHE_DIR=./data/cache
RATE_LIMIT_PER_SECOND=5
CACHE_EXPIRY_DAYS=30
```

### 3. 서버 실행

```bash
# 개발 모드 (자동 리로드)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📡 API 사용법

### 엔드포인트: `GET /api/v1/ebitda`

**쿼리 파라미터:**
- `company` (필수): 회사명 또는 종목코드 (예: "삼성전자", "005930")
- `year` (필수): 사업연도 (예: 2024)
- `report_code` (필수): 보고서 코드
  - `11011`: 사업보고서 (연간)
  - `11012`: 반기보고서
  - `11013`: 1분기보고서
  - `11014`: 3분기보고서
- `fs_div` (선택, 기본값: "CFS"): 재무제표 구분
  - `CFS`: 연결재무제표
  - `OFS`: 개별재무제표

### 테스트 예시

```bash
# 1. 삼성전자 2024년 3분기 연결 EBITDA
curl "http://localhost:8000/api/v1/ebitda?company=005930&year=2024&report_code=11014&fs_div=CFS"

# 2. 현대자동차 2023년 사업보고서 개별 EBITDA
curl "http://localhost:8000/api/v1/ebitda?company=현대자동차&year=2023&report_code=11011&fs_div=OFS"

# 3. SK하이닉스 2024년 반기 연결 EBITDA
curl "http://localhost:8000/api/v1/ebitda?company=000660&year=2024&report_code=11012"
```

## 📊 응답 예시

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
    "basis": "당기금액"
  },
  "source": {
    "rcept_no": "20241114000000",
    "fetched_at": "2026-02-05T06:30:00Z",
    "cached": false
  },
  "warnings": [
    "당기금액 기준으로 계산되었습니다. 누적금액이 필요한 경우 별도 요청이 필요합니다."
  ]
}
```

## 🔧 주요 기능

### 1. 자동 캐싱
- `corp_code` 매핑: 최초 1회 다운로드 후 로컬 캐시 (30일 유효)
- 재무정보: (corp_code, year, report_code, fs_div) 조합으로 SQLite 캐싱

### 2. Rate Limiting
- OPENDART API 호출 제한 대응
- 초당 5회 요청 제한 (설정 가능)
- Exponential backoff 재시도

### 3. 에러 핸들링
- `020`: 요청 제한 초과 → 사용자 친화 메시지
- `013`: 데이터 없음 → 명확한 안내
- `000`: 정상 / `010`: 등록되지 않은 키

### 4. 경고 시스템
- 누적/당기 금액 구분 알림
- 데이터 품질 이슈 감지

## 🛠️ 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **httpx**: 비동기 HTTP 클라이언트
- **SQLite**: 경량 캐시 데이터베이스
- **python-dotenv**: 환경변수 관리
- **lxml**: XML 파싱

## 📝 라이선스

MIT License
