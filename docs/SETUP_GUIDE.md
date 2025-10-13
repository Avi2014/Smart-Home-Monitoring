# 🏠 Smart Home IoT Monitoring System - Setup Guide

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows/Linux/MacOS
- **Internet Connection**: Required for MQTT broker
- **Git** (optional): For cloning the repository

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Python Dependencies

```powershell
# Create and activate virtual environment (recommended)
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Verify Installation

```powershell
# Test MQTT connection
python tests\mqtt_connection_test.py
```

You should see:
```
✅ Successfully connected to MQTT Broker
✅ Published test message successfully
✅ Received test message successfully
✅ Connection time: X.XX seconds
```

### Step 3: Start the System

**Option A: Start All at Once (Recommended)**
```powershell
.\scripts\start_all.ps1
```

**Option B: Start Individually**

Terminal 1 - Dashboard:
```powershell
streamlit run dashboard.py
```

Terminal 2 - Alert System:
```powershell
python alert_system.py
```

Terminal 3 - Sensor Simulators:
```powershell
python src\sensors\run_all_sensors.py
```

Terminal 4 - Interactive Control (Optional):
```powershell
python interactive_control.py
```

## 🔧 Configuration

### MQTT Broker Setup

Default configuration uses public broker `test.mosquitto.org`.

To use your own broker, edit `src/sensors/sensor_config.json`:

```json
{
  "mqtt": {
    "broker": "your-broker-address.com",
    "port": 1883,
    "client_id_prefix": "iot_sensor"
  }
}
```

### Alert Thresholds

Modify thresholds in `src/sensors/sensor_config.json`:

```json
{
  "sensors": {
    "temperature": {
      "safe_range": [20, 28]
    },
    "humidity": {
      "safe_range": [40, 60]
    }
  }
}
```

## 📊 Accessing the Dashboard

Once started, access the dashboard at:
- **Local**: http://localhost:8501
- **Network**: http://YOUR_IP:8501

## 🧪 Testing

### Quick Test
```powershell
python tests\quick_test.py
```

### Performance Metrics
```powershell
# Test latency
python src\metrics\latency_test.py

# Test throughput
python src\metrics\throughput_test.py

# Simulate battery life
python src\metrics\battery_simulation.py
```

## 🐛 Troubleshooting

### Dashboard Not Loading?
- Check if port 8501 is available
- Restart: `Ctrl+C` and run again

### No Sensor Data?
- Verify MQTT broker connection
- Check internet connection
- Restart sensor simulators

### No Alert Beeps?
- Ensure volume is turned up
- Verify `winsound` works: `python -c "import winsound; winsound.Beep(1000, 500)"`
- Check alert thresholds are configured correctly

### Import Errors?
- Ensure virtual environment is activated
- Reinstall: `pip install -r requirements.txt --force-reinstall`

## 📱 Next Steps

- Read [USER_GUIDE.md](USER_GUIDE.md) for detailed usage
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options
- Customize sensor parameters in configuration files

## 💡 Tips

- Use `interactive_control.py` for manual testing
- Keep all terminals visible to monitor system behavior
- Check alert system terminal for threshold violations
- Dashboard auto-refreshes every 2 seconds

## 🆘 Support

For issues or questions:
1. Check documentation in `docs/` folder
2. Review troubleshooting section above
3. Check configuration files for errors
4. Verify all dependencies are installed

---

**🎉 Setup Complete! Your IoT monitoring system is ready!**
