'use client';

import { AlertTriangle, Info } from 'lucide-react';

interface WarningAlertsProps {
  warnings: string[];
}

export default function WarningAlerts({ warnings }: WarningAlertsProps) {
  if (!warnings || warnings.length === 0) {
    return null;
  }

  return (
    <div className="space-y-2">
      {warnings.map((warning, index) => {
        const isError = warning.includes('⚠️') || warning.includes('경고');
        const isInfo = warning.includes('ℹ️') || warning.includes('안내');

        return (
          <div
            key={index}
            className={`flex items-start gap-3 p-4 rounded-lg ${
              isError
                ? 'bg-yellow-50 border border-yellow-200'
                : 'bg-blue-50 border border-blue-200'
            }`}
          >
            {isError ? (
              <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
            ) : (
              <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
            )}
            <p
              className={`text-sm ${
                isError ? 'text-yellow-800' : 'text-blue-800'
              }`}
            >
              {warning}
            </p>
          </div>
        );
      })}
    </div>
  );
}
