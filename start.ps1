# Smart Home IoT Monitoring System - All-in-One Launcher
# Run this script to start the entire system: .\start.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Smart Home IoT Monitoring System" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "[OK] Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "[WARN] Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
    Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
    .\venv\Scripts\pip install -r requirements.txt
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting system components..." -ForegroundColor Cyan
Write-Host ""

# Get current directory
$currentDir = Get-Location

# Start Dashboard
Write-Host "[1/4] Starting Dashboard..." -ForegroundColor Yellow
$dashboardScript = "Set-Location '$currentDir'; & .\venv\Scripts\Activate.ps1; Write-Host 'DASHBOARD - Loading Streamlit...' -ForegroundColor Cyan; streamlit run dashboard.py"
Start-Process powershell -ArgumentList "-NoExit","-Command",$dashboardScript
Start-Sleep -Seconds 2

# Start Alert System
Write-Host "[2/4] Starting Alert System..." -ForegroundColor Yellow
$alertScript = "Set-Location '$currentDir'; & .\venv\Scripts\Activate.ps1; Write-Host 'ALERT SYSTEM - Monitoring thresholds...' -ForegroundColor Red; python alert_system.py"
Start-Process powershell -ArgumentList "-NoExit","-Command",$alertScript
Start-Sleep -Seconds 2

# Start Sensor Simulators
Write-Host "[3/4] Starting Sensor Simulators..." -ForegroundColor Yellow
$sensorScript = "Set-Location '$currentDir'; & .\venv\Scripts\Activate.ps1; Write-Host 'SENSORS - Starting all 4 sensors...' -ForegroundColor Green; python src\sensors\run_all_sensors.py"
Start-Process powershell -ArgumentList "-NoExit","-Command",$sensorScript
Start-Sleep -Seconds 2

# Start Interactive Control
Write-Host "[4/4] Starting Interactive Control..." -ForegroundColor Yellow
$controlScript = "Set-Location '$currentDir'; & .\venv\Scripts\Activate.ps1; Write-Host 'INTERACTIVE CONTROL - Manual sensor control ready!' -ForegroundColor Magenta; Write-Host 'Tip: Press 5 for quick scenarios, 2 for high temp, 9 for emergency' -ForegroundColor Cyan; python interactive_control.py"
Start-Process powershell -ArgumentList "-NoExit","-Command",$controlScript

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[OK] All components started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dashboard:      http://localhost:8501" -ForegroundColor Cyan
Write-Host "Alert System:   Check terminal for alarms" -ForegroundColor Cyan
Write-Host "Sensors:        Running in background" -ForegroundColor Cyan
Write-Host "Control Panel:  Use menu to trigger alarms" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tip: Use Interactive Control (Press 5 then 2) to trigger alarms!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
