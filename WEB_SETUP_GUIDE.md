# 웹 프론트엔드 설정 가이드

## 문제 해결

### 1. 한글 인코딩 문제
✅ **해결 완료**: FastAPI 응답에 UTF-8 인코딩을 명시적으로 설정했습니다.

### 2. 웹 프론트엔드 실행 방법

## 프론트엔드 설정 및 실행

### 1단계: 프론트엔드 디렉토리로 이동
```powershell
cd files
```

### 2단계: 의존성 설치
```powershell
npm install
```

또는 yarn을 사용하는 경우:
```powershell
yarn install
```

### 3단계: 환경 변수 설정
`files` 디렉토리에 `.env.local` 파일을 생성하고 다음 내용을 추가:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 4단계: 개발 서버 실행
```powershell
npm run dev
```

서버가 실행되면 브라우저에서 `http://localhost:3000`으로 접속할 수 있습니다.

## 전체 실행 순서

### 터미널 1: 백엔드 서버
```powershell
# 프로젝트 루트에서
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 터미널 2: 프론트엔드 서버
```powershell
# files 디렉토리에서
cd files
npm install
npm run dev
```

## 프론트엔드 기능

프론트엔드는 다음 기능을 제공합니다:

1. **검색 폼**: 회사명/종목코드, 연도, 보고서 선택
2. **결과 테이블**: EBITDA 계산 결과를 표 형식으로 표시
3. **차트**: 시계열 데이터 시각화
4. **정보 패널**: EBITDA 설명 및 안내
5. **에러 처리**: 사용자 친화적 에러 메시지
6. **경고 알림**: 데이터 품질 관련 경고 표시

## 문제 해결

### 포트 충돌
프론트엔드가 3000 포트를 사용합니다. 다른 포트를 사용하려면:
```powershell
npm run dev -- -p 3001
```

### API 연결 오류
`.env.local` 파일의 `NEXT_PUBLIC_API_URL`이 올바른지 확인하세요.

### 한글 깨짐
백엔드 서버를 재시작하면 UTF-8 인코딩이 적용됩니다.
