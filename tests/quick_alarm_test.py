"""
Quick Alarm Test - Publish high temperature to trigger alarm
"""
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

print("🚨 QUICK ALARM TEST")
print("="*60)
print("Publishing HIGH TEMPERATURE (35°C) to trigger alarm...")
print()

# Create client
client = mqtt.Client(
    client_id="quick_test",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

# Connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
time.sleep(1)

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
