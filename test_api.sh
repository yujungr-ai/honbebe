#!/bin/bash

# EBITDA API 테스트 스크립트
# 사용법: ./test_api.sh

BASE_URL="http://localhost:8000"

echo "=================================="
echo "OPENDART EBITDA Calculator API 테스트"
echo "=================================="
echo ""

# 컬러 코드
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 헬스 체크
echo -e "${BLUE}[1] 헬스 체크${NC}"
echo "GET $BASE_URL/api/v1/health"
curl -s "$BASE_URL/api/v1/health" | jq '.'
echo ""
echo ""

# 테스트 1: 삼성전자 2024년 3분기 연결 EBITDA
echo -e "${BLUE}[2] 삼성전자 2024년 3분기 연결 EBITDA${NC}"
echo "GET $BASE_URL/api/v1/ebitda?company=005930&year=2024&report_code=11014&fs_div=CFS"
curl -s "$BASE_URL/api/v1/ebitda?company=005930&year=2024&report_code=11014&fs_div=CFS" | jq '.'
echo ""
echo ""

# 테스트 2: 현대자동차 2023년 사업보고서 개별 EBITDA
echo -e "${BLUE}[3] 현대자동차 2023년 사업보고서 개별 EBITDA${NC}"
echo "GET $BASE_URL/api/v1/ebitda?company=현대자동차&year=2023&report_code=11011&fs_div=OFS"
curl -s "$BASE_URL/api/v1/ebitda?company=현대자동차&year=2023&report_code=11011&fs_div=OFS" | jq '.'
echo ""
echo ""

# 테스트 3: SK하이닉스 2024년 반기 연결 EBITDA
echo -e "${BLUE}[4] SK하이닉스 2024년 반기 연결 EBITDA${NC}"
echo "GET $BASE_URL/api/v1/ebitda?company=000660&year=2024&report_code=11012"
curl -s "$BASE_URL/api/v1/ebitda?company=000660&year=2024&report_code=11012" | jq '.'
echo ""
echo ""

# 에러 테스트: 존재하지 않는 회사
echo -e "${BLUE}[5] 에러 테스트: 존재하지 않는 회사${NC}"
echo "GET $BASE_URL/api/v1/ebitda?company=존재하지않는회사&year=2024&report_code=11011"
curl -s "$BASE_URL/api/v1/ebitda?company=존재하지않는회사&year=2024&report_code=11011" | jq '.'
echo ""
echo ""

echo -e "${GREEN}테스트 완료!${NC}"
