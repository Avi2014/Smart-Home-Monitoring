# Smart Home IoT Monitoring System - Startup Script
# Starts all components in separate windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🏠 Smart Home IoT Monitoring System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    .\venv\Scripts\pip install -r requirements.txt
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting system components..." -ForegroundColor Cyan
Write-Host ""

# Start Dashboard
Write-Host "1️⃣  Starting Dashboard..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {
    Write-Host '📊 DASHBOARD' -ForegroundColor Cyan;
    Write-Host 'Loading Streamlit dashboard...' -ForegroundColor Yellow;
    cd '$PWD';
    .\venv\Scripts\Activate.ps1;
    streamlit run dashboard.py
}"

Start-Sleep -Seconds 2

# Start Alert System
Write-Host "2️⃣  Starting Alert System..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {
    Write-Host '🚨 ALERT SYSTEM' -ForegroundColor Red;
    Write-Host 'Starting alert monitoring...' -ForegroundColor Yellow;
    cd '$PWD';
    .\venv\Scripts\Activate.ps1;
    python alert_system.py
}"

Start-Sleep -Seconds 2

# Start Sensor Simulators
Write-Host "3️⃣  Starting Sensor Simulators..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {
    Write-Host '🔌 SENSOR SIMULATORS' -ForegroundColor Green;
    Write-Host 'Starting all sensors...' -ForegroundColor Yellow;
    cd '$PWD';
    .\venv\Scripts\Activate.ps1;
    python src\sensors\run_all_sensors.py
}"

Start-Sleep -Seconds 2

# Start Interactive Control (Optional)
Write-Host "4️⃣  Starting Interactive Control..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {
    Write-Host '🎮 INTERACTIVE CONTROL PANEL' -ForegroundColor Magenta;
    Write-Host 'Manual sensor control ready!' -ForegroundColor Yellow;
    Write-Host '';
    Write-Host 'Use this to manually trigger alarms:' -ForegroundColor Cyan;
    Write-Host '  - Press 5 for quick scenarios' -ForegroundColor White;
    Write-Host '  - Press 2 for high temperature alarm' -ForegroundColor White;
    Write-Host '  - Press 9 for emergency (all alarms!)' -ForegroundColor White;
    Write-Host '';
    cd '$PWD';
    .\venv\Scripts\Activate.ps1;
    python interactive_control.py
}"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ All components started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Dashboard:          http://localhost:8501" -ForegroundColor Cyan
Write-Host "🚨 Alert System:       Check terminal for alarms" -ForegroundColor Cyan
Write-Host "🔌 Sensors:            Running in background" -ForegroundColor Cyan
Write-Host "🎮 Control Panel:      Use menu to trigger alarms" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Tip: Use Interactive Control (Press 5 → 2) to trigger alarms!" -ForegroundColor Yellow
Write-Host ""
Write-Host "⏸️  Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
