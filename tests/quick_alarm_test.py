"""
Quick Alarm Test - Publish high temperature to trigger alarm
"""
import paho.mqtt.client as mqtt
import json
import ssl
import os
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "95c2f02d61404267847ebc19552f72b0.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "true").lower() == "true"

print("🚨 QUICK ALARM TEST")
print("="*60)
print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
print("Publishing HIGH TEMPERATURE (35°C) to trigger alarm...")
print()

# Create client
client = mqtt.Client(
    client_id="quick_test",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)

# Set credentials if available
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Enable TLS if required
if MQTT_USE_TLS:
    client.tls_set(
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

# Connect
print("⏳ Connecting...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
time.sleep(2)
print("✅ Connected!\n")

# Publish high temperature
message = {
    'sensor_type': 'temperature',
    'sensor_id': 'quick_test',
    'value': 35.0,
    'unit': '°C',
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'battery_level': 100.0
}

client.publish('hostel/room1/temperature', json.dumps(message))
print("✅ Published: Temperature = 35°C (Exceeds 28°C limit)")
print("🔊 Check alert system terminal - should BEEP!")
print()

time.sleep(3)

# Publish normal temperature to clear
message['value'] = 24.0
client.publish('hostel/room1/temperature', json.dumps(message))
print("✅ Published: Temperature = 24°C (Normal)")
print("✅ Alarm should clear")
print()

time.sleep(2)
client.loop_stop()
client.disconnect()

print("="*60)
print("✅ Test complete!")
