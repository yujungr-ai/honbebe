import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'EBITDA Calculator - OPENDART 기반 기업 분석',
  description: 'OPENDART API를 활용한 기업 EBITDA 계산 및 분석 도구',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
