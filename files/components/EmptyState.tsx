'use client';

import { Search, BarChart3 } from 'lucide-react';

export default function EmptyState() {
  return (
    <div className="bg-white rounded-lg shadow-md p-12">
      <div className="flex flex-col items-center justify-center gap-4 text-center">
        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
          <BarChart3 className="w-8 h-8 text-gray-400" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            EBITDA 계산 시작하기
          </h3>
          <p className="text-gray-600 mb-4">
            회사명 또는 종목코드를 입력하고 검색 버튼을 클릭하세요.
          </p>
          <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
            <Search className="w-4 h-4" />
            <span>예: 삼성전자, 005930</span>
          </div>
        </div>
      </div>
    </div>
  );
}
