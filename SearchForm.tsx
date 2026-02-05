'use client';

import { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';
import { SearchFormData, REPORT_CODES, FS_DIV } from '@/types';

interface SearchFormProps {
  onSubmit: (data: SearchFormData) => void;
  isLoading: boolean;
}

export default function SearchForm({ onSubmit, isLoading }: SearchFormProps) {
  const currentYear = new Date().getFullYear();
  
  const [formData, setFormData] = useState<SearchFormData>({
    company: '',
    year: currentYear,
    report_code: '11011',
    fs_div: 'CFS',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.company.trim()) {
      alert('회사명 또는 종목코드를 입력해주세요.');
      return;
    }
    
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* 회사명/종목코드 입력 */}
        <div className="lg:col-span-2">
          <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
            회사명 또는 종목코드
          </label>
          <input
            type="text"
            id="company"
            value={formData.company}
            onChange={(e) => setFormData({ ...formData, company: e.target.value })}
            placeholder="예: 삼성전자, 005930"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
            disabled={isLoading}
          />
          <p className="mt-1 text-xs text-gray-500">
            회사명 또는 6자리 종목코드를 입력하세요
          </p>
        </div>

        {/* 사업연도 선택 */}
        <div>
          <label htmlFor="year" className="block text-sm font-medium text-gray-700 mb-2">
            사업연도
          </label>
          <select
            id="year"
            value={formData.year}
            onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
            disabled={isLoading}
          >
            {Array.from({ length: 10 }, (_, i) => currentYear - i).map((year) => (
              <option key={year} value={year}>
                {year}년
              </option>
            ))}
          </select>
        </div>

        {/* 보고서 코드 선택 */}
        <div>
          <label htmlFor="report_code" className="block text-sm font-medium text-gray-700 mb-2">
            보고서 유형
          </label>
          <select
            id="report_code"
            value={formData.report_code}
            onChange={(e) => setFormData({ ...formData, report_code: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
            disabled={isLoading}
          >
            {Object.entries(REPORT_CODES).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        {/* 재무제표 구분 선택 */}
        <div>
          <label htmlFor="fs_div" className="block text-sm font-medium text-gray-700 mb-2">
            재무제표 구분
          </label>
          <select
            id="fs_div"
            value={formData.fs_div}
            onChange={(e) => setFormData({ ...formData, fs_div: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
            disabled={isLoading}
          >
            {Object.entries(FS_DIV).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </div>

        {/* 검색 버튼 */}
        <div className="flex items-end">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:ring-4 focus:ring-primary-300 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-200 flex items-center justify-center gap-2 font-medium"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                조회 중...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                EBITDA 조회
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
}
