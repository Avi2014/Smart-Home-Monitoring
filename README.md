# Smart Home Environment Monitoring System - IoT Lab Project

## Project Overview
Real-time IoT dashboard system for monitoring hostel room environmental conditions including:
- 🌡️ **Temperature** monitoring
- 💧 **Humidity** tracking
- 🌫️ **Air Quality (CO2)** measurement
- 💡 **Light levels** detection

## Architecture

```
┌─────────────────────┐
│  Sensor Simulators  │
│  (Python Scripts)   │
│  - Temperature      │
│  - Humidity         │
│  - CO2              │
│  - Light            │
└──────────┬──────────┘
           │ MQTT Protocol
           ▼
┌─────────────────────┐
│   MQTT Broker       │
│   (Mosquitto)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Node-RED         │
│  - Data Processing  │
│  - Rule Engine      │
│  - Alerts           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    InfluxDB         │
│  (Time-Series DB)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Grafana         │
│  Real-time Dashboard│
│  - Gauges           │
│  - Charts           │
│  - Alerts           │
└─────────────────────┘
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Sensors** | Python 3.x | Simulate IoT sensor data |
| **Message Broker** | Mosquitto MQTT | Lightweight messaging protocol |
| **Data Processing** | Node-RED | Visual flow-based programming |
| **Database** | InfluxDB | Time-series data storage |
| **Visualization** | Grafana | Real-time dashboards |
| **Language** | Python, JavaScript | Implementation |

## Features

### ✅ Real-time Monitoring
- Live sensor data updates every 2-5 seconds
- Multiple sensor types per room
- Configurable sampling rates

### 📊 Dashboard Capabilities
- Real-time gauges for current values
- Historical trend charts
- Multi-room comparison
- Alert notifications when thresholds exceeded

### 📈 Metrics to Measure
1. **Latency**: Time from sensor reading to dashboard display
2. **Throughput**: Messages processed per second
3. **Battery Life**: Simulated power consumption based on sampling rate

## Project Structure

```
iot/
├── README.md                          # This file
├── sensors/                           # Sensor simulation scripts
│   ├── temperature_sensor.py
│   ├── humidity_sensor.py
│   ├── co2_sensor.py
│   ├── light_sensor.py
│   └── sensor_config.json
├── mqtt/                              # MQTT configuration
│   └── mosquitto.conf
├── node-red/                          # Node-RED flows
│   └── flows.json
├── grafana/                           # Grafana dashboards
│   └── dashboard.json
├── metrics/                           # Performance measurement scripts
│   ├── latency_test.py
│   ├── throughput_test.py
│   └── battery_simulation.py
├── docs/                              # Documentation
│   ├── installation.md
│   ├── setup_guide.md
│   └── test_results.md
└── requirements.txt                   # Python dependencies
```

## Quick Start

### Prerequisites
- Windows 10/11
- Python 3.8+
- Node.js 16+
- Internet connection for downloads

### Installation Steps
1. Install MQTT Broker (Mosquitto)
2. Install Node-RED
3. Install InfluxDB
4. Install Grafana
5. Install Python dependencies
6. Configure and run sensors
7. Import Node-RED flows
8. Set up Grafana dashboard

### Running the System
```powershell
# Terminal 1: Start MQTT Broker
mosquitto -v

# Terminal 2: Start InfluxDB
influxd

# Terminal 3: Start Node-RED
node-red

# Terminal 4: Start Grafana
grafana-server

# Terminal 5: Run sensor simulators
python sensors/temperature_sensor.py
```

## Expected Outcomes

1. **Real-time Dashboard**: Live visualization of all sensor data
2. **Performance Metrics**:
   - Latency: < 200ms from sensor to dashboard
   - Throughput: 100+ messages/second
   - Battery simulation: Calculated based on transmission frequency
3. **Alert System**: Notifications when values exceed safe thresholds
4. **Historical Data**: 24-hour trend analysis

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
