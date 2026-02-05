# npm 설치 가이드

## npm이란?

npm (Node Package Manager)은 Node.js와 함께 제공되는 패키지 관리자입니다. JavaScript/TypeScript 프로젝트의 의존성을 관리하는 데 사용됩니다.

## 설치 방법

### 방법 1: Node.js 공식 웹사이트에서 설치 (권장)

1. **Node.js 공식 웹사이트 방문**
   - URL: https://nodejs.org/
   - 또는 한국어 페이지: https://nodejs.org/ko/

2. **LTS 버전 다운로드**
   - LTS (Long Term Support) 버전을 선택하세요 (안정적이고 권장됨)
   - 현재 LTS 버전: v20.x.x 또는 v18.x.x
   - Windows용 `.msi` 파일을 다운로드하세요

3. **설치 실행**
   - 다운로드한 `.msi` 파일을 실행
   - 설치 마법사를 따라 진행
   - 기본 설정으로 설치하면 됩니다 (npm이 자동으로 포함됨)

4. **설치 확인**
   ```powershell
   node --version
   npm --version
   ```

### 방법 2: Chocolatey 사용 (Windows 패키지 관리자)

Chocolatey가 설치되어 있다면:

```powershell
choco install nodejs-lts
```

### 방법 3: winget 사용 (Windows 11/10)

```powershell
winget install OpenJS.NodeJS.LTS
```

## 설치 확인

PowerShell 또는 명령 프롬프트에서 다음 명령어를 실행하세요:

```powershell
# Node.js 버전 확인
node --version

# npm 버전 확인
npm --version
```

정상적으로 설치되었다면 다음과 같은 출력이 나옵니다:
```
v20.11.0
10.2.4
```

## 설치 후 해야 할 일

### 1. npm 캐시 확인 (선택사항)
```powershell
npm config get cache
```

### 2. npm 업데이트 (선택사항)
```powershell
npm install -g npm@latest
```

### 3. 프론트엔드 프로젝트 의존성 설치
```powershell
cd files
npm install
```

## 문제 해결

### npm 명령어를 찾을 수 없는 경우

1. **환경 변수 확인**
   - Node.js 설치 시 "Add to PATH" 옵션이 체크되어 있는지 확인
   - 재설치 시 PATH 옵션을 반드시 체크하세요

2. **PowerShell 재시작**
   - 설치 후 PowerShell을 완전히 종료하고 다시 실행

3. **시스템 재부팅**
   - 환경 변수가 제대로 적용되지 않았다면 시스템 재부팅

### 설치 경로 확인

Node.js와 npm은 보통 다음 경로에 설치됩니다:
- `C:\Program Files\nodejs\`
- `C:\Users\[사용자명]\AppData\Roaming\npm\`

### 수동으로 PATH 추가 (필요한 경우)

1. Windows 검색에서 "환경 변수" 검색
2. "시스템 환경 변수 편집" 선택
3. "환경 변수" 버튼 클릭
4. "시스템 변수"에서 "Path" 선택 후 "편집"
5. 다음 경로 추가:
   - `C:\Program Files\nodejs\`
   - `C:\Users\[사용자명]\AppData\Roaming\npm\`

## 유용한 링크

- **Node.js 공식 웹사이트**: https://nodejs.org/
- **Node.js 한국어 페이지**: https://nodejs.org/ko/
- **npm 공식 문서**: https://docs.npmjs.com/
- **npm 한국어 문서**: https://docs.npmjs.com/ko/
- **Node.js 다운로드**: https://nodejs.org/download/

## 추가 정보

### Node.js 버전 선택 가이드

- **LTS (Long Term Support)**: 안정적이고 장기 지원되는 버전 (권장)
- **Current**: 최신 기능이 포함된 버전 (실험적)

### npm 대체 도구

- **yarn**: Facebook에서 개발한 패키지 관리자
- **pnpm**: 더 빠르고 효율적인 패키지 관리자

## 다음 단계

npm이 설치되면 다음 명령어로 프론트엔드를 실행할 수 있습니다:

```powershell
cd files
npm install
npm run dev
```
