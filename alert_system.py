"""
Fixed IoT Alert System with Better Debugging
Monitors sensor data and triggers alarms when thresholds are exceeded
"""
import paho.mqtt.client as mqtt
import json
import os
import sys
import ssl
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MQTT Configuration - Load from environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER", "95c2f02d61404267847ebc19552f72b0.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "true").lower() == "true"

MQTT_TOPICS = [
    os.getenv("MQTT_TOPIC_TEMPERATURE", "hostel/room1/temperature"),
    os.getenv("MQTT_TOPIC_HUMIDITY", "hostel/room1/humidity"),
    os.getenv("MQTT_TOPIC_CO2", "hostel/room1/co2"),
    os.getenv("MQTT_TOPIC_LIGHT", "hostel/room1/light")
]

# Validate credentials
if not MQTT_BROKER or not MQTT_USERNAME or not MQTT_PASSWORD:
    print("❌ Error: MQTT credentials not found!")
    print("Please create a .env file with:")
    print("  MQTT_BROKER=your-broker-url")
    print("  MQTT_PORT=8883")
    print("  MQTT_USERNAME=your-username")
    print("  MQTT_PASSWORD=your-password")
    print("  MQTT_USE_TLS=true")
    sys.exit(1)

# Alert Thresholds
THRESHOLDS = {
    'temperature': {'min': 20, 'max': 28, 'unit': '°C'},
    'humidity': {'min': 40, 'max': 60, 'unit': '%'},
    'co2': {'min': None, 'max': 1000, 'unit': 'ppm'},
    'light': {'min': 200, 'max': 800, 'unit': 'lux'}
}

class AlertSystem:
    def __init__(self):
        self.active_alerts = {}
        self.alert_count = 0
        self.message_count = 0
        
    def beep(self):
        """Play system beep sound"""
        try:
            # Windows beep
            import winsound
            winsound.Beep(1000, 500)  # 1000Hz for 500ms - louder and longer
            print("🔊 BEEP!")
        except Exception as e:
            # Fallback
            print(f'🔊 BEEP! (Sound error: {e})')
            print('\a')  # ASCII bell character
    
    def check_thresholds(self, sensor_type, value):
        """Check if value exceeds thresholds"""
        if sensor_type not in THRESHOLDS:
            return None
        
        threshold = THRESHOLDS[sensor_type]
        
        # Check minimum threshold
        if threshold['min'] is not None and value < threshold['min']:
            return {
                'type': 'LOW',
                'threshold': threshold['min'],
                'value': value,
                'unit': threshold['unit']
            }
        
        # Check maximum threshold
        if threshold['max'] is not None and value > threshold['max']:
            return {
                'type': 'HIGH',
                'threshold': threshold['max'],
                'value': value,
                'unit': threshold['unit']
            }
        
        return None
    
    def trigger_alert(self, sensor_type, alert_info):
        """Trigger an alert"""
        alert_key = f"{sensor_type}_{alert_info['type']}"
        
        # Only trigger if not already active
        if alert_key not in self.active_alerts:
            self.active_alerts[alert_key] = True
            self.alert_count += 1
            
            # Beep sound
            self.beep()
            
            # Visual alert
            emoji = {'temperature': '🌡️', 'humidity': '💧', 'co2': '🌫️', 'light': '💡'}.get(sensor_type, '📊')
            
            print(f"\n{'='*70}")
            print(f"🚨🚨🚨 ALERT #{self.alert_count} - {alert_info['type']} {sensor_type.upper()} 🚨🚨🚨")
            print(f"{'='*70}")
            print(f"{emoji} Current Value: {alert_info['value']}{alert_info['unit']}")
            print(f"⚠️  Threshold Limit: {alert_info['threshold']}{alert_info['unit']}")
            print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*70}\n")
    
    def clear_alert(self, sensor_type, value, unit):
        """Clear alerts when value returns to normal"""
        cleared = []
        
        for alert_key in list(self.active_alerts.keys()):
            if alert_key.startswith(sensor_type):
                del self.active_alerts[alert_key]
                cleared.append(alert_key)
        
        if cleared:
            emoji = {'temperature': '🌡️', 'humidity': '💧', 'co2': '🌫️', 'light': '💡'}.get(sensor_type, '📊')
            print(f"\n{'='*70}")
            print(f"✅ ALERT CLEARED - {sensor_type.upper()}")
            print(f"{'='*70}")
            print(f"{emoji} Current Value: {value}{unit} (Back to normal)")
            print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*70}\n")

