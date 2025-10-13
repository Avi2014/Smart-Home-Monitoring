# 🚀 QUICK START SCRIPT
# Run this to start your IoT Dashboard

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  🏠 IoT Smart Home Dashboard - Quick Start" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if in virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment is active" -ForegroundColor Green
} else {
    Write-Host "⚠️  Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

Write-Host ""
Write-Host "📋 What will happen:" -ForegroundColor Yellow
Write-Host "   1. Dashboard will open in your browser" -ForegroundColor White
Write-Host "   2. Open new terminals to run sensors" -ForegroundColor White
Write-Host "   3. Data will appear in real-time" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Dashboard URL: http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "📊 To run sensors, open NEW terminals and run:" -ForegroundColor Yellow
Write-Host "   Terminal 2: python sensors\temperature_sensor.py" -ForegroundColor White
Write-Host "   Terminal 3: python sensors\humidity_sensor.py" -ForegroundColor White
Write-Host "   Terminal 4: python sensors\co2_sensor.py" -ForegroundColor White
Write-Host "   Terminal 5: python sensors\light_sensor.py" -ForegroundColor White
Write-Host ""
Write-Host "   OR run all at once:" -ForegroundColor White
Write-Host "   Terminal 2: python sensors\run_all_sensors.py" -ForegroundColor White
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan

Read-Host "Press Enter to start the dashboard"

Write-Host ""
Write-Host "🚀 Starting dashboard..." -ForegroundColor Green
Write-Host ""

streamlit run dashboard.py
