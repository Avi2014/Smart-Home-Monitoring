# Alert System Test Guide

## 🚨 How to Test the Alert System

### Method 1: Using Test Script (Automated)

**Terminal 1 - Start Alert System:**
```powershell
python alert_system.py
# Press Enter when prompted
```

**Terminal 2 - Run Tests:**
```powershell
python test_alerts.py
# Press Enter when prompted
```

The test will send 12 different alert scenarios and you'll hear beeps!

---

### Method 2: Using Real Sensors (Manual)

The alert system monitors your sensors and triggers when values go outside safe ranges:

**Safe Ranges:**
- 🌡️ Temperature: 20-28°C
- 💧 Humidity: 40-60%
- 🌫️ CO2: 400-1000 ppm
- 💡 Light: 200-800 lux

**To trigger alerts:**

1. **Start alert system:**
   ```powershell
   python alert_system.py
   ```

2. **Run sensors** - they will randomly spike and trigger alerts:
   ```powershell
   python sensors\temperature_sensor.py
   python sensors\humidity_sensor.py
   python sensors\co2_sensor.py
   python sensors\light_sensor.py
   ```

3. **Watch for alerts!** The system will:
   - Print alert messages
   - Play beep sounds (🔊)
   - Show when alerts clear

---

### What Triggers Alerts?

The sensors have built-in "spike" simulation that occasionally sends extreme values:

- **Temperature spikes**: ±3-4°C (may go outside 20-28°C)
- **Humidity spikes**: ±10-15% (may go outside 40-60%)
- **CO2 spikes**: +200-400 ppm (may go above 1000 ppm)
- **Light spikes**: ±200-300 lux (may go outside 200-800 lux)

**Spike probability**: 5% (configured in `sensor_config.json`)

---

### Expected Output

When alert triggers:
```
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

  ⚠️  ALERT #1 - TOO HIGH
  📊 Sensor: Temperature
  📈 Current Value: 35.0 °C
  ✅ Safe Range: 20 - 28 °C
  ⏰ Time: 01:45:23

🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

[BEEP SOUND]
```

When alert clears:
```
✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅

  ✅ ALERT CLEARED
  📊 Sensor: Temperature
  📈 Current Value: 24.0 °C
  ⏰ Time: 01:45:30

✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅
```

---

### Troubleshooting

**No alerts appearing:**
- Make sure alert_system.py is running
- Check sensors are publishing data
- Verify using same MQTT broker (test.mosquitto.org)
- Wait for random spikes (5% probability)

**No beep sound:**
- Normal on some systems
- Visual alerts still work
- Check Windows volume is on

**Too many/few alerts:**
- Adjust thresholds in alert_system.py
- Modify spike probability in sensors/sensor_config.json

---

### For Lab Report

**Screenshots to capture:**
1. Alert system startup screen
2. Alert triggered (with full details)
3. Alert cleared message
4. Multiple alerts from different sensors
5. Alert count summary

**Metrics to document:**
- Number of alerts triggered
- Response time (instant)
- Alert types (too high/too low)
- Clear time when values normalize

---

## Quick Commands

```powershell
# Terminal 1: Alert System
python alert_system.py

# Terminal 2: Run all sensors (more chances for alerts)
python sensors\temperature_sensor.py

# Terminal 3: Or use test suite
python test_alerts.py
```

**Let the sensors run for 2-3 minutes to see natural alerts from spike simulation!**
