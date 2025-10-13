# 🚨 Alert System - Complete Guide

## What Is It?

The **Alert System** monitors your IoT sensors in real-time and triggers alarms when values go outside safe ranges. It will:
- ✅ Display alert messages
- 🔊 Play beep sounds (Windows)
- 📊 Track alert count
- ✅ Clear alerts when values return to normal

---

## 🎯 How to Test Alerts

### Option 1: Quick Demo (Easiest!)

Run this single command to see instant alerts:

```powershell
python quick_alert_test.py
```

**What it does:**
1. Sends a HIGH temperature (35°C - triggers alert!)
2. Wait 2 seconds
3. Sends NORMAL temperature (24°C - clears alert!)

**You'll see:**
```
🚨🚨🚨 ALERT - TOO HIGH 🚨🚨🚨
Temperature: 35°C
[BEEP SOUND]

✅✅✅ ALERT CLEARED ✅✅✅  
Temperature: 24°C
```

---

### Option 2: Live Monitoring (Most Realistic!)

**Step 1:** Start the alert system
```powershell
python alert_system.py
```

**Step 2:** Run your sensors (they have random spikes!)
```powershell
# Open new terminals for each:
python sensors\temperature_sensor.py
python sensors\humidity_sensor.py
python sensors\co2_sensor.py
python sensors\light_sensor.py
```

**Step 3:** Wait and watch! 
- Sensors randomly spike every ~30-60 seconds
- Alerts trigger automatically when spikes exceed thresholds
- You'll hear beeps! 🔊

---

### Option 3: Automated Test Suite

**Terminal 1:**
```powershell
python alert_system.py
```

**Terminal 2:**
```powershell
python test_alerts.py
```

This sends 12 different test scenarios:
- Temperature: Too high, too low, normal
- Humidity: Too high, too low, normal
- CO2: Too high, too low, normal
- Light: Too high, too low, normal

---

## 🎚️ Alert Thresholds

| Sensor | Safe Range | Alert Triggers When |
|--------|------------|---------------------|
| 🌡️ Temperature | 20-28°C | < 20°C or > 28°C |
| 💧 Humidity | 40-60% | < 40% or > 60% |
| 🌫️ CO2 | 400-1000 ppm | < 400 or > 1000 ppm |
| 💡 Light | 200-800 lux | < 200 or > 800 lux |

---

## 📸 For Your Lab Report

### Screenshots to Capture:

1. **Alert System Startup:**
   - Shows threshold configuration
   - Connection status
   - Monitoring message

2. **Alert Triggered:**
   - Full alert message with sensor details
   - Shows current value vs safe range
   - Timestamp

3. **Alert Cleared:**
   - Clearance message
   - New normal value

4. **Multiple Alerts:**
   - Different sensor types
   - Alert count increasing

---

## 🔊 About the Sounds

**Alert Triggered:** Low beep (1000 Hz, 500ms)  
**Alert Cleared:** High beep (2000 Hz, 200ms)

*Note: Sounds work on Windows. If no sound, visual alerts still work perfectly!*

---

## 💡 Tips

1. **Best for demo:** Use `quick_alert_test.py` - instant results!
2. **Best for realism:** Run actual sensors - watch natural alerts
3. **Most comprehensive:** Use `test_alerts.py` - tests all scenarios

---

## 🎓 What to Document

For your lab report, describe:

1. **Alert System Purpose**
   - Real-time monitoring
   - Threshold-based alerts
   - Automated notifications

2. **Implementation**
   - MQTT subscription
   - Threshold checking
   - Alert triggering logic

3. **Results**
   - Number of alerts triggered
   - Response time (instant)
   - Alert types demonstrated

4. **Real-world Applications**
   - Fire safety (high temperature)
   - Flood detection (high humidity)
   - Air quality (high CO2)
   - Security (light changes)

---

## 🚀 Quick Start

```powershell
# Easiest way to see alerts NOW:
python quick_alert_test.py

# Press Enter when prompted
# Watch the magic! ✨
```

---

**Your alert system is ready to protect your IoT environment!** 🛡️
