# 🚀 Quick Start Guide - One Simple Command

## One-Command Launch 🎯

Just run this **ONE** command to start the entire IoT monitoring system:

```powershell
.\start.ps1
```

**That's it!** Everything launches automatically.

---

## What Happens When You Run It? 🏃‍♂️

The single command automatically launches **4 components** in separate windows:

1. **📊 Dashboard** → http://localhost:8501
   - Real-time sensor visualization
   - Interactive charts and gauges
   - Alert status monitoring

2. **🔔 Alert System** → Terminal window
   - Monitors sensor thresholds
   - Triggers audio beeps on violations
   - Logs all alerts

3. **📡 Sensors (4 simulators)** → Terminal window
   - Temperature sensor (every 3s)
   - Humidity sensor (every 3s)
   - CO2 sensor (every 5s)
   - Light sensor (every 4s)

4. **🎮 Interactive Control** → Terminal window
   - Manual sensor control
   - Test scenarios
   - Emergency simulations

---

## First Time Setup (One-Time Only) ⚙️

Before running for the first time, ensure you have:

### 1. Python Installed:
```powershell
python --version
# Should show Python 3.8 or higher
```

### 2. MQTT Credentials in `.env` file:
Create a `.env` file with:
```env
MQTT_BROKER=95c2f02d61404267847ebc19552f72b0.s1.eu.hivemq.cloud
MQTT_PORT=8883
MQTT_USERNAME=ar153
MQTT_PASSWORD=ARhive@25
MQTT_USE_TLS=true
```

**Note**: The `start.ps1` script will automatically:
- Create virtual environment if missing
- Install all dependencies
- Set up everything for you

---

## Stopping the System 🛑

To stop all components:

1. Close each terminal window (4 windows total)
2. Or press `Ctrl+C` in each terminal

---

## Individual Component Commands 🔧

If you want to run components separately:

### Just Dashboard:
```powershell
.\venv\Scripts\Activate.ps1
streamlit run dashboard.py
```

### Just Sensors:
```powershell
.\venv\Scripts\Activate.ps1
python src/sensors/run_all_sensors.py
```

### Just Alert System:
```powershell
.\venv\Scripts\Activate.ps1
python alert_system.py
```

### Just Interactive Control:
```powershell
.\venv\Scripts\Activate.ps1
python interactive_control.py
```

---

## Testing Commands 🧪

### Verify System:
```powershell
python verify_system.py
```

### Test MQTT Connection:
```powershell
.\venv\Scripts\Activate.ps1
python mqtt_connection_test.py
```

### Run Single Sensor:
```powershell
.\venv\Scripts\Activate.ps1
python src/sensors/temperature_sensor.py
```

---

## Quick Scenarios 🎭

### Trigger Temperature Alert:
1. Run: `python interactive_control.py`
2. Press `2` → Sets temperature to 30°C (above 28°C threshold)
3. Alert system will beep! 🔔

### Trigger Multiple Alerts:
1. Run: `python interactive_control.py`
2. Press `5` (Quick Scenarios)
3. Press `6` (Multiple Alerts)
4. Multiple beeps! 🔔🔔🔔

### Emergency Simulation:
1. Run: `python interactive_control.py`
2. Press `5` (Quick Scenarios)
3. Press `9` (Emergency - All Alerts)
4. Continuous beeps! 🚨🔔🚨

---

## Access Points 🌐

After running the start command:

| Component | URL/Location |
|-----------|--------------|
| Dashboard | http://localhost:8501 |
| Alternative Dashboard | http://localhost:8502 |
| Sensors | Check "Sensors" terminal window |
| Alerts | Check "Alert System" terminal window |
| Control | Check "Interactive Control" terminal window |

---

## Troubleshooting 🔧

### "start.ps1 cannot be loaded" Error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use:
- Close other instances of Streamlit
- Check dashboard URL (might be on port 8502 instead of 8501)

### Sensors Not Connecting:
- Check `.env` file exists
- Verify MQTT credentials are correct
- Check internet connection

### No Data on Dashboard:
- Ensure sensors window shows "✅ Temperature: XX°C | Messages: XX"
- Check dashboard shows "✅ Connected" (green)
- Verify auto-refresh is enabled

---

## File Structure 📁

**Simplified structure - just ONE launcher file!**

```
iot/
├── start.ps1           ← Run this! (All-in-one launcher)
├── dashboard.py
├── alert_system.py
├── interactive_control.py
├── .env                ← Your MQTT credentials
└── src/sensors/
    └── ...
```

---

## Pro Tips 💡

1. **Always use the start script** - It handles everything automatically
2. **Dashboard loads at http://localhost:8501** - Open in browser after ~10 seconds
3. **Watch the sensor terminal** - Shows live data: "Messages: 50, 51, 52..."
4. **Use Interactive Control** to test the alert system quickly
5. **Sensors run infinitely** - They won't stop until you close the window

---

## 📝 Summary

**Single Command:**
```powershell
.\start.ps1
```

**What You Get:**
- ✅ Dashboard running at http://localhost:8501
- ✅ Alert system monitoring
- ✅ 4 sensors publishing data continuously
- ✅ Interactive control ready
- ✅ Everything connected via MQTT
- ✅ TLS/SSL encryption enabled
- ✅ Auto-installs dependencies if needed

**Just ONE file to rule them all!** 🎉

**Access:**
- Open browser → http://localhost:8501
- Watch the magic happen! 🎉

---

**That's it! Enjoy your Smart Home IoT Monitoring System! 🏠📊🔔**
