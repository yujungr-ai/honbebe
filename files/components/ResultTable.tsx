'use client';

import { EBITDAResponse } from '@/types';
import { formatAmount, formatDate, calculatePercentage } from '../lib/utils';
import { Building2, Calendar, FileText, Database } from 'lucide-react';

interface ResultTableProps {
  data: EBITDAResponse;
}

export default function ResultTable({ data }: ResultTableProps) {
  const { company, period, components, ebitda, source } = data;

  // EBITDA 대비 각 구성요소 비율 계산
  const opIncomePercent = calculatePercentage(
    components.operating_income.amount,
    ebitda.total
  );
  const depPercent = calculatePercentage(
    components.depreciation.amount,
    ebitda.total
  );
  const amortPercent = calculatePercentage(
    components.amortization.amount,
    ebitda.total
  );

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      {/* 헤더 정보 */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6">
        <div className="flex items-center gap-3 mb-4">
          <Building2 className="w-8 h-8" />
          <div>
            <h2 className="text-2xl font-bold">{company.corp_name}</h2>
            <p className="text-primary-100 text-sm">
              {company.stock_code && `종목코드: ${company.stock_code} | `}
              고유번호: {company.corp_code}
            </p>
          </div>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            <span>{period.year}년 {period.report_name}</span>
          </div>
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            <span>{period.fs_name}</span>
          </div>
          <div className="flex items-center gap-2">
            <Database className="w-4 h-4" />
            <span>{source.cached ? '캐시 데이터' : '실시간 조회'}</span>
          </div>
          {source.rcept_no && (
            <div className="text-xs">
              접수번호: {source.rcept_no}
            </div>
          )}
        </div>
      </div>

      {/* EBITDA 요약 */}
      <div className="bg-primary-50 p-6 border-b">
        <div className="text-center">
          <p className="text-sm text-gray-600 mb-2">총 EBITDA</p>
          <p className="text-4xl font-bold text-primary-700">
            {formatAmount(ebitda.total)}
          </p>
          <p className="text-xs text-gray-500 mt-2">
            계산 기준: {ebitda.basis}
          </p>
        </div>
      </div>

      {/* 구성요소 테이블 */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                항목
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                금액 (억원)
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                비율
              </th>
              <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                상태
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {/* 영업이익 */}
            <tr className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                  <span className="text-sm font-medium text-gray-900">
                    {components.operating_income.label}
                  </span>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900 font-semibold">
                {formatAmount(components.operating_income.amount)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-500">
                {opIncomePercent}%
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-center">
                <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                  정상
                </span>
              </td>
            </tr>

            {/* 감가상각비 */}
            <tr className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-sm font-medium text-gray-900">
                    {components.depreciation.label}
                  </span>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                {formatAmount(components.depreciation.amount)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-500">
                {depPercent}%
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-center">
                <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                  정상
                </span>
              </td>
            </tr>

            {/* 무형자산상각비 */}
            <tr className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
                  <span className="text-sm font-medium text-gray-900">
                    {components.amortization.label}
                  </span>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                {formatAmount(components.amortization.amount)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-500">
                {amortPercent}%
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-center">
                <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                  정상
                </span>
              </td>
            </tr>

            {/* 합계 */}
            <tr className="bg-primary-50 font-semibold">
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                총 EBITDA
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-primary-700">
                {formatAmount(ebitda.total)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                100%
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-center">
                <span className="px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded">
                  합계
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* 푸터 정보 */}
      <div className="bg-gray-50 px-6 py-4 text-xs text-gray-600">
        <p>조회 시각: {formatDate(source.fetched_at)}</p>
      </div>
    </div>
  );
}
