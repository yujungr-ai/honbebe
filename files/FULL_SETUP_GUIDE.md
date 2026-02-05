# 🎯 EBITDA Calculator - 전체 시스템 실행 가이드

백엔드(FastAPI) + 프론트엔드(Next.js) 통합 실행 가이드

## 📋 시스템 요구사항

### 필수 소프트웨어
- **Python**: 3.11 이상
- **Node.js**: 18.0 이상
- **npm**: 9.0 이상 (Node.js 설치 시 포함)
- **DART API Key**: https://opendart.fss.or.kr/ 에서 발급

### 선택사항
- **Git**: 버전 관리
- **Docker**: 컨테이너 실행 (선택)

---

## 🚀 빠른 시작 (Quick Start)

### 1️⃣ 백엔드 실행

```bash
# 1. 백엔드 디렉토리로 이동
cd ebitda-api

# 2. Python 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경변수 설정 (.env 파일 생성)
echo "DART_API_KEY=your_40_character_api_key" > .env

# 5. 서버 실행
uvicorn app.main:app --reload --port 8000
```

**✅ 확인**: http://localhost:8000/docs

---

### 2️⃣ 프론트엔드 실행

```bash
# 1. 프론트엔드 디렉토리로 이동
cd ebitda-frontend

# 2. 의존성 설치
npm install

# 3. 환경변수 설정 (.env.local 파일 생성)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# 4. 개발 서버 실행
npm run dev
```

**✅ 확인**: http://localhost:3000

---

## 📊 전체 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     브라우저                              │
│                http://localhost:3000                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP 요청
                     ↓
┌─────────────────────────────────────────────────────────┐
│               Next.js 프론트엔드                          │
│  - 검색 폼                                                │
│  - 결과 테이블                                            │
│  - 시계열 차트                                            │
│  - EBITDA 정보 패널                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ API 호출
                     ↓
┌─────────────────────────────────────────────────────────┐
│               FastAPI 백엔드                              │
│  GET /api/v1/ebitda                                      │
│  - 회사 검색 (corp_resolver)                             │
│  - 재무정보 조회 (financial_service)                      │
│  - EBITDA 계산 (ebitda_calculator)                       │
│  - 캐싱 (SQLite)                                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ API 요청
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 OPENDART API                             │
│           https://opendart.fss.or.kr                     │
│  - corpCode.xml (회사 매핑)                              │
│  - fnlttSinglAcntAll.json (재무제표)                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 환경변수 설정

### 백엔드 (.env)

```env
# OPENDART API Key (필수)
DART_API_KEY=your_40_character_api_key_here

# 캐시 설정
CACHE_DIR=./data/cache
CACHE_EXPIRY_DAYS=30

# Rate Limiting
RATE_LIMIT_PER_SECOND=5

# 로깅
LOG_LEVEL=INFO
```

### 프론트엔드 (.env.local)

```env
# API 서버 URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 테스트 시나리오

### 1. 백엔드 API 테스트

```bash
# 헬스 체크
curl http://localhost:8000/api/v1/health

# 삼성전자 EBITDA 조회
curl "http://localhost:8000/api/v1/ebitda?company=005930&year=2024&report_code=11014&fs_div=CFS"

