# 🧪 API 테스트 예시

## cURL 테스트 예시

### 1. 삼성전자 2024년 3분기 연결 EBITDA

```bash
curl -X GET "http://localhost:8000/api/v1/ebitda?company=005930&year=2024&report_code=11014&fs_div=CFS" \
  -H "accept: application/json" | jq '.'
```

**설명:**
- 회사: 삼성전자 (종목코드: 005930)
- 연도: 2024년
- 보고서: 3분기보고서 (11014)
- 재무제표: 연결재무제표 (CFS)

**예상 결과:**
```json
{
  "company": {
    "corp_code": "00126380",
    "corp_name": "삼성전자",
    "stock_code": "005930"
  },
  "ebitda": {
    "total": 45000000000000,
    "currency": "KRW",
    "basis": "누적금액"
  }
}
```

---

### 2. 현대자동차 2023년 사업보고서 개별 EBITDA

```bash
curl -X GET "http://localhost:8000/api/v1/ebitda?company=%ED%98%84%EB%8C%80%EC%9E%90%EB%8F%99%EC%B0%A8&year=2023&report_code=11011&fs_div=OFS" \
  -H "accept: application/json" | jq '.'
```

**URL 인코딩 없이:**
```bash
curl -G "http://localhost:8000/api/v1/ebitda" \
  --data-urlencode "company=현대자동차" \
  --data-urlencode "year=2023" \
  --data-urlencode "report_code=11011" \
  --data-urlencode "fs_div=OFS" | jq '.'
```

**설명:**
- 회사: 현대자동차 (회사명으로 검색)
- 연도: 2023년
- 보고서: 사업보고서 (11011) - 연간 실적
- 재무제표: 개별재무제표 (OFS)

---

### 3. SK하이닉스 2024년 반기 연결 EBITDA

```bash
curl -X GET "http://localhost:8000/api/v1/ebitda?company=000660&year=2024&report_code=11012" \
  -H "accept: application/json" | jq '.'
```

**설명:**
- 회사: SK하이닉스 (종목코드: 000660)
- 연도: 2024년
- 보고서: 반기보고서 (11012)
- 재무제표: CFS (기본값, 생략 가능)

---

## Python 테스트 예시

