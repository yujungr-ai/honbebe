/**
 * 금액 포맷팅 (억원 단위)
 */
export function formatAmount(amount: number): string {
  if (amount === 0) return '0원';
  
  const 억 = amount / 100000000;
  const 조 = 억 / 10000;
  
  if (조 >= 1) {
    return `${조.toFixed(2)}조원`;
  } else if (억 >= 1) {
    return `${억.toFixed(2)}억원`;
  } else {
    return `${amount.toLocaleString()}원`;
  }
}

/**
 * 차트용 금액 포맷팅
 */
export function formatChartAmount(value: number): string {
  if (value === 0) return '0';
  
  const 억 = value / 100;
  const 조 = 억 / 10000;
  
  if (조 >= 1) {
    return `${조.toFixed(1)}조`;
  } else if (억 >= 1) {
    return `${억.toFixed(1)}억`;
  } else {
    return `${value.toLocaleString()}`;
  }
}

/**
 * 날짜 포맷팅
 */
export function formatDate(dateString: string): string {
  try {
    const date = new Date(dateString);
    return date.toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateString;
  }
}

/**
 * 퍼센트 계산
 */
export function calculatePercentage(part: number, total: number): number {
  if (total === 0) return 0;
  return (part / total) * 100;
}

/**
 * 최근 N년 배열 생성
 */
export function getRecentYears(count: number): number[] {
  const currentYear = new Date().getFullYear();
  return Array.from({ length: count }, (_, i) => currentYear - i).reverse();
}