# 현대자동차 EBITDA 조회
curl "http://localhost:8000/api/v1/ebitda?company=현대자동차&year=2023&report_code=11011&fs_div=OFS"
```

### 2. 프론트엔드 테스트

1. 브라우저에서 http://localhost:3000 접속
2. 검색 폼 입력:
   - 회사명: `삼성전자`
   - 사업연도: `2024`
   - 보고서: `3분기보고서`
   - 재무제표: `연결재무제표`
3. "EBITDA 조회" 클릭
4. 결과 확인:
   - ✅ 결과 테이블 표시
   - ✅ 시계열 차트 표시
   - ✅ 경고 메시지 표시
   - ✅ EBITDA 정보 패널 (우측 고정)

---

## 🎨 주요 기능

### 백엔드
- ✅ 회사명/종목코드 자동 변환
- ✅ EBITDA 자동 계산
- ✅ SQLite 캐싱 (30일)
- ✅ Rate Limiting (초당 5회)
- ✅ Exponential Backoff 재시도
- ✅ 사용자 친화 에러 메시지

### 프론트엔드
- ✅ 반응형 디자인 (모바일/태블릿/데스크톱)
- ✅ 검색 폼 (드롭다운 선택)
- ✅ 결과 테이블 (EBITDA 구성요소)
- ✅ 시계열 차트 (최근 5년, 라인/막대)
- ✅ EBITDA 정보 패널 (sticky, 스크롤 고정)
- ✅ 경고/에러 처리 (UX 친화적)
- ✅ 빈 상태 안내

---

## 📁 프로젝트 구조

```
project/
├── ebitda-api/              # 백엔드 (FastAPI)
│   ├── app/
│   │   ├── main.py          # 엔트리포인트
│   │   ├── config.py        # 설정
│   │   ├── models.py        # 데이터 모델
│   │   ├── services/        # 비즈니스 로직
│   │   ├── utils/           # 유틸리티
│   │   └── routers/         # API 라우터
│   ├── data/cache/          # 캐시 저장소
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
└── ebitda-frontend/         # 프론트엔드 (Next.js)
    ├── src/
    │   ├── app/             # 페이지
    │   ├── components/      # 컴포넌트
    │   ├── lib/             # API 클라이언트
    │   └── types/           # TypeScript 타입
    ├── package.json
    ├── .env.local
    └── README.md
```

---

## 🔧 트러블슈팅

### 문제: "Cannot connect to API server"

**원인**: 백엔드 서버 미실행

**해결**:
```bash
cd ebitda-api
uvicorn app.main:app --reload --port 8000
```

---

### 문제: "등록되지 않은 API 키"

**원인**: DART API 키 미설정

**해결**:
1. https://opendart.fss.or.kr/ 접속
2. 로그인 후 API 키 발급
3. `ebitda-api/.env` 파일에 키 입력
4. 서버 재시작

---

### 문제: "Port 8000 already in use"

**원인**: 포트 충돌

**해결**:
```bash
# 다른 포트 사용
uvicorn app.main:app --reload --port 8001

# 프론트엔드 .env.local 수정
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

### 문제: 데이터가 조회되지 않음

**원인**: 
- 회사명 오타
- 데이터가 없는 연도/보고서
- API 서버 에러

**해결**:
1. 정확한 회사명 또는 6자리 종목코드 입력
2. 다른 연도/보고서 시도
3. 백엔드 로그 확인
4. API 헬스 체크: http://localhost:8000/api/v1/health

---

## 📊 성능 최적화

### 백엔드
- **캐싱**: 재무정보 30일 캐싱
- **Rate Limiting**: OPENDART API 보호
- **멀티 워커**: 프로덕션에서 4개 워커 사용

### 프론트엔드
- **코드 스플리팅**: Next.js 자동 최적화
- **이미지 최적화**: Next.js Image 컴포넌트
- **CSS 최적화**: Tailwind CSS Purge

---

## 🚀 프로덕션 배포

### 백엔드
```bash
cd ebitda-api
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 프론트엔드
```bash
cd ebitda-frontend
npm run build
npm start
```

### Docker Compose (권장)
```yaml
version: '3.8'
services:
  backend:
    build: ./ebitda-api
    ports: ["8000:8000"]
    environment:
      - DART_API_KEY=${DART_API_KEY}
    volumes:
      - ./ebitda-api/data:/app/data
  
  frontend:
    build: ./ebitda-frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

실행:
```bash
docker-compose up -d
```

---

## 📝 추가 문서

- **백엔드**: `ebitda-api/README.md`
- **프론트엔드**: `ebitda-frontend/README.md`
- **설치 가이드**: `ebitda-frontend/SETUP.md`
- **테스트 예시**: `ebitda-api/TEST_EXAMPLES.md`
- **아키텍처**: `ebitda-api/ARCHITECTURE.md`

---

## 🤝 지원

문제가 발생하면:
1. 백엔드 로그 확인
2. 프론트엔드 브라우저 콘솔 확인
3. API 문서 참조: http://localhost:8000/docs
4. GitHub Issues 제출

---

## 📜 라이선스

MIT License

© 2024 EBITDA Calculator. All rights reserved.
