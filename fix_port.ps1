# 포트 8000을 사용하는 프로세스 종료 스크립트

Write-Host "포트 8000을 사용하는 프로세스 확인 중..." -ForegroundColor Yellow

$portInfo = netstat -ano | findstr :8000 | findstr LISTENING
if ($portInfo) {
    $processId = ($portInfo -split '\s+')[-1]
    Write-Host "프로세스 ID: $processId" -ForegroundColor Cyan
    
    try {
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "프로세스 종료 중: $($process.ProcessName) (PID: $processId)" -ForegroundColor Yellow
            Stop-Process -Id $processId -Force
            Write-Host "프로세스 종료 완료" -ForegroundColor Green
        } else {
            Write-Host "프로세스를 찾을 수 없습니다." -ForegroundColor Red
        }
    } catch {
        Write-Host "프로세스 종료 실패: $_" -ForegroundColor Red
    }
} else {
    Write-Host "포트 8000을 사용하는 프로세스가 없습니다." -ForegroundColor Green
}

Write-Host "`n서버를 시작하려면 다음 명령어를 실행하세요:" -ForegroundColor Cyan
Write-Host "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000" -ForegroundColor White
