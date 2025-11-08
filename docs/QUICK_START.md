# 🚀 Quick Start Guide - 5 Minutes to Running System

Get the Smart Home IoT Monitoring System up and running in just 5 minutes!

## ⚡ Super Quick Start (TL;DR)

```powershell
# 1. Clone
git clone https://github.com/Avi2014/Smart-Home-Monitoring.git
cd Smart-Home-Monitoring

# 2. Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Run
.\start.ps1
```

**Done!** 🎉 Dashboard opens at http://localhost:8501

---

## 📋 Detailed Steps

### Step 1: Install Prerequisites (2 minutes)

#### Check Python Version
```powershell
python --version
# Should show: Python 3.13.x or higher
```

**Don't have Python?**
1. Download from https://www.python.org/downloads/
2. During installation: ✅ Check "Add Python to PATH"
3. Restart terminal after installation

#### Check Git
```powershell
git --version
# Should show: git version 2.x.x
```

**Don't have Git?**
- Download from https://git-scm.com/downloads

---

### Step 2: Clone Repository (30 seconds)

```powershell
# Clone the project
git clone https://github.com/Avi2014/Smart-Home-Monitoring.git

# Navigate to project folder
cd Smart-Home-Monitoring
```

---

### Step 3: Create Virtual Environment (1 minute)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

**Troubleshooting:** If activation fails with "execution policy" error:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# Then try activating again
```

You should see `(venv)` prefix in your terminal:
```
(venv) PS C:\...\Smart-Home-Monitoring>
```

---

### Step 4: Install Dependencies (1 minute)

```powershell
pip install -r requirements.txt
```

**What's being installed:**
- Streamlit 1.40.2 (Dashboard)
- Plotly 5.24.1 (Charts)
- Paho-MQTT 2.1.0 (IoT messaging)
- Pandas, NumPy (Data processing)
- python-dotenv (Configuration)

**Wait for:** "Successfully installed..." message

---

### Step 5: Verify Installation (30 seconds)

```powershell
python verify_system.py
```

**You should see:**
```
✅ Python version 3.13.5
✅ All required packages installed
✅ .env file present
✅ HiveMQ Cloud connection successful
✅ MQTT publish/subscribe working
```

**If any checks fail:** See troubleshooting section below

---

### Step 6: Launch System (10 seconds)

```powershell
.\start.ps1
```

**What happens:**
1. ✅ Checks virtual environment
2. 🚀 Opens 4 terminal windows:
   - **Window 1:** Dashboard (Streamlit)
   - **Window 2:** Alert System
   - **Window 3:** Sensor Simulators
   - **Window 4:** Interactive Control
3. 🌐 Opens browser to http://localhost:8501

**You should see:**
```
============================================
 Smart Home IoT Monitoring System
============================================

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
```

---

## 🎯 Verify Everything Works

### Check 1: Dashboard (http://localhost:8501)

**You should see:**
- 🟢 **Connected** status (top right)
- **4 Gauges:** Temperature, Humidity, CO2, Light
- **4 Charts:** Trend lines with flowing data
- **Sidebar:** Message count increasing

**Wait 10-15 seconds** for sensors to connect and start publishing data.

### Check 2: Sensors Terminal

**You should see:**
```
🌡️ Temperature: 24.5°C | Battery: 100.0% | Messages: 1
🌡️ Temperature: 24.3°C | Battery: 100.0% | Messages: 2
🌡️ Temperature: 24.6°C | Battery: 100.0% | Messages: 3
...
```

Similar output for all 4 sensors (Temperature, Humidity, CO2, Light).

### Check 3: Alert System Terminal

**You should see:**
```
Alert System Active - Listening for sensor data...
✅ Temperature: 24.5°C (Normal)
✅ Humidity: 52.3% (Normal)
✅ CO2: 650 ppm (Normal)
✅ Light: 450 lux (Normal)
```

### Check 4: Interactive Control Terminal

**You should see:**
```
═══════════════════════════════════════
  🎮 INTERACTIVE SENSOR CONTROL PANEL
═══════════════════════════════════════

1. 🌡️  Set Temperature
2. 💧  Set Humidity
...
9. ❌  Exit

