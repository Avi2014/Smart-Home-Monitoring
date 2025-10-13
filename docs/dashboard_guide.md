# IoT Dashboard Quick Start Guide

## 🚀 How to Run Your Dashboard

### Option 1: Quick Start (Single Command)
```powershell
# This will start the dashboard
streamlit run dashboard.py
```

Then in **separate terminals**, run the sensors:
```powershell
# Terminal 2
python sensors\temperature_sensor.py

# Terminal 3
python sensors\humidity_sensor.py

# Terminal 4
python sensors\co2_sensor.py

# Terminal 5
python sensors\light_sensor.py
```

### Option 2: Run All Sensors at Once
```powershell
# Terminal 1: Dashboard
streamlit run dashboard.py

# Terminal 2: All sensors
python sensors\run_all_sensors.py
```

---

## 📊 What You'll See

1. **Dashboard URL**: http://localhost:8501
2. **Real-time gauges** showing current values
3. **Trend charts** showing historical data
4. **Battery levels** for each sensor
5. **Connection status** and message counts

---

## 🎯 Features

### Gauges Section
- 🌡️ **Temperature** - Shows current temp with safe range indicator
- 💧 **Humidity** - Real-time humidity percentage
- 🌫️ **CO2** - Air quality monitoring
- 💡 **Light** - Light level in lux

### Trend Charts
- Last 50 data points for each sensor
- Time-based X-axis
- Interactive hover tooltips
- Auto-scaling Y-axis

### Sidebar
- Battery status for all sensors
- Data point counts
- Clear data button
- Connection status

---

## 🔧 Troubleshooting

### Dashboard won't start
```powershell
# Make sure you're in the venv
.\venv\Scripts\Activate.ps1

# Reinstall if needed
pip install streamlit plotly
```

### No data appearing
1. Check if sensors are running
2. Verify MQTT connection (should show 🟢 Connected)
3. Check sensors are using same broker (`test.mosquitto.org`)

### Dashboard freezes
- Refresh browser (F5)
- Or click "Clear Data" in sidebar

---

## 📸 Taking Screenshots for Lab Report

1. Start all sensors
2. Let them run for 2-3 minutes
3. Take screenshot of:
   - Full dashboard view
   - Gauge section (current values)
   - Trend charts (historical data)
   - Sidebar (battery levels)

---

## 🎓 For Your Lab Report

### What to Document:
1. **Dashboard screenshots** - Full view and details
2. **Real-time updates** - Show data changing over time
3. **Battery simulation** - Battery levels decreasing
4. **Data visualization** - How trends are displayed
5. **Message counts** - Throughput demonstration

### Key Features to Highlight:
- ✅ Real-time data updates (every 2 seconds)
- ✅ Multiple sensor types
- ✅ Interactive visualizations
- ✅ Battery level monitoring
- ✅ Historical trend analysis
- ✅ Threshold indicators (safe zones)

---

## 🚦 Next Steps

After running the dashboard:
1. ✅ Test latency measurement: `python metrics\latency_test.py`
2. ✅ Test throughput: `python metrics\throughput_test.py`
3. ✅ Analyze battery life: `python metrics\battery_simulation.py`
4. 📝 Document results for lab report

---

## 💡 Tips

- Dashboard updates every 2 seconds automatically
- Keeps last 50 data points per sensor
- Works with any MQTT broker
- Can be customized easily
- Access from any device on same network using your IP

---

**Enjoy your IoT Dashboard!** 🎉
