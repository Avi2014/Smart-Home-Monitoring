# 🎛️ Interactive Sensor Control Guide

## Overview
Manually control sensor values to test the dashboard and trigger alarms in real-time!

## Quick Start

### 1. Start the Dashboard (if not running)
```powershell
streamlit run dashboard.py
```

### 2. Start the Alert System (if not running)
```powershell
python alert_system.py
```

### 3. Launch Interactive Control Panel
```powershell
python interactive_sensor_control.py
```

## Features

### 📊 Manual Sensor Control
Control any sensor individually:
- **Temperature**: Set any value (°C)
- **Humidity**: Set any value (%)
- **CO2**: Set any value (ppm)
- **Light**: Set any value (lux)

### 🚨 Alarm Thresholds
Values outside these ranges will trigger alarms:
- 🌡️ **Temperature**: 20-28°C (safe)
- 💧 **Humidity**: 40-60% (safe)
- 🌫️ **CO2**: 400-1000 ppm (safe)
- 💡 **Light**: 200-800 lux (safe)

### 🚀 Quick Test Scenarios
Pre-configured scenarios to test different alert conditions:

1. **Normal conditions** - All sensors in safe range
2. **High temperature** - 35°C (triggers alarm 🔥)
3. **Low temperature** - 15°C (triggers alarm ❄️)
4. **High humidity** - 85% (triggers alarm 💦)
5. **High CO2** - 1500 ppm (triggers alarm 🌫️)
6. **Low light** - 50 lux (triggers alarm 🕯️)
7. **Multiple alerts** - Temperature + CO2 high
8. **Emergency** - All sensors critical! 🚨

### 🔄 Continuous Mode
Keep sending values at regular intervals:
- Choose sensor
- Enter value
- Set interval (e.g., 2 seconds)
- Watch dashboard update in real-time

## Usage Examples

### Example 1: Test Temperature Alarm
```
1. Select: 1 (Temperature)
2. Enter value: 35
3. Watch dashboard turn red
4. Hear beep alarm! 🔊
```

### Example 2: Test Multiple Alarms
```
1. Select: 5 (Quick Scenarios)
2. Select: 7 (Multiple alerts)
3. See both temperature and CO2 alarms
4. Multiple beeps! 🔊🔊
```

### Example 3: Gradual Temperature Increase
```
1. Select: 6 (Continuous Mode)
2. Select: 1 (Temperature)
3. Enter interval: 2 seconds
4. Start with: 24°C (normal)
5. Then: 26°C (still normal)
6. Then: 29°C (alarm triggers! 🚨)
```

### Example 4: Emergency Scenario
```
1. Select: 5 (Quick Scenarios)
2. Select: 8 (Emergency)
3. ALL sensors go critical!
4. Multiple alarms beeping! 🚨🔊
```

## How It Works

```
Interactive Control → MQTT Broker → Dashboard + Alert System
                                         ↓           ↓
                                    Visual Update  Beep Alarm
```

1. **You enter value** in interactive control
2. **Published to MQTT** broker
3. **Dashboard receives** and updates gauges/charts
4. **Alert system checks** if value exceeds thresholds
5. **Alarm beeps** if threshold crossed! 🔊

## Dashboard Changes to Watch

### When Normal (Safe Range):
- ✅ Green indicators
- 🟢 Gauges in green zone
- 😊 No alarms

### When Alert Triggered:
- 🚨 Red indicators on dashboard
- 🔴 Gauges showing red zone
- 🔊 **BEEP BEEP BEEP** from alert system!
- 📊 Trend charts spike up/down

## Tips for Testing

1. **Start with normal values** to establish baseline
2. **Gradually increase/decrease** to see smooth transitions
3. **Use quick scenarios** for instant dramatic effects
4. **Test multiple sensors** at once for complex scenarios
5. **Watch both dashboard and alert terminal** simultaneously

## Troubleshooting

### Dashboard not updating?
- Check MQTT status is 🟢 Green
- Click "Reconnect" button if red
- Refresh browser

### No alarm beeping?
- Make sure `alert_system.py` is running
- Check if value is actually outside threshold
- Windows: Volume should be up 🔊

### Connection issues?
- Check internet connection (using public MQTT broker)
- Try again after a few seconds
- Restart interactive control

## Fun Test Sequence

Try this sequence for a complete demo:

```
1. Start with scenario 1 (Normal) - establish baseline
2. Wait 5 seconds
3. Run scenario 2 (High temp) - trigger first alarm
4. Wait 10 seconds  
5. Run scenario 5 (High CO2) - trigger second alarm
6. Wait 10 seconds
7. Run scenario 8 (Emergency) - trigger all alarms!
8. Finally, run scenario 1 (Normal) - clear all alarms
```

This creates a complete narrative: normal → warning → danger → EMERGENCY → recovery! 🎬

## Keyboard Shortcuts

- **Ctrl+C**: Stop continuous mode / Exit program
- **Enter**: Confirm selection
- **0**: Return to main menu / Exit

## Next Steps

After testing, you can:
1. Document test results with screenshots
2. Measure response times
3. Test alert acknowledgment
4. Create your own test scenarios

---

**Happy Testing! 🎉**

*Remember: The louder the beep, the more critical the situation!* 🔊
