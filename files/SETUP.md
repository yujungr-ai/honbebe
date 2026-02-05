# 🚀 프론트엔드 실행 가이드

## 전체 시스템 실행 순서

### 1단계: 백엔드 API 서버 실행

```bash
# 백엔드 디렉토리로 이동
cd ebitda-api

# 의존성 설치 (최초 1회)
pip install -r requirements.txt

# .env 파일에 DART API 키 설정
# DART_API_KEY=your_40_character_key

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

**확인**: http://localhost:8000/docs 접속 (Swagger UI)

---

### 2단계: 프론트엔드 실행

```bash
# 프론트엔드 디렉토리로 이동
cd ebitda-frontend

# 의존성 설치 (최초 1회)
npm install

# 개발 서버 실행
npm run dev
```

**확인**: http://localhost:3000 접속

---

## 상세 실행 방법

### Windows

**터미널 1 (백엔드):**
```cmd
cd C:\path\to\ebitda-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**터미널 2 (프론트엔드):**
```cmd
cd C:\path\to\ebitda-frontend
npm install
npm run dev
```

### macOS / Linux

**터미널 1 (백엔드):**
```bash
cd /path/to/ebitda-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**터미널 2 (프론트엔드):**
```bash
cd /path/to/ebitda-frontend
npm install
npm run dev
```

---

## 환경변수 설정

### 백엔드 (.env)
```env
DART_API_KEY=your_40_character_api_key_here
CACHE_DIR=./data/cache
RATE_LIMIT_PER_SECOND=5
CACHE_EXPIRY_DAYS=30
LOG_LEVEL=INFO
```

### 프론트엔드 (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 첫 실행 체크리스트

- [ ] Node.js 설치 확인 (v18 이상)
- [ ] Python 설치 확인 (v3.11 이상)
- [ ] DART API 키 발급 (https://opendart.fss.or.kr/)
- [ ] 백엔드 .env 파일 생성 및 API 키 설정
- [ ] 백엔드 의존성 설치
- [ ] 백엔드 서버 실행 (8000 포트)
- [ ] 프론트엔드 의존성 설치
- [ ] 프론트엔드 서버 실행 (3000 포트)
- [ ] 브라우저에서 http://localhost:3000 접속
- [ ] 검색 테스트 (예: 삼성전자)

---

## 빠른 테스트

### 백엔드 API 테스트

```bash
# 헬스 체크
curl http://localhost:8000/api/v1/health

# EBITDA 조회 (삼성전자 2024년 3분기)
curl "http://localhost:8000/api/v1/ebitda?company=005930&year=2024&report_code=11014&fs_div=CFS"
```

### 프론트엔드 접속

1. 브라우저에서 http://localhost:3000 접속
2. 검색 폼에 입력:
   - 회사명: `삼성전자` (또는 `005930`)
   - 사업연도: `2024`
   - 보고서: `3분기보고서`
   - 재무제표: `연결재무제표`
3. "EBITDA 조회" 버튼 클릭
4. 결과 확인:
   - 결과 테이블
   - 시계열 차트
   - 경고 메시지

---

## 트러블슈팅

### 문제: "Cannot connect to API server"

**원인**: 백엔드 서버가 실행되지 않음

**해결**:
```bash
# 백엔드 디렉토리에서
uvicorn app.main:app --reload --port 8000
```

---

### 문제: "Module not found" (Python)

**원인**: 의존성 미설치

**해결**:
```bash
pip install -r requirements.txt
```

---

### 문제: "npm ERR! Missing script: dev"

**원인**: package.json 없음 또는 npm install 미실행

**해결**:
```bash
npm install
```

---

### 문제: "등록되지 않은 API 키"

**원인**: DART API 키 미설정 또는 잘못된 키

**해결**:
1. https://opendart.fss.or.kr/ 접속
2. 로그인 후 API 키 확인
3. .env 파일에 올바른 키 입력
4. 백엔드 서버 재시작

---

### 문제: 포트 충돌 (Port already in use)

**원인**: 8000 또는 3000 포트가 이미 사용 중

**해결**:
```bash
# 백엔드: 다른 포트 사용
uvicorn app.main:app --reload --port 8001

# 프론트엔드: 다른 포트 사용
npm run dev -- -p 3001

# 또는 기존 프로세스 종료
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

---

## 프로덕션 빌드

### 프론트엔드 빌드

```bash
cd ebitda-frontend
npm run build
npm start
```

빌드된 파일은 `.next` 디렉토리에 생성됩니다.

### 백엔드 프로덕션 실행

```bash
cd ebitda-api
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Docker 실행 (선택사항)

### 백엔드 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 프론트엔드 Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./ebitda-api
    ports:
      - "8000:8000"
    environment:
      - DART_API_KEY=${DART_API_KEY}
    volumes:
      - ./ebitda-api/data:/app/data

  frontend:
    build: ./ebitda-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

실행:
```bash
docker-compose up
```

---

## 개발 팁

### 핫 리로드

- **백엔드**: `--reload` 옵션으로 코드 변경 시 자동 재시작
- **프론트엔드**: Next.js Fast Refresh로 즉시 반영

### 로그 확인

```bash
# 백엔드: 터미널에 실시간 로그 출력
# 프론트엔드: 브라우저 개발자 도구 Console 탭
```

### API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 성능 최적화

### 백엔드
- 캐싱 활성화 (SQLite)
- Rate limiting 조정
- 워커 프로세스 증가

### 프론트엔드
- 프로덕션 빌드 사용
- 이미지 최적화
- 코드 스플리팅

---

## 지원

문제가 계속되면:
1. 백엔드 로그 확인
2. 프론트엔드 브라우저 콘솔 확인
3. API 서버 헬스 체크
4. DART API 키 유효성 확인