Select option [1-9]:
```

---

## 🧪 Test the System

### Test 1: Trigger an Alarm

1. Go to **Interactive Control** terminal
2. Press **`5`** (Quick Test Scenarios)
3. Press **`2`** (High Temperature - 35°C)
4. Press **Enter**

**Expected result:**
- 🔊 **Beep sound** from Alert System
- 🚨 **Console message:** "ALERT: Temperature HIGH..."
- 🔴 **Dashboard gauge** turns red

### Test 2: Clear the Alarm

1. In Interactive Control
2. Press **`5`** (Quick Test Scenarios)
3. Press **`1`** (Normal conditions)
4. Press **Enter**

**Expected result:**
- ✅ **Alert clears** in Alert System
- 🟢 **Dashboard gauge** turns green
- 📝 **Console:** "Alert cleared for temperature"

### Test 3: View Real-Time Data

1. Open **Dashboard** in browser (http://localhost:8501)
2. Watch the **trend charts** for 30 seconds
3. See the **lines moving** with random sensor data
4. Check **message count** increasing in sidebar

---

## 🛑 How to Stop

### Method 1: Close All Windows
Simply close all 4 terminal windows that opened.

### Method 2: Ctrl+C Each Terminal
Press `Ctrl+C` in each terminal window.

### Method 3: Kill All Python
```powershell
taskkill /F /IM python.exe
```

---

## 🔧 Troubleshooting

### Issue: "Python not found"
**Solution:**
1. Install Python 3.13+ from https://www.python.org/downloads/
2. During installation: ✅ Check "Add Python to PATH"
3. Restart terminal

### Issue: "Cannot activate virtual environment"
**Solution:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv\Scripts\Activate.ps1
```

### Issue: "Module not found" errors
**Solution:**
```powershell
# Make sure venv is activated (see (venv) prefix)
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "MQTT connection failed"
**Solution:**
1. Check internet connection
2. Verify `.env` file exists with credentials
3. Run: `python verify_system.py`
4. Check firewall allows port 8883

### Issue: "Port 8501 already in use"
**Solution:**
```powershell
# Find process using port 8501
netstat -ano | findstr :8501

# Kill that process (replace PID)
taskkill /F /PID <process_id>

# Or change Streamlit port
streamlit run dashboard.py --server.port 8502
```

### Issue: "No data on dashboard"
**Solution:**
1. Wait 10-15 seconds for sensors to connect
2. Check **Sensors terminal** - should show "Messages: 1, 2, 3..."
3. Check **Dashboard** shows "🟢 Connected" (not "🔴 Disconnected")
4. Refresh browser (F5)
5. Check debug output in Dashboard terminal for "📨 Received message..."

### Issue: "Dashboard not opening in browser"
**Solution:**
1. Manually open browser
2. Go to: http://localhost:8501
3. If still not working, check Dashboard terminal for errors

---

## ⚙️ Configuration (Optional)

### Change Sensor Update Rate

**Default:** 3 seconds

**Edit:** `src/sensors/sensor_config.json`
```json
{
  "sensors": {
    "temperature": {
      "sampling_rate": 1  // Change to 1-10 seconds
    }
  }
}
```

### Change Dashboard Refresh Rate

**Default:** 3 seconds

**Method 1 - In Browser:**
- Open dashboard sidebar
- Adjust "Refresh Rate" slider

**Method 2 - In Code:**
Edit `dashboard.py` line 328:
```python
refresh_rate = st.slider("Refresh Rate (seconds)", 1, 10, 3)
#                                                          ^ change default
```

### Change Alert Thresholds

**Edit:** `alert_system.py` (lines 30-35)
```python
self.thresholds = {
    'temperature': (20, 28),  # (min, max) in °C
    'humidity': (40, 60),     # (min, max) in %
    'co2': (400, 1000),       # (min, max) in ppm
    'light': (200, 800)       # (min, max) in lux
}
```

---

## 📚 What's Next?

### Learn More
- **[README.md](README.md)** - Complete documentation
- **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - Detailed features
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Cloud deployment

### Explore Features
1. **Test all 9 scenarios** in Interactive Control
2. **Adjust thresholds** and trigger custom alarms
3. **Monitor trends** for 5-10 minutes
4. **Customize ranges** in sensor_config.json

### Deploy to Cloud
- Streamlit Cloud (free): Share dashboard publicly
- AWS/Azure VM: 24/7 operation
- Docker: Containerized deployment

---

## 🎉 Success!

You now have a fully functional IoT monitoring system running!

**What you have:**
- ✅ Real-time dashboard with live data
- ✅ 4 sensors publishing data every 3 seconds
- ✅ Alert system monitoring thresholds
- ✅ Interactive control for testing
- ✅ Cloud MQTT broker (HiveMQ)

**Next steps:**
- Run for 30 minutes and observe patterns
- Trigger different alarm scenarios
- Take screenshots for lab report
- Experiment with configurations

---

<div align="center">

**Need help?** Open an issue on GitHub or check the full README.md

[📖 Full Documentation](README.md) · 
[🐛 Report Issue](https://github.com/Avi2014/Smart-Home-Monitoring/issues) · 
[💬 Discussions](https://github.com/Avi2014/Smart-Home-Monitoring/discussions)

**Built with ❤️ for IoT Education**

</div>
