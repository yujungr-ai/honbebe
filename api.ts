import axios, { AxiosError } from 'axios';
import { EBITDAResponse, APIError, SearchFormData } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 에러 메시지 추출
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<APIError>;
    
    if (axiosError.response?.data) {
      const data = axiosError.response.data;
      return data.message || data.detail || '알 수 없는 에러가 발생했습니다.';
    }
    
    if (axiosError.code === 'ECONNABORTED') {
      return '요청 시간이 초과되었습니다. 다시 시도해주세요.';
    }
    
    if (axiosError.code === 'ERR_NETWORK') {
      return 'API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.';
    }
    
    return axiosError.message;
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return '알 수 없는 에러가 발생했습니다.';
}

// EBITDA 조회 API
export async function fetchEBITDA(params: SearchFormData): Promise<EBITDAResponse> {
  const response = await apiClient.get<EBITDAResponse>('/api/v1/ebitda', {
    params: {
      company: params.company,
      year: params.year,
      report_code: params.report_code,
      fs_div: params.fs_div,
    },
  });
  
  return response.data;
}

// 헬스 체크 API
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await apiClient.get('/api/v1/health');
    return response.data.status === 'ok';
  } catch {
    return false;
  }
}

// 여러 연도 데이터 조회 (시계열)
export async function fetchEBITDATimeSeries(
  company: string,
  years: number[],
  reportCode: string,
  fsDiv: string
): Promise<EBITDAResponse[]> {
  const promises = years.map(year =>
    fetchEBITDA({ company, year, report_code: reportCode, fs_div: fsDiv })
  );
  
  // 병렬 요청 (실패한 것은 필터링)
  const results = await Promise.allSettled(promises);
  
  return results
    .filter((result): result is PromiseFulfilledResult<EBITDAResponse> => 
      result.status === 'fulfilled'
    )
    .map(result => result.value);
}
