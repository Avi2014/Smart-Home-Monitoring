# 🏠 Smart Home Monitoring System

**Monitor Temperature, Humidity, CO2, and Light in real-time with automatic alerts!**

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Easy](https://img.shields.io/badge/Setup-3_Steps-green) ![Status](https://img.shields.io/badge/Status-Working-success)

---

## ⚡ Quick Start (3 Simple Steps!)

### Step 1: Download
```powershell
git clone https://github.com/Avi2014/Smart-Home-Monitoring.git
cd Smart-Home-Monitoring
```

### Step 2: Install (First Time Only)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**If activation fails:** Run this first, then try again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Step 3: Run
```powershell
.\start.ps1
```

✅ **Done!** Your browser will open automatically showing the dashboard.

---

## 📺 What You'll See

After running, **4 windows** will open:

| Window | What It Shows |
|--------|---------------|
| **1. Dashboard (Browser)** | Beautiful web page with live charts at http://localhost:8501 |
| **2. Alert System** | Beeps when sensors go above/below safe limits |
| **3. Sensors** | 4 sensors sending data every 3 seconds |
| **4. Control Panel** | Menu to test alarms manually |

---

## 🎯 What It Does

This is a fake smart home with 4 sensors:

| Sensor | What It Measures | Safe Range | If Unsafe |
|--------|-----------------|------------|-----------|
| 🌡️ **Temperature** | Room temperature | 20-28°C | Beeps + Red warning |
| 💧 **Humidity** | Moisture in air | 40-60% | Beeps + Red warning |
| 🌫️ **CO2** | Air quality | 400-1000 ppm | Beeps + Red warning |
| 💡 **Light** | Brightness | 200-800 lux | Beeps + Red warning |

**The sensors aren't real** - they're simulated (fake) and generate random data for testing!

---

## 🎮 How to Test It

### Test 1: See Live Data
1. Open your browser to http://localhost:8501
2. Watch the numbers change every 3 seconds
3. See the line charts moving

### Test 2: Trigger an Alarm
1. Go to **Control Panel** window (Window 4)
2. Press `5` (Quick Test Scenarios)
3. Press `2` (High Temperature - 35°C)
4. You'll hear a **beep** and see **red warning** on dashboard!

### Test 3: Clear the Alarm
1. In Control Panel, press `5` again
2. Press `1` (Normal conditions)
3. Alarm clears, everything back to green ✅

---

## 🛑 How to Stop

**Easy ways to stop:**
1. Close all the terminal windows, OR
2. Press `Ctrl+C` in each window

**Nuclear option** (kills all Python processes):
```powershell
taskkill /F /IM python.exe
```

---

## 🔧 Troubleshooting

### "Python not found"
**Solution:** Install Python from https://python.org/downloads
- ✅ Check "Add Python to PATH" during installation

### "Cannot activate venv"
**Solution:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv\Scripts\Activate.ps1
```

### "Module not found"
**Solution:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "No data on dashboard"
**Solution:** Wait 10-15 seconds. Sensors need time to connect!

### "Port 8501 already in use"
**Solution:** Close other programs using that port, or restart your computer.

---

## ⚙️ Want to Change Settings?

### Change how often sensors send data
**Default:** Every 3 seconds

**To change:** Edit `src/sensors/sensor_config.json`
```json
"sampling_rate": 1  // Change 3 to 1 for faster, or 10 for slower
```

### Change when alarms trigger
**Edit:** `alert_system.py` (around line 30)
```python
self.thresholds = {
    'temperature': (20, 28),  # Change these numbers!
    'humidity': (40, 60),
    'co2': (400, 1000),
    'light': (200, 800)
}
```

---

## 📁 Project Files (Simple Explanation)

```
Smart-Home-Monitoring/
│
├── start.ps1              ← 👈 RUN THIS FILE!
│
├── dashboard.py           ← Makes the web page
├── alert_system.py        ← Makes beep sounds
├── interactive_control.py ← Test menu
│
├── src/sensors/           ← Fake sensors (4 files)
│   ├── temperature_sensor.py
│   ├── humidity_sensor.py
│   ├── co2_sensor.py
│   └── light_sensor.py
│
├── requirements.txt       ← List of software needed
├── .env                   ← Private settings (auto-created)
└── README.md             ← This file!
```

**You only need to run `start.ps1` - everything else is automatic!**

---

## 🎓 For Your Lab Report

This project shows:
- ✅ IoT sensor simulation
- ✅ Real-time data visualization
- ✅ MQTT messaging (cloud communication)
- ✅ Alert system with thresholds
- ✅ Web dashboard (Streamlit + Plotly)

**Take screenshots of:**
1. Dashboard with all 4 sensors showing data
2. Triggered alarms (red warnings)
3. Control panel testing menu
4. Terminal showing sensor messages

---

## 💡 Tips for Your Friends

### First Time Running?
1. Make sure you have **Python 3.13** installed
2. Run all 3 setup steps (above)
3. Wait 10-15 seconds after `start.ps1` for sensors to connect
4. Open http://localhost:8501 in your browser

### Already Set Up?
Just run:
```powershell
.\start.ps1
```

### Showing to Someone?
1. Run `start.ps1`
2. Open browser to http://localhost:8501
3. Go to Control Panel window
4. Press `5` then `9` (EMERGENCY) - triggers ALL alarms!
5. Watch dashboard go red + hear beeps 🔴🔊

---

## ❓ Common Questions

**Q: Is this using real sensors?**  
A: No, it's simulated (fake). Perfect for learning without buying hardware!

**Q: Do I need internet?**  
A: Yes, for the cloud MQTT broker (HiveMQ Cloud). Dashboard works offline though.

**Q: Can I change the sensor values?**  
A: Yes! Use the Control Panel (Window 4) to set custom values.

**Q: Why 4 windows?**  
A: Each part runs separately: Dashboard, Alerts, Sensors, Control. You can close any you don't need.

**Q: Can I run this on Mac/Linux?**  
A: Almost! Change `.\start.ps1` to run each Python file separately. The code works on any OS.

---

## 🆘 Need Help?

1. **Check QUICK_START.md** - More detailed setup guide
2. **Run verify_system.py** - Tests if everything is installed correctly
3. **Open an Issue** - https://github.com/Avi2014/Smart-Home-Monitoring/issues

---

## 📞 Credits

**Built by:** [@Avi2014](https://github.com/Avi2014)  
**Purpose:** IoT Lab Project  
**Technologies:** Python, Streamlit, MQTT, HiveMQ Cloud  
**License:** Free to use (MIT)

---

<div align="center">

**⭐ If this helped you, star the repo!**

[📖 Full Documentation](README_DETAILED.md) · 
[🐛 Report Problem](https://github.com/Avi2014/Smart-Home-Monitoring/issues) · 
[💬 Ask Question](https://github.com/Avi2014/Smart-Home-Monitoring/discussions)

Made with ❤️ for students learning IoT

</div>
