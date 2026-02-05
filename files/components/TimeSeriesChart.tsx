'use client';

import { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Loader2 } from 'lucide-react';
import { fetchEBITDATimeSeries, getErrorMessage } from '../lib/api';
import { SearchFormData, EBITDAResponse } from '../types';
import { formatChartAmount, getRecentYears } from '../lib/utils';

interface TimeSeriesChartProps {
  latestData: EBITDAResponse;
  searchParams: SearchFormData;
}

interface ChartData {
  year: number;
  ebitda: number;
  operating_income: number;
  depreciation: number;
  amortization: number;
}

export default function TimeSeriesChart({ latestData, searchParams }: TimeSeriesChartProps) {
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [chartType, setChartType] = useState<'line' | 'bar'>('line');

  useEffect(() => {
    loadTimeSeriesData();
  }, [latestData]);

  const loadTimeSeriesData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // 최근 5년 데이터 조회
      const years = getRecentYears(5);
      const responses = await fetchEBITDATimeSeries(
        searchParams.company,
        years,
        searchParams.report_code,
        searchParams.fs_div
      );

      // 차트 데이터 변환
      const data: ChartData[] = responses.map(response => ({
        year: response.period.year,
        ebitda: response.ebitda.total / 100000000, // 억원 단위
        operating_income: response.components.operating_income.amount / 100000000,
        depreciation: response.components.depreciation.amount / 100000000,
        amortization: response.components.amortization.amount / 100000000,
      })).sort((a, b) => a.year - b.year);

      setChartData(data);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  // 커스텀 툴팁
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-900 mb-2">{label}년</p>
          {payload.map((entry: any, index: number) => (
            <div key={index} className="flex items-center gap-2 text-sm">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: entry.color }}
              />
              <span className="text-gray-600">{entry.name}:</span>
              <span className="font-medium text-gray-900">
                {formatChartAmount(entry.value * 100000000)}
              </span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-12">
        <div className="flex flex-col items-center justify-center gap-4">
          <Loader2 className="w-12 h-12 text-primary-600 animate-spin" />
          <p className="text-gray-600">시계열 데이터를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-sm text-yellow-800">
            ⚠️ 시계열 데이터 조회 중 일부 오류가 발생했습니다: {error}
          </p>
        </div>
      </div>
    );
  }

  if (chartData.length === 0) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <TrendingUp className="w-6 h-6 text-primary-600" />
          <h3 className="text-xl font-bold text-gray-900">
            EBITDA 시계열 분석
          </h3>
        </div>
        
        {/* 차트 타입 선택 */}
        <div className="flex gap-2">
          <button
            onClick={() => setChartType('line')}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              chartType === 'line'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            라인 차트
          </button>
          <button
            onClick={() => setChartType('bar')}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              chartType === 'bar'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            막대 차트
          </button>
        </div>
      </div>

      {/* 차트 */}
      <ResponsiveContainer width="100%" height={400}>
        {chartType === 'line' ? (
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="year" 
              stroke="#6b7280"
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              stroke="#6b7280"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => formatChartAmount(value * 100000000)}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ fontSize: '14px' }}
              formatter={(value) => {
                const labels: Record<string, string> = {
                  ebitda: 'EBITDA',
                  operating_income: '영업이익',
                  depreciation: '감가상각비',
                  amortization: '무형자산상각비',
                };
                return labels[value] || value;
              }}
            />
            <Line 
              type="monotone" 
              dataKey="ebitda" 
              stroke="#2563eb" 
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
            />
            <Line 
              type="monotone" 
              dataKey="operating_income" 
              stroke="#3b82f6" 
              strokeWidth={2}
              strokeDasharray="5 5"
            />
            <Line 
              type="monotone" 
              dataKey="depreciation" 
              stroke="#10b981" 
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey="amortization" 
              stroke="#8b5cf6" 
              strokeWidth={2}
            />
          </LineChart>
        ) : (
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="year" 
              stroke="#6b7280"
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              stroke="#6b7280"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => formatChartAmount(value * 100000000)}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ fontSize: '14px' }}
              formatter={(value) => {
                const labels: Record<string, string> = {
                  ebitda: 'EBITDA',
                  operating_income: '영업이익',
                  depreciation: '감가상각비',
                  amortization: '무형자산상각비',
                };
                return labels[value] || value;
              }}
            />
            <Bar dataKey="ebitda" fill="#2563eb" />
            <Bar dataKey="operating_income" fill="#3b82f6" />
            <Bar dataKey="depreciation" fill="#10b981" />
            <Bar dataKey="amortization" fill="#8b5cf6" />
          </BarChart>
        )}
      </ResponsiveContainer>

      {/* 설명 */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">
          <strong>참고:</strong> 차트는 최근 5년간의 데이터를 표시합니다. 
          데이터가 없는 연도는 자동으로 제외됩니다.
        </p>
      </div>
    </div>
  );
}
