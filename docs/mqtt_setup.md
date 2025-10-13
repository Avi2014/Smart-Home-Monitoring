# MQTT Broker Setup Guide

## Step 2: Install and Configure Mosquitto MQTT Broker

### What is MQTT?
MQTT (Message Queuing Telemetry Transport) is a lightweight messaging protocol perfect for IoT devices. It uses a publish-subscribe model where:
- **Publishers** (our sensors) send messages to topics
- **Subscribers** (Node-RED) receive messages from topics
- **Broker** (Mosquitto) routes messages between publishers and subscribers

---

## Installation Options

### Option 1: Install Mosquitto (Recommended for Full System)

#### Download and Install
1. **Download Mosquitto for Windows:**
   - Visit: https://mosquitto.org/download/
   - Choose: "Windows 64-bit" installer
   - Or direct link: https://mosquitto.org/files/binary/win64/mosquitto-2.0.18-install-windows-x64.exe

2. **Install:**
   - Run the installer as Administrator
   - Default location: `C:\Program Files\mosquitto`
   - Install with all default options

3. **Add to PATH:**
   ```powershell
   # Add Mosquitto to system PATH
   $env:Path += ";C:\Program Files\mosquitto"
   # Make it permanent (requires admin)
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\mosquitto", "Machine")
   ```

4. **Create Configuration File:**
   - Location: `C:\Program Files\mosquitto\mosquitto.conf`
   - Content:
   ```
   listener 1883
   allow_anonymous true
   ```

5. **Start Mosquitto:**
   ```powershell
   # Start as a service
   net start mosquitto
   
   # Or run manually in terminal
   mosquitto -v -c "C:\Program Files\mosquitto\mosquitto.conf"
   ```

---

### Option 2: Use Public MQTT Broker (Quick Testing)

For quick testing without installation, use a public broker:

**Popular Public Brokers:**
- `test.mosquitto.org` (port 1883)
- `broker.hivemq.com` (port 1883)
- `mqtt.eclipseprojects.io` (port 1883)

**Update sensor_config.json:**
```json
{
  "mqtt": {
    "broker": "test.mosquitto.org",
    "port": 1883,
    ...
  }
}
```

⚠️ **Warning:** Public brokers are:
- Not secure (anyone can see your data)
- May have connection limits
- Good for testing only, not production

---

### Option 3: Docker (If you have Docker installed)

```powershell
docker run -d -p 1883:1883 --name mosquitto eclipse-mosquitto
```

---

## Testing MQTT Connection

### Test with Python (Easiest)

We'll create simple test scripts:

1. **MQTT Publisher Test:**
   ```powershell
   python mqtt_test_publisher.py
   ```

2. **MQTT Subscriber Test:**
   ```powershell
   python mqtt_test_subscriber.py
   ```

### Test with Mosquitto Command Line

If Mosquitto is installed:

**Terminal 1 - Subscriber:**
```powershell
mosquitto_sub -h localhost -t test/topic -v
```

**Terminal 2 - Publisher:**
```powershell
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT!"
```

---

## Troubleshooting

### Port 1883 Already in Use
```powershell
# Check what's using port 1883
netstat -ano | findstr :1883

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Firewall Blocking
```powershell
# Add firewall rule (run as Administrator)
New-NetFirewallRule -DisplayName "Mosquitto MQTT" -Direction Inbound -Protocol TCP -LocalPort 1883 -Action Allow
```

### Service Won't Start
```powershell
# Check service status
sc query mosquitto

# Restart service
net stop mosquitto
net start mosquitto
```

---

## Next Steps

Once MQTT broker is running:
1. Test connection with test scripts
2. Run sensor simulators
3. Verify messages are being published
4. Set up Node-RED to subscribe to sensor topics

---

## Quick Start Commands

```powershell
# After installation, run in three separate terminals:

# Terminal 1: Start Mosquitto
mosquitto -v

# Terminal 2: Test subscriber
python mqtt_test_subscriber.py

# Terminal 3: Run a sensor
python sensors\temperature_sensor.py
```

You should see messages flowing from sensor → broker → subscriber!
