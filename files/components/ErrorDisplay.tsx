'use client';

import { AlertCircle, RefreshCw, X } from 'lucide-react';

interface ErrorDisplayProps {
  error: string;
  onRetry?: () => void;
  onReset?: () => void;
}

export default function ErrorDisplay({
  error,
  onRetry,
  onReset,
}: ErrorDisplayProps) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-red-900 mb-2">오류 발생</h3>
          <p className="text-red-800 mb-4">{error}</p>
          <div className="flex gap-3">
            {onRetry && (
              <button
                onClick={onRetry}
                className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                다시 시도
              </button>
            )}
            {onReset && (
              <button
                onClick={onReset}
                className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
              >
                <X className="w-4 h-4" />
                초기화
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
