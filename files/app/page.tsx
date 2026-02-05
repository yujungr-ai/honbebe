'use client';

import { useState } from 'react';
import { BarChart3 } from 'lucide-react';
import SearchForm from '@/components/SearchForm';
import ResultTable from '@/components/ResultTable';
import TimeSeriesChart from '@/components/TimeSeriesChart';
import EBITDAInfoPanel from '@/components/EBITDAInfoPanel';
import WarningAlerts from '@/components/WarningAlerts';
import ErrorDisplay from '@/components/ErrorDisplay';
import EmptyState from '@/components/EmptyState';
import { fetchEBITDA, getErrorMessage } from '@/lib/api';
import { EBITDAResponse, SearchFormData } from '@/types';

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState<EBITDAResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [searchParams, setSearchParams] = useState<SearchFormData | null>(null);

  const handleSearch = async (formData: SearchFormData) => {
    setIsLoading(true);
    setError(null);
    setData(null);
    setSearchParams(formData);

    try {
      const result = await fetchEBITDA(formData);
      setData(result);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setData(null);
    setError(null);
    setSearchParams(null);
  };

  const handleRetry = () => {
    if (searchParams) {
      handleSearch(searchParams);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* 헤더 */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                EBITDA Calculator
              </h1>
              <p className="text-sm text-gray-600">
                OPENDART 기반 기업 EBITDA 분석 도구
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* 메인 컨텐츠 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 왼쪽: 검색 & 결과 (2/3) */}
          <div className="lg:col-span-2 space-y-6">
            {/* 검색 폼 */}
            <SearchForm onSubmit={handleSearch} isLoading={isLoading} />

            {/* 에러 표시 */}
            {error && (
              <ErrorDisplay 
                error={error} 
                onRetry={handleRetry}
                onReset={handleReset}
              />
            )}

            {/* 로딩 상태 */}
            {isLoading && (
              <div className="bg-white rounded-lg shadow-md p-12">
                <div className="flex flex-col items-center justify-center gap-4">
                  <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
                  <p className="text-gray-600 font-medium">EBITDA 계산 중...</p>
                  <p className="text-sm text-gray-500">데이터를 불러오고 있습니다.</p>
                </div>
              </div>
            )}

            {/* 결과 표시 */}
            {!isLoading && !error && data && (
              <>
                {/* 경고 메시지 */}
                <WarningAlerts warnings={data.warnings} />

                {/* 결과 테이블 */}
                <ResultTable data={data} />

                {/* 시계열 차트 */}
                {searchParams && (
                  <TimeSeriesChart 
                    latestData={data} 
                    searchParams={searchParams}
                  />
                )}
              </>
            )}

            {/* 빈 상태 */}
            {!isLoading && !error && !data && (
              <EmptyState />
            )}
          </div>

          {/* 오른쪽: EBITDA 정보 패널 (1/3) */}
          <div className="lg:col-span-1">
            <EBITDAInfoPanel />
          </div>
        </div>
      </main>

      {/* 푸터 */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p className="mb-2">
              데이터 출처: 금융감독원 전자공시시스템 (OPENDART)
            </p>
            <p className="text-xs text-gray-500">
              © 2024 EBITDA Calculator. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
