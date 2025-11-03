# 🏠 Smart Home IoT Monitoring System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-red)](https://streamlit.io/)
[![MQTT](https://img.shields.io/badge/MQTT-Paho-green)](https://www.eclipse.org/paho/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Real-time IoT environmental monitoring system for smart homes with interactive dashboard, alert system, and sensor simulators.

## 🚀 Quick Start - One Simple Command!

```powershell
.\start.ps1
```

**That's it!** The entire system launches automatically with all components running.

- 📊 **Dashboard** → http://localhost:8501
- 🔔 **Alert System** → Monitoring thresholds
- 📡 **Sensors** → Generating realistic data
- 🎮 **Control Panel** → Manual testing

---

## 🎯 Features

- 📊 **Real-Time Dashboard** - Beautiful Streamlit web interface with live gauges and charts
- 🚨 **Alert System** - Threshold monitoring with audio alarms
- � **Sensor Simulators** - 4 realistic IoT sensors (Temperature, Humidity, CO2, Light)
- 🎮 **Interactive Control** - Manual sensor control for testing
- 📈 **Performance Metrics** - Latency, throughput, and battery life analysis
- 🌐 **MQTT Communication** - Industry-standard IoT protocol
- � **Audio Alerts** - Beep notifications when thresholds exceeded

## 🏗️ Architecture

```
┌─────────────────────┐
│  Sensor Simulators  │
│  - Temperature      │
│  - Humidity         │
│  - CO2 (Air Quality)│
│  - Light Level      │
└──────────┬──────────┘
           │ MQTT (Publish)
           ▼
┌─────────────────────┐
│   MQTT Broker       │
│ test.mosquitto.org  │
└──────────┬──────────┘
           │ MQTT (Subscribe)
           ▼
     ┌─────┴──────┐
     │            │
     ▼            ▼
┌─────────┐  ┌──────────┐
│Dashboard│  │  Alert   │
│(Streamlit)│  │ System   │
│- Gauges │  │- Monitor │
│- Charts │  │- Beep 🔊 │
└─────────┘  └──────────┘
```

## Technology Stack

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Dashboard** | Streamlit 1.50.0 | Real-time web interface |
| **Visualization** | Plotly 6.3.1 | Interactive charts & gauges |
| **Message Broker** | MQTT (Paho 2.1.0) | IoT communication protocol |
| **Sensors** | Python 3.8+ | Realistic sensor simulators |
| **Alert System** | winsound | Audio notifications |
| **Data Processing** | Pandas, NumPy | Real-time data analysis |
| **Language** | Python | Full implementation |

## 📁 Project Structure

```
iot/
├── src/                          # Source code
│   ├── sensors/                  # Sensor simulators
│   │   ├── temperature_sensor.py
│   │   ├── humidity_sensor.py
│   │   ├── co2_sensor.py
│   │   ├── light_sensor.py
│   │   ├── run_all_sensors.py
│   │   └── sensor_config.json
│   └── metrics/                  # Performance analysis
│       ├── latency_test.py
│       ├── throughput_test.py
│       └── battery_simulation.py
│
├── tests/                        # Test scripts
│   ├── test_scenarios.py         # Consolidated test suite
│   ├── mqtt_connection_test.py   # Connection verification
│   └── quick_test.py             # Quick alarm test
│
├── scripts/                      # Utility scripts
│   └── start_all.ps1             # One-click startup (Windows)
│
├── docs/                         # Documentation
│   ├── SETUP_GUIDE.md            # Installation & setup
│   ├── USER_GUIDE.md             # Complete usage guide
│   └── DEPLOYMENT.md             # Deployment options
│
├── dashboard.py                  # Main Streamlit dashboard
├── alert_system.py               # Threshold monitoring & alerts
├── interactive_control.py        # Manual sensor control panel
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git exclusions
└── README.md                     # This file
```

## 🚀 Quick Start

### 5-Minute Setup

```powershell
# 1. Clone repository
git clone https://github.com/Avi2014/Smart-Home-Monitoring.git
cd Smart-Home-Monitoring

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start everything (one command!)
.\scripts\start_all.ps1
```

This will open 4 terminals:
- 🌐 **Dashboard** - http://localhost:8501
- 🚨 **Alert System** - Monitoring thresholds
- 📊 **Sensors** - Publishing data
- 🎮 **Interactive Control** - Manual testing

### Prerequisites
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Internet connection** - For MQTT broker (test.mosquitto.org)
- **Windows OS** - For audio alerts (winsound)

## 📋 Usage

### Dashboard
Access the live dashboard at http://localhost:8501
- **Status Bar** - Connection status and last update time
- **Gauges** - Current sensor readings with color-coded thresholds
- **Trend Charts** - 10-minute historical data
- **Sidebar** - System information and statistics

### Alert System
Monitors thresholds 24/7:
- 🌡️ Temperature: 20-28°C (safe range)
- 💧 Humidity: 40-60% (safe range)
- 🌫️ CO2: 400-1000 ppm (safe range)
- 💡 Light: 200-800 lux (safe range)

When exceeded, triggers:
- 🔊 Beep sound (1000Hz, 500ms)
- 🚨 Console alert message
- ⚠️ Visual warning in dashboard

### Interactive Control
Test the system manually:
```powershell
python interactive_control.py
```
9 pre-configured scenarios:
1. Normal conditions
2. High temperature (35°C)
3. Low temperature (15°C)
4. High humidity (80%)
5. Low humidity (25%)
6. High CO2 (1500 ppm)
7. Bright light (950 lux)
8. Low light (50 lux)
9. Emergency (all critical)

### Run Tests
```powershell
# Full test suite with 8 scenarios
python tests\test_scenarios.py

# Quick connection test
python tests\mqtt_connection_test.py

# Single alarm test
python tests\quick_test.py
```

### Performance Metrics
```powershell
# Measure end-to-end latency
python src\metrics\latency_test.py

# Calculate throughput
python src\metrics\throughput_test.py

# Simulate battery life
python src\metrics\battery_simulation.py
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation, configuration, troubleshooting
- **[User Guide](docs/USER_GUIDE.md)** - Complete feature documentation (400+ lines)
- **[Deployment Guide](docs/DEPLOYMENT.md)** - 5 deployment options (Local, Cloud, Docker, VM, Private MQTT)

## 🎯 Features

### Real-Time Dashboard
- ✅ Live sensor data updates every 2 seconds
- ✅ Beautiful gauges with color-coded zones
- ✅ Interactive trend charts (10-minute history)
- ✅ Thread-safe data handling
- ✅ Auto-refresh with connection monitoring

### Alert System
- ✅ Threshold monitoring for all 4 sensors
- ✅ Audio alerts (beep sounds)
- ✅ Visual console notifications
- ✅ Automatic alert clearing when back to normal
- ✅ Configurable thresholds

### Sensor Simulators
- ✅ Realistic data patterns with natural variation
- ✅ Temperature: Gradual changes, day/night cycles
- ✅ Humidity: Correlated with temperature
- ✅ CO2: People occupancy simulation
- ✅ Light: Daily patterns with smooth transitions

### Performance Metrics
- ✅ **Latency Test**: Measures round-trip time (typically <100ms)
- ✅ **Throughput Test**: Messages/second capability
- ✅ **Battery Simulation**: 4 scenarios showing power consumption

## 🔧 Configuration

### MQTT Settings
Edit `src/sensors/sensor_config.json`:
```json
{
  "mqtt": {
    "broker": "test.mosquitto.org",
    "port": 1883,
    "topics": {
      "temperature": "hostel/room1/temperature",
      "humidity": "hostel/room1/humidity",
      "co2": "hostel/room1/co2",
      "light": "hostel/room1/light"
    }
  }
}
```

### Threshold Customization
Modify ranges in `alert_system.py`:
```python
self.thresholds = {
    'temperature': (20, 28),  # °C
    'humidity': (40, 60),     # %
    'co2': (400, 1000),       # ppm
    'light': (200, 800)       # lux
}
```

## 🚀 Deployment

Multiple deployment options available:

1. **Local Development** - Use `start_all.ps1` script
2. **Streamlit Cloud** - Free hosting for dashboard
3. **Docker** - Containerized deployment with docker-compose
4. **Cloud VM** - AWS/Azure/GCP with PM2 + nginx
5. **Private MQTT** - Self-hosted Mosquitto broker

See **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** for complete instructions.

## 📊 Expected Performance

| Metric | Target | Typical |
|--------|--------|---------|
| **Latency** | <200ms | 50-100ms |
| **Throughput** | 100+ msg/s | 150-200 msg/s |
| **Dashboard Update** | 2s refresh | Real-time |
| **Alert Response** | <1s | Immediate |
| **Battery Life** | Configurable | 30-180 days (simulated) |

## 🤝 Contributing

This is an educational IoT lab project. Contributions welcome!

## 📄 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- **MQTT Broker**: test.mosquitto.org (Eclipse Mosquitto)
- **Dashboard**: Streamlit framework
- **Visualization**: Plotly library
- **IoT Protocol**: MQTT (Message Queuing Telemetry Transport)

---

**Built for IoT Lab Project** - Real-time Environmental Monitoring System


## Lab Report Components

- [ ] System architecture diagram
- [ ] Implementation details
- [ ] Performance metrics results
- [ ] Dashboard screenshots
- [ ] Latency analysis
- [ ] Throughput analysis
- [ ] Battery life optimization analysis
- [ ] Challenges and solutions
- [ ] Future improvements

## Author
Lab Work - IoT Mobile Apps Development
Date: October 2025

## License
Educational Project