### 기본 사용법

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def get_ebitda(company, year, report_code, fs_div="CFS"):
    """EBITDA 조회"""
    url = f"{BASE_URL}/api/v1/ebitda"
    
    params = {
        "company": company,
        "year": year,
        "report_code": report_code,
        "fs_div": fs_div
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return None

# 테스트 1: 삼성전자
result = get_ebitda("005930", 2024, "11014", "CFS")
if result:
    print(f"회사: {result['company']['corp_name']}")
    print(f"EBITDA: {result['ebitda']['total']:,.0f} KRW")

# 테스트 2: 현대자동차
result = get_ebitda("현대자동차", 2023, "11011", "OFS")
if result:
    print(f"회사: {result['company']['corp_name']}")
    print(f"EBITDA: {result['ebitda']['total']:,.0f} KRW")

# 테스트 3: SK하이닉스
result = get_ebitda("000660", 2024, "11012")
if result:
    print(f"회사: {result['company']['corp_name']}")
    print(f"EBITDA: {result['ebitda']['total']:,.0f} KRW")
```

### 상세 정보 출력

```python
def print_ebitda_detail(data):
    """EBITDA 상세 정보 출력"""
    if not data:
        return
    
    print("=" * 60)
    print(f"📊 {data['company']['corp_name']} EBITDA 분석")
    print("=" * 60)
    
    # 기간 정보
    period = data['period']
    print(f"\n📅 보고 기간: {period['year']}년 {period['report_name']}")
    print(f"📋 재무제표: {period['fs_name']}")
    
    # EBITDA 구성요소
    print(f"\n💰 EBITDA 구성:")
    components = data['components']
    
    op_income = components['operating_income']
    print(f"  영업이익: {op_income['amount']:>20,.0f} {op_income['currency']}")
    
    depreciation = components['depreciation']
    print(f"  + 감가상각비: {depreciation['amount']:>20,.0f} {depreciation['currency']}")
    
    amortization = components['amortization']
    print(f"  + 무형자산상각비: {amortization['amount']:>16,.0f} {amortization['currency']}")
    
    print(f"  {'─' * 50}")
    
    ebitda = data['ebitda']
    print(f"  EBITDA: {ebitda['total']:>20,.0f} {ebitda['currency']}")
    print(f"  (계산 기준: {ebitda['basis']})")
    
    # 경고 메시지
    if data.get('warnings'):
        print(f"\n⚠️ 참고 사항:")
        for warning in data['warnings']:
            print(f"  {warning}")
    
    # 데이터 출처
    source = data['source']
    print(f"\n📌 데이터 출처:")
    print(f"  접수번호: {source.get('rcept_no', 'N/A')}")
    print(f"  조회 시각: {source['fetched_at']}")
    print(f"  캐시 사용: {'예' if source['cached'] else '아니오'}")
    print("=" * 60)

# 사용 예시
result = get_ebitda("005930", 2024, "11014")
print_ebitda_detail(result)
```

### 여러 회사 비교

```python
def compare_companies(companies, year, report_code):
    """여러 회사의 EBITDA 비교"""
    results = []
    
    for company in companies:
        data = get_ebitda(company, year, report_code)
        if data:
            results.append({
                "name": data['company']['corp_name'],
                "ebitda": data['ebitda']['total'],
                "operating_income": data['components']['operating_income']['amount']
            })
    
    # 정렬 (EBITDA 기준 내림차순)
    results.sort(key=lambda x: x['ebitda'], reverse=True)
    
    # 출력
    print(f"\n📊 {year}년 {report_code} EBITDA 비교")
    print("=" * 80)
    print(f"{'순위':<5} {'회사명':<20} {'EBITDA':>20} {'영업이익':>20}")
    print("-" * 80)
    
    for idx, result in enumerate(results, 1):
        print(f"{idx:<5} {result['name']:<20} {result['ebitda']:>20,.0f} {result['operating_income']:>20,.0f}")
    
    print("=" * 80)

# 사용 예시: 반도체 3사 비교
compare_companies(
    companies=["005930", "000660", "000990"],  # 삼성전자, SK하이닉스, DB하이텍
    year=2024,
    report_code="11014"
)
```

### 에러 처리

```python
def get_ebitda_safe(company, year, report_code, fs_div="CFS"):
    """안전한 EBITDA 조회 (에러 처리 포함)"""
    try:
        url = f"{BASE_URL}/api/v1/ebitda"
        params = {
            "company": company,
            "year": year,
            "report_code": report_code,
            "fs_div": fs_div
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json(), None
        
        elif response.status_code == 404:
            error = response.json()
            return None, f"데이터 없음: {error['detail']['message']}"
        
        elif response.status_code == 429:
            return None, "요청 제한 초과. 잠시 후 다시 시도해주세요."
        
        else:
            error = response.json()
            return None, f"에러 발생: {error['detail']['message']}"
    
    except requests.exceptions.Timeout:
        return None, "요청 시간 초과"
    
    except requests.exceptions.ConnectionError:
        return None, "서버에 연결할 수 없습니다"
    
    except Exception as e:
        return None, f"알 수 없는 에러: {str(e)}"

# 사용 예시
data, error = get_ebitda_safe("005930", 2024, "11014")

if error:
    print(f"❌ {error}")
else:
    print(f"✅ EBITDA: {data['ebitda']['total']:,.0f} KRW")
```

---

## JavaScript/Node.js 테스트 예시

```javascript
// axios 사용
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function getEbitda(company, year, reportCode, fsDiv = 'CFS') {
    try {
        const response = await axios.get(`${BASE_URL}/api/v1/ebitda`, {
            params: {
                company,
                year,
                report_code: reportCode,
                fs_div: fsDiv
            }
        });
        
        return response.data;
    } catch (error) {
        if (error.response) {
            console.error('Error:', error.response.data);
        } else {
            console.error('Error:', error.message);
        }
        return null;
    }
}

// 테스트
(async () => {
    const result = await getEbitda('005930', 2024, '11014');
    
    if (result) {
        console.log(`회사: ${result.company.corp_name}`);
        console.log(`EBITDA: ${result.ebitda.total.toLocaleString()} KRW`);
    }
})();
```

---

## 보고서 코드 참고

| 코드 | 보고서명 | 설명 |
|-----|---------|------|
| 11011 | 사업보고서 | 연간 실적 (당기금액 사용) |
| 11012 | 반기보고서 | 1월~6월 누적 |
| 11013 | 1분기보고서 | 1월~3월 누적 |
| 11014 | 3분기보고서 | 1월~9월 누적 |

## 재무제표 구분

| 코드 | 재무제표 | 설명 |
|-----|---------|------|
| CFS | 연결재무제표 | 종속회사 포함 |
| OFS | 개별재무제표 | 모회사 단독 |

---

## 헬스 체크

```bash
# 서버 상태 확인
curl http://localhost:8000/api/v1/health

# 예상 응답
{
  "status": "ok",
  "timestamp": "2026-02-05T06:30:00.000000"
}
```
