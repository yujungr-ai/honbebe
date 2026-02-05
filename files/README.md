# EBITDA Calculator Frontend

OPENDART API를 활용한 기업 EBITDA 계산 웹 애플리케이션

## 설치 및 실행

### 1. 의존성 설치
```bash
npm install
```

### 2. 환경 변수 설정
`.env.local` 파일이 자동으로 생성되었습니다. 필요시 수정하세요:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 3. 개발 서버 실행
```bash
npm run dev
```

브라우저에서 `http://localhost:3000`으로 접속하세요.

## 프로젝트 구조

```
files/
├── app/              # Next.js App Router
│   ├── layout.tsx    # 루트 레이아웃
│   ├── page.tsx      # 메인 페이지
│   └── globals.css   # 전역 스타일
├── components/       # React 컴포넌트
│   ├── SearchForm.tsx
│   ├── ResultTable.tsx
│   ├── TimeSeriesChart.tsx
│   ├── EBITDAInfoPanel.tsx
│   └── ...
├── lib/              # 유틸리티 및 API
│   └── api.ts        # API 클라이언트
├── types.ts          # TypeScript 타입 정의
└── package.json      # 의존성 관리
```

## 기능

- ✅ 회사명/종목코드 검색
- ✅ EBITDA 계산 결과 표시
- ✅ 시계열 차트 시각화
- ✅ 반응형 디자인
- ✅ 에러 처리 및 로딩 상태
