# 🎛️ Alarm System - Complete Setup & Testing Guide

## ✅ What's Been Set Up

Your IoT system now has **3 working components**:

### 1. 📊 **Dashboard** (Streamlit)
- Real-time gauges for all 4 sensors
- Historical trend charts
- MQTT connection status
- Battery levels

### 2. 🚨 **Alert System** (`alert_system_fixed.py`)
- Monitors all 4 sensor values
- **Triggers BEEP when thresholds exceeded**
- Shows alert messages
- Clears alerts when values return to normal

### 3. 🎮 **Interactive Control Panel** (`interactive_control.py`)
- Manual control of all sensor values
- Quick test scenarios
- Continuous mode

---

## 🚀 HOW TO TEST THE ALARM (3 Steps)

### Step 1: Start Alert System
```powershell
python alert_system_fixed.py
```
You should see:
```
✅ Connected to MQTT Broker
📡 Subscribed to all topics
🎯 Alert System Active - Listening...
```

### Step 2: Start Interactive Control
```powershell
python interactive_control.py
```
You should see the menu with options 1-8

### Step 3: Trigger an Alarm
In the interactive control panel:
1. **Press `5`** (Quick Test Scenarios)
2. **Press `2`** (High temperature - 35°C)
3. **Watch the alert terminal** - you should see:
   - 🚨 Red alert message
   - 🔊 **BEEP SOUND!**
4. **Press `1`** (Normal conditions) to clear the alarm

---

## 🎯 Alarm Thresholds

| Sensor | Safe Range | Alarm Triggers When |
|--------|------------|---------------------|
| 🌡️ Temperature | 20-28°C | < 20°C or > 28°C |
| 💧 Humidity | 40-60% | < 40% or > 60% |
| 🌫️ CO2 | 400-1000 ppm | > 1000 ppm |
| 💡 Light | 200-800 lux | < 200 or > 800 lux |

---

## 📋 Quick Test Scenarios Available

From interactive_control.py → Option 5:

| Scenario | What It Does | Expected Alarm |
|----------|--------------|----------------|
| 1 | Normal conditions | None (clears all) |
| 2 | Temperature 35°C | 🔥 HIGH TEMP |
| 3 | Temperature 15°C | ❄️ LOW TEMP |
| 4 | Humidity 80% | 💧 HIGH HUMIDITY |
| 5 | Humidity 25% | 🌵 LOW HUMIDITY |
| 6 | CO2 1500 ppm | 🌫️ HIGH CO2 |
| 7 | Light 950 lux | 💡 BRIGHT LIGHT |
| 8 | Light 50 lux | 🌑 LOW LIGHT |
| 9 | ALL CRITICAL | 🚨 EMERGENCY - All alarms! |

---

## 🔍 Troubleshooting

### No BEEP Sound?
1. **Check volume** - Make sure Windows volume is up
2. **Try winsound** - Run this test:
   ```powershell
   python -c "import winsound; winsound.Beep(1000, 500)"
   ```
3. **Check alert terminal** - Should show alert messages even if no sound

### Alert System Not Receiving Data?
1. Check MQTT connection status (should see "Connected")
2. Make sure interactive_control.py is connected
3. Try publishing with quick_alarm_test.py

### Dashboard Not Updating?
1. Check MQTT status (should be 🟢 Green)
2. Click "Reconnect" button
3. Refresh browser

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `alert_system_fixed.py` | Main alarm system with beeps |
| `interactive_control.py` | Manual sensor control panel |
| `quick_alarm_test.py` | Quick single alarm test |
| `test_alarm.py` | Full alarm test suite |

---

## 🎬 Demo Sequence (For Presentation)

**Perfect for showing your project:**

1. **Start everything:**
   ```powershell
   # Terminal 1:
   streamlit run dashboard.py
   
   # Terminal 2:
   python alert_system_fixed.py
   
   # Terminal 3:
   python interactive_control.py
   ```

2. **Normal conditions (baseline):**
   - In control panel: Press `5` → Press `1`
   - Show dashboard with normal green gauges

3. **Single alarm (high temp):**
   - Press `5` → Press `2`
   - 🔊 **BEEP!**
   - Show red alert on dashboard

4. **Emergency scenario:**
   - Press `5` → Press `9`
   - 🔊🔊🔊🔊 **Multiple BEEPS!**
   - All gauges red
   - Multiple alert messages

5. **Recovery:**
   - Press `5` → Press `1`
   - ✅ Alarms clear
   - Gauges return to green

---

## 💡 Pro Tips

1. **Volume Up!** - Beeps are only 500ms, make sure you can hear them
2. **Multiple Terminals** - Keep all 3 terminals visible to see real-time updates
3. **Scenarios 9** - Most impressive for demos (all alarms at once!)
4. **Dashboard + Alert Side-by-Side** - Best view to see correlation

---

## ✅ Verification Checklist

- [ ] Alert system connects to MQTT
- [ ] Interactive control connects to MQTT
- [ ] Dashboard shows 🟢 Connected
- [ ] Can manually set sensor values
- [ ] Alert beeps when threshold exceeded
- [ ] Alert message appears in terminal
- [ ] Dashboard shows red when alert active
- [ ] Alert clears when value returns to normal

---

**🎉 Your alarm system is ready to demo!**

Use `interactive_control.py` to manually trigger any sensor value and watch the alarm system respond in real-time!
