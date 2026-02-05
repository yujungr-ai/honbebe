// API 응답 타입 정의
export interface CompanyInfo {
  corp_code: string;
  corp_name: string;
  stock_code?: string;
}

export interface PeriodInfo {
  year: number;
  report_code: string;
  report_name: string;
  fs_div: string;
  fs_name: string;
}

export interface ComponentAmount {
  label: string;
  amount: number;
  currency: string;
}

export interface EBITDAComponents {
  operating_income: ComponentAmount;
  depreciation: ComponentAmount;
  amortization: ComponentAmount;
}

export interface EBITDAResult {
  total: number;
  currency: string;
  basis: string;
}

export interface SourceInfo {
  rcept_no?: string;
  fetched_at: string;
  cached: boolean;
}

export interface EBITDAResponse {
  company: CompanyInfo;
  period: PeriodInfo;
  components: EBITDAComponents;
  ebitda: EBITDAResult;
  source: SourceInfo;
  warnings: string[];
}

export interface APIError {
  error: string;
  message: string;
  detail?: string;
}

// 폼 입력 타입
export interface SearchFormData {
  company: string;
  year: number;
  report_code: string;
  fs_div: string;
}

// 차트 데이터 타입
export interface ChartDataPoint {
  year: number;
  report_name: string;
  ebitda: number;
  operating_income: number;
}

// 보고서 코드 옵션
export const REPORT_CODES = {
  '11011': '사업보고서 (연간)',
  '11012': '반기보고서',
  '11013': '1분기보고서',
  '11014': '3분기보고서',
} as const;

export const FS_DIV = {
  'CFS': '연결재무제표',
  'OFS': '개별재무제표',
} as const;

export type ReportCode = keyof typeof REPORT_CODES;
export type FsDiv = keyof typeof FS_DIV;
