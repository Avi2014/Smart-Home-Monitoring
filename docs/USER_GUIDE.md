# 🎛️ Smart Home IoT Monitoring - User Guide

## 📖 Table of Contents
1. [System Overview](#system-overview)
2. [Starting the System](#starting-the-system)
3. [Using the Dashboard](#using-the-dashboard)
4. [Alert System](#alert-system)
5. [Interactive Control](#interactive-control)
6. [Sensor Simulators](#sensor-simulators)
7. [Performance Metrics](#performance-metrics)

---

## 🏠 System Overview

### Components

| Component | Purpose | Access |
|-----------|---------|--------|
| **Dashboard** | Real-time visualization | http://localhost:8501 |
| **Alert System** | Threshold monitoring & alarms | Terminal output + beeps |
| **Sensors** | Simulate IoT devices | Background process |
| **Interactive Control** | Manual testing | Terminal interface |

### Architecture

```
Sensors → MQTT Broker → Dashboard + Alert System
                            ↓           ↓
                     Visual Display   Beep Alarms
```

---

## 🚀 Starting the System

### Method 1: Quick Start (Recommended)

```powershell
.\scripts\start_all.ps1
```

This starts:
- ✅ Dashboard (http://localhost:8501)
- ✅ Alert System
- ✅ All 4 sensor simulators

### Method 2: Manual Start

**Terminal 1 - Dashboard:**
```powershell
streamlit run dashboard.py
```

**Terminal 2 - Alert System:**
```powershell
python alert_system.py
```

**Terminal 3 - Sensors:**
```powershell
python src\sensors\run_all_sensors.py
```

**Terminal 4 - Interactive Control (Optional):**
```powershell
python interactive_control.py
```

---

## 📊 Using the Dashboard

### Main Features

#### 1. Status Bar
- **MQTT Status**: 🟢 Connected / 🔴 Disconnected
- **Messages Received**: Total count
- **Last Update**: Timestamp of latest data
- **Broker**: MQTT broker address

#### 2. Current Sensor Readings (Gauges)
- 🌡️ **Temperature** (°C)
- 💧 **Humidity** (%)
- 🌫️ **CO2** (ppm)
- 💡 **Light** (lux)

**Color Coding:**
- 🟢 **Green Zone**: Safe range
- 🟡 **Yellow Zone**: Warning  
- 🔴 **Red Zone**: Critical (alarm triggers)

#### 3. Historical Trends (Charts)
- Line graphs showing last 50 data points
- X-axis: Time
- Y-axis: Sensor value
- Hover for exact values

#### 4. Sidebar
- **Battery Status**: Real-time battery levels
- **Data Info**: Number of data points per sensor
- **Clear Data**: Reset all charts

### Dashboard Actions

**Reconnect MQTT:**
- If status shows 🔴 Disconnected
- Click "🔄 Reconnect" button

**Clear Data:**
- Sidebar → "🔄 Clear Data" button
- Resets all historical charts

**Refresh:**
- Auto-refreshes every 2 seconds
- Manual refresh: `F5` or refresh browser

---

## 🚨 Alert System

### Threshold Configuration

| Sensor | Safe Range | Alert Triggers |
|--------|------------|----------------|
| 🌡️ Temperature | 20-28°C | <20°C or >28°C |
| 💧 Humidity | 40-60% | <40% or >60% |
| 🌫️ CO2 | 400-1000 ppm | >1000 ppm |
| 💡 Light | 200-800 lux | <200 or >800 lux |

### Alert Types

**🔊 BEEP Alarm:**
- Audible beep when threshold exceeded
- 1000Hz for 500ms
- Only triggers once per alert

**📋 Terminal Alert:**
```
======================================================================
🚨🚨🚨 ALERT #1 - HIGH TEMPERATURE 🚨🚨🚨
======================================================================
🌡️ Current Value: 35.0°C
⚠️  Threshold Limit: 28°C
🕐 Time: 14:30:45
======================================================================
```

**✅ Alert Cleared:**
```
======================================================================
✅ ALERT CLEARED - TEMPERATURE
======================================================================
🌡️ Current Value: 24.0°C (Back to normal)
🕐 Time: 14:31:10
======================================================================
```

### Monitoring Alerts

1. **Watch the alert system terminal**
2. **Listen for beep sounds** 🔊
3. **Check dashboard** for red gauges
4. **Alert count** shown in terminal

---

## 🎮 Interactive Control

### Starting Interactive Control

```powershell
python interactive_control.py
```

### Menu Options

```
1. 🌡️  Set Temperature
2. 💧 Set Humidity
3. 🌫️  Set CO2 Level
4. 💡 Set Light Level
5. 🚀 Quick Test Scenarios
6. 🔄 Continuous Mode
7. 📊 View Current Values
8. ❌ Exit
```

### Manual Control

**Example: Set Temperature**
1. Press `1`
2. Enter value: `35`
3. Press Enter
4. Watch dashboard update
5. Hear alarm beep! 🔊

### Quick Test Scenarios

**Press `5` to access:**

| Scenario | Description | Alarm? |
|----------|-------------|--------|
| 1 | Normal conditions | ❌ No |
| 2 | High temperature (35°C) | ✅ Yes |
| 3 | Low temperature (15°C) | ✅ Yes |
| 4 | High humidity (80%) | ✅ Yes |
| 5 | Low humidity (25%) | ✅ Yes |
| 6 | High CO2 (1500 ppm) | ✅ Yes |
| 7 | Bright light (950 lux) | ✅ Yes |
| 8 | Low light (50 lux) | ✅ Yes |
| 9 | **EMERGENCY** (all critical) | ✅✅✅✅ Yes! |

**Recommended Test Sequence:**
1. Press `5` (Scenarios)
2. Press `1` (Normal) - baseline
3. Wait 5 seconds
4. Press `2` (High temp) - trigger alarm
5. Wait for beep 🔊
6. Press `1` (Normal) - clear alarm

### Continuous Mode

Gradually changes sensor values automatically.

1. Press `6`
2. Watch values increase over time
3. Alarms trigger as thresholds crossed
4. Press `Ctrl+C` to stop

---

## 🔌 Sensor Simulators

### What They Simulate

**🌡️ Temperature Sensor:**
- Daily cycles (cooler at night, warmer during day)
- Random spikes (+3 to -3°C)
- Smooth transitions (sensor inertia)
- Range: 18-35°C

**💧 Humidity Sensor:**
- Inverse daily pattern (higher at night)
- Random spikes (±10-15%)
- Weather-like variations
- Range: 30-80%

**🌫️ CO2 Sensor:**
- Occupancy-based (higher during sleep/study)
- Poor ventilation spikes (+200-400 ppm)
- Air quality classification
- Range: 400-2000 ppm

**💡 Light Sensor:**
- Natural light cycle (0 at night, high during day)
- Artificial lighting in evening
- Window/curtain effects
- Range: 0-1000 lux

### Running Sensors

**All Sensors:**
```powershell
python src\sensors\run_all_sensors.py
```

**Individual Sensor:**
```powershell
python src\sensors\temperature_sensor.py
python src\sensors\humidity_sensor.py
python src\sensors\co2_sensor.py
python src\sensors\light_sensor.py
```

**Stop Sensors:**
- Press `Ctrl+C` in terminal

---

## 📈 Performance Metrics

### Latency Test

Measures end-to-end message delay.

```powershell
python src\metrics\latency_test.py
```

**Output:**
- Mean latency
- Median latency
- Min/Max latency
- Latency distribution

### Throughput Test

Measures messages per second.

```powershell
python src\metrics\throughput_test.py
```

**Output:**
- Total messages received
- Messages per second
- Per-sensor breakdown
- Data rate estimation

### Battery Simulation

Estimates battery life for different configurations.

```powershell
python src\metrics\battery_simulation.py
```

**Output:**
- Current config battery life
- Optimized config battery life
- High-frequency scenario
- Low-power scenario

---

## 💡 Tips & Best Practices

### For Demonstrations

1. **Start everything first**
2. **Show normal dashboard** (green gauges)
3. **Use interactive control** to trigger alarms
4. **Point out beep sounds** 🔊
5. **Show alert messages** in terminal
6. **Clear alarms** to show system recovery

### For Testing

1. **Use scenario 9** (Emergency) for dramatic effect
2. **Keep terminals side-by-side** to see correlations
3. **Test one sensor at a time** for clarity
4. **Document alert counts** from terminal stats

### For Development

1. **Modify thresholds** in `src/sensors/sensor_config.json`
2. **Adjust sampling rates** per sensor
3. **Change battery drain rate** for different scenarios
4. **Customize dashboard layout** in `dashboard.py`

---

## 🎯 Common Use Cases

### Use Case 1: Quick Demo
```powershell
.\scripts\start_all.ps1
# Wait for everything to load
# Open browser to localhost:8501
# Show real-time updates
```

### Use Case 2: Test Specific Alarm
```powershell
# Terminal 1: python alert_system.py
# Terminal 2: python interactive_control.py
# In control panel: Press 5 → 2 (High temp)
# Watch alarm trigger!
```

### Use Case 3: Collect Metrics
```powershell
python src\metrics\latency_test.py > results_latency.txt
python src\metrics\throughput_test.py > results_throughput.txt
python src\metrics\battery_simulation.py > results_battery.txt
```

---

## ❓ FAQs

**Q: Dashboard shows "Disconnected"?**
A: Click "Reconnect" button or check internet connection.

**Q: No beep sounds?**
A: Check volume, verify `winsound` module, or check if value actually exceeds threshold.

**Q: Sensors not publishing?**
A: Check MQTT broker connection, restart sensors with `Ctrl+C` and rerun.

**Q: Want different alert thresholds?**
A: Edit `src/sensors/sensor_config.json` and restart alert system.

**Q: Can I use my own MQTT broker?**
A: Yes! Change broker address in `src/sensors/sensor_config.json`.

---

**🎉 Enjoy your Smart Home IoT Monitoring System!**

For setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)  
For deployment options, see [DEPLOYMENT.md](DEPLOYMENT.md)
