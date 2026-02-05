'use client';

import { Info, AlertCircle, BookOpen } from 'lucide-react';

export default function EBITDAInfoPanel() {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg shadow-md p-6 sticky top-6">
      {/* 제목 */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
          <BookOpen className="w-6 h-6 text-white" />
        </div>
        <h3 className="text-xl font-bold text-gray-900">
          EBITDA 개념 가이드
        </h3>
      </div>

      {/* EBITDA 정의 */}
      <div className="mb-6">
        <div className="flex items-start gap-2 mb-2">
          <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">EBITDA란?</h4>
            <p className="text-sm text-gray-700 leading-relaxed">
              <strong>E</strong>arnings <strong>B</strong>efore <strong>I</strong>nterest, 
              <strong>T</strong>axes, <strong>D</strong>epreciation and <strong>A</strong>mortization의 약자로, 
              이자·세금·감가상각비 차감 전 영업이익을 의미합니다.
            </p>
          </div>
        </div>

        {/* 계산 공식 */}
        <div className="mt-4 p-4 bg-white rounded-lg border border-blue-200">
          <p className="text-sm font-mono text-center text-gray-900">
            <strong>EBITDA</strong> = 영업이익 + 감가상각비 + 무형자산상각비
          </p>
        </div>
      </div>

      {/* 구성 요소 설명 */}
      <div className="mb-6">
        <h4 className="font-semibold text-gray-900 mb-3">구성 요소</h4>
        <div className="space-y-3">
          <div className="flex items-start gap-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-1.5 flex-shrink-0"></div>
            <div className="text-sm">
              <strong className="text-gray-900">영업이익:</strong>
              <span className="text-gray-700"> 본업에서 창출한 이익 (매출액 - 매출원가 - 판관비)</span>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-1.5 flex-shrink-0"></div>
            <div className="text-sm">
              <strong className="text-gray-900">감가상각비:</strong>
              <span className="text-gray-700"> 유형자산(건물, 기계 등)의 가치 감소분</span>
            </div>
          </div>
          <div className="flex items-start gap-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full mt-1.5 flex-shrink-0"></div>
            <div className="text-sm">
              <strong className="text-gray-900">무형자산상각비:</strong>
              <span className="text-gray-700"> 무형자산(특허권, 소프트웨어 등)의 가치 감소분</span>
            </div>
          </div>
        </div>
      </div>

      {/* 중요 주의사항 */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
        <div className="flex items-start gap-2">
          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-amber-900 mb-2">⚠️ 주의사항</h4>
            <ul className="space-y-2 text-sm text-amber-800">
              <li className="flex items-start gap-2">
                <span className="font-bold">•</span>
                <span>
                  <strong>누적 vs 당기:</strong> 분기/반기보고서는 <strong className="text-amber-900">누적금액</strong> 기준입니다. 
                  단일 분기 실적은 이전 분기를 차감해야 합니다.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="font-bold">•</span>
                <span>
                  <strong>사업보고서:</strong> 연간 실적이므로 <strong className="text-amber-900">당기금액</strong>을 사용합니다.
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="font-bold">•</span>
                <span>
                  <strong>데이터 제약:</strong> 감가상각비가 손익계산서에 별도 표시되지 않는 경우 
                  현금흐름표에서 추출합니다.
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* EBITDA 활용 */}
      <div className="mt-6">
        <h4 className="font-semibold text-gray-900 mb-3">활용 사례</h4>
        <div className="space-y-2 text-sm text-gray-700">
          <p>✓ 기업의 영업 현금 창출 능력 평가</p>
          <p>✓ 산업 간/국가 간 기업 비교 (회계 기준 차이 최소화)</p>
          <p>✓ M&A 기업 가치 평가 (EV/EBITDA 배수)</p>
          <p>✓ 부채 상환 능력 분석</p>
        </div>
      </div>

      {/* 보고서 코드 참고 */}
      <div className="mt-6 p-4 bg-white rounded-lg border border-gray-200">
        <h4 className="font-semibold text-gray-900 mb-2 text-sm">보고서 코드</h4>
        <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
          <div>11011: 사업보고서 (연간)</div>
          <div>11012: 반기보고서</div>
          <div>11013: 1분기보고서</div>
          <div>11014: 3분기보고서</div>
        </div>
      </div>

      {/* 데이터 출처 */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          데이터 출처: 금융감독원 전자공시시스템 (OPENDART)
        </p>
      </div>
    </div>
  );
}