# Global alert system instance
alert_system = AlertSystem()

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print(f"✅ Connected to MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
            print(f"📡 Subscribed to: {topic}")
        print(f"\n🎯 Alert System Active - Listening for sensor data...\n")
    else:
        error_messages = {
            1: "Connection refused - incorrect protocol version",
            2: "Connection refused - invalid client identifier",
            3: "Connection refused - server unavailable",
            4: "Connection refused - bad username or password",
            5: "Connection refused - not authorized"
        }
        print(f"❌ Connection failed with code {rc}: {error_messages.get(rc, 'Unknown error')}")
        sys.exit(1)

def on_disconnect(client, userdata, disconnect_flags, rc, properties=None):
    """Callback when disconnected"""
    if rc != 0:
        print(f"⚠️ Unexpected disconnection (code: {rc}). Attempting to reconnect...")

def on_message(client, userdata, msg):
    """Callback when message received"""
    try:
        alert_system.message_count += 1
        data = json.loads(msg.payload.decode())
        
        sensor_type = data.get('sensor_type')
        value = data.get('value')
        unit = data.get('unit', '')
        
        # Show incoming data for debugging
        print(f"📥 [{alert_system.message_count}] Received: {sensor_type} = {value}{unit}")
        
        # Check thresholds
        alert_info = alert_system.check_thresholds(sensor_type, value)
        
        if alert_info:
            # Alert triggered
            alert_system.trigger_alert(sensor_type, alert_info)
        else:
            # Value normal - clear any active alerts
            alert_system.clear_alert(sensor_type, value, unit)
    
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def main():
    """Main function"""
    print(f"\n{'='*70}")
    print(f"🚨 IoT ALERT SYSTEM - Starting...")
    print(f"{'='*70}\n")
    
    print(f"📋 MQTT Configuration:")
    print(f"   Broker: {MQTT_BROKER}")
    print(f"   Port: {MQTT_PORT}")
    print(f"   TLS: {'✅ Enabled' if MQTT_USE_TLS else '❌ Disabled'}")
    print(f"   Auth: {'✅ Enabled' if MQTT_USERNAME else '❌ Disabled'}\n")
    
    print(f"📋 Alert Thresholds:")
    for sensor, threshold in THRESHOLDS.items():
        emoji = {'temperature': '🌡️', 'humidity': '💧', 'co2': '🌫️', 'light': '💡'}.get(sensor, '📊')
        min_val = f"{threshold['min']}{threshold['unit']}" if threshold['min'] else "None"
        max_val = f"{threshold['max']}{threshold['unit']}" if threshold['max'] else "None"
        print(f"   {emoji} {sensor.title()}: {min_val} - {max_val}")
    print()
    
    # Create MQTT client
    client = mqtt.Client(
        client_id="alert_system",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        protocol=mqtt.MQTTv311
    )
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Set username and password if provided
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # Enable TLS if required (for HiveMQ Cloud)
    if MQTT_USE_TLS:
        client.tls_set(
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
    
    # Connect and start
    try:
        print(f"🔌 Connecting to MQTT broker...\n")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print(f"\n\n⏸️  Alert system stopped by user")
        print(f"📊 Final Stats: {alert_system.message_count} messages, "
              f"{alert_system.alert_count} total alerts\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()