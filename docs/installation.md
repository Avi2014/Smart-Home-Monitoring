# Installation Guide - Smart Home IoT Monitoring System

## Prerequisites Check

Before starting, ensure you have:
- ✅ Windows 10 or 11
- ✅ Administrator access
- ✅ At least 2GB free disk space
- ✅ Internet connection

## Step-by-Step Installation

### 1. Install Python 3.x

1. Download Python from: https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:
```powershell
python --version
pip --version
```

### 2. Install Node.js

1. Download from: https://nodejs.org/ (LTS version)
2. Run installer with default settings
3. Verify installation:
```powershell
node --version
npm --version
```

### 3. Install Mosquitto MQTT Broker

1. Download from: https://mosquitto.org/download/
2. Choose "Windows 64-bit" installer
3. Install to default location: `C:\Program Files\mosquitto`
4. Add to Windows PATH:
   - Open System Properties → Environment Variables
   - Add `C:\Program Files\mosquitto` to PATH
5. Verify installation:
```powershell
mosquitto -h
```

### 4. Install Node-RED

```powershell
npm install -g --unsafe-perm node-red
```

Verify installation:
```powershell
node-red --help
```

### 5. Install InfluxDB

1. Download from: https://portal.influxdata.com/downloads/
2. Choose "InfluxDB v2.x" for Windows
3. Extract to `C:\influxdb`
4. Create data directory: `C:\influxdb\data`

### 6. Install Grafana

1. Download from: https://grafana.com/grafana/download?platform=windows
2. Choose "Windows Installer"
3. Install with default settings
4. Service will start automatically

### 7. Install Python Dependencies

Navigate to project directory:
```powershell
cd C:\Users\avina\OneDrive\Desktop\iot
pip install -r requirements.txt
```

### 8. Install Node-RED Nodes

Start Node-RED once:
```powershell
node-red
```

Open browser: http://localhost:1880

Install these nodes via Palette Manager (Menu → Manage palette → Install):
- `node-red-contrib-influxdb`
- `node-red-dashboard`
- `node-red-contrib-mqtt-broker`

## Configuration

### Configure Mosquitto

Create/edit `C:\Program Files\mosquitto\mosquitto.conf`:
```
listener 1883
allow_anonymous true
```

### Configure InfluxDB

First run:
```powershell
cd C:\influxdb
.\influxd.exe
```

Open browser: http://localhost:8086
- Create initial user: `admin / password123`
- Organization: `iot-lab`
- Bucket: `sensor-data`
- Save the API token generated

### Configure Grafana

Open browser: http://localhost:3000
- Default login: `admin / admin`
- Change password when prompted
- Add data source: InfluxDB
  - URL: `http://localhost:8086`
  - Organization: `iot-lab`
  - Token: (paste your token)
  - Bucket: `sensor-data`

## Verify Installation

Run all services:

```powershell
# Terminal 1
mosquitto -v

# Terminal 2
cd C:\influxdb
.\influxd.exe

# Terminal 3
node-red

# Terminal 4
cd C:\Program Files\GrafanaLabs\grafana\bin
.\grafana-server.exe
```

Access UIs:
- Node-RED: http://localhost:1880
- InfluxDB: http://localhost:8086
- Grafana: http://localhost:3000

## Troubleshooting

### Mosquitto won't start
- Check if port 1883 is free: `netstat -ano | findstr :1883`
- Run as Administrator

### Node-RED installation fails
- Clear npm cache: `npm cache clean --force`
- Try: `npm install -g node-red --verbose`

### Python dependencies fail
- Update pip: `python -m pip install --upgrade pip`
- Install Visual C++ Build Tools if needed

### InfluxDB connection refused
- Ensure influxd.exe is running
- Check firewall settings for port 8086

## Next Steps

Once all installations are complete, proceed to:
- [Setup Guide](setup_guide.md) - Configure the system
- Run sensor simulators
- Import Node-RED flows
- Create Grafana dashboard

## Support

If you encounter issues:
1. Check service is running: Task Manager → Services
2. Review error logs in respective application folders
3. Ensure no port conflicts (1880, 1883, 8086, 3000)
