# ✅ Startup Script Fixed!

## Issue Resolved

The `start_all.ps1` script had PowerShell syntax errors:
1. **Ampersand (&) character issues** - Not properly escaped in command strings
2. **Unicode character encoding problems** - Emojis causing parser errors
3. **String termination issues** - Malformed multi-line command blocks

## Solution

Recreated the script with:
- ✅ Proper PowerShell variable syntax for command strings
- ✅ Simple ASCII text instead of Unicode emojis
- ✅ Correct `-ArgumentList` parameter formatting
- ✅ Clean string handling without special characters

## How to Use

### One-Click Startup
```powershell
.\scripts\start_all.ps1
```

This will launch **4 terminal windows**:
1. **Dashboard** - Streamlit web interface (http://localhost:8501)
2. **Alert System** - Threshold monitoring with audio beeps
3. **Sensors** - All 4 sensor simulators running
4. **Interactive Control** - Manual testing panel

### What Happens
```
========================================
Smart Home IoT Monitoring System
========================================

[OK] Virtual environment found

Starting system components...

[1/4] Starting Dashboard...
[2/4] Starting Alert System...
[3/4] Starting Sensor Simulators...
[4/4] Starting Interactive Control...

========================================
[OK] All components started!
========================================

Dashboard:      http://localhost:8501
Alert System:   Check terminal for alarms
Sensors:        Running in background
Control Panel:  Use menu to trigger alarms

Tip: Use Interactive Control (Press 5 then 2) to trigger alarms!
```

## Alternative: Manual Startup

If you prefer to start components individually:

```powershell
# Terminal 1: Dashboard
streamlit run dashboard.py

# Terminal 2: Alert System  
python alert_system.py

# Terminal 3: Sensors
python src\sensors\run_all_sensors.py

# Terminal 4: Interactive Control (Optional)
python interactive_control.py
```

## Testing the System

After starting, test the alert system:

1. **Open Interactive Control terminal** (4th window)
2. **Press 5** for quick scenarios menu
3. **Press 2** for high temperature alarm
4. **Listen for beep** sound from Alert System terminal
5. **Check Dashboard** - see the high temperature value

## Troubleshooting

### Script won't run
```powershell
# Check execution policy
Get-ExecutionPolicy

# If Restricted, change it:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Virtual environment not found
The script will automatically:
1. Create the virtual environment
2. Install all dependencies from requirements.txt

### Port already in use (Streamlit)
```powershell
# Kill existing Streamlit process
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"} | Stop-Process -Force

# Or use different port
streamlit run dashboard.py --server.port 8502
```

### Sensors not connecting
- Check internet connection (test.mosquitto.org requires internet)
- Wait 10-15 seconds for MQTT connection to establish
- Check sensor terminal for connection messages

## What's Next?

Your system is now fully operational! You can:
- 📊 View real-time data on the dashboard
- 🚨 Test alert system with interactive control
- 📈 Run performance metrics tests
- 🚀 Deploy to cloud (see docs/DEPLOYMENT.md)

---

**Status**: ✅ All Fixed and Working!
**Date**: October 13, 2025
**Script Location**: `scripts/start_all.ps1`
