"""
Quick Alert Demo
Sends one high-temperature alert immediately
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

print("\n" + "="*70)
print(" 🔥 QUICK ALERT TEST - High Temperature")
print("="*70)
print("\nThis will send a HIGH TEMPERATURE alert to test the system.")
print("Make sure alert_system.py is running in another terminal!\n")

input("Press Enter to send alert...\n")

# MQTT Configuration
broker = "test.mosquitto.org"
port = 1883
topic = "hostel/room1/temperature"

# Create client
client = mqtt.Client(
    client_id="quick_test",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

try:
    print("🔌 Connecting to MQTT broker...")
    client.connect(broker, port, 60)
    client.loop_start()
    time.sleep(1)
    
    # Send HIGH temperature (will trigger alert)
    print("📤 Sending HIGH temperature: 35°C (Safe range: 20-28°C)")
    message = {
        'sensor_id': 'TEMP_TEST_001',
        'sensor_type': 'temperature',
        'value': 35.0,  # Way above safe max of 28°C
        'unit': '°C',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'message_count': 1,
        'location': 'Hostel Room 1 - ALERT TEST'
    }
    
    client.publish(topic, json.dumps(message), qos=1)
    print("✅ Alert sent!")
    print("\n🚨 Check the alert_system.py terminal - you should see:")
    print("   - Alert message")
    print("   - Beep sound")
    print("   - Temperature: 35°C (TOO HIGH)")
    
    time.sleep(2)
    
    # Send NORMAL temperature (will clear alert)
    print("\n📤 Sending NORMAL temperature: 24°C")
    message['value'] = 24.0
    message['message_count'] = 2
    message['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    
    client.publish(topic, json.dumps(message), qos=1)
    print("✅ Normal value sent!")
    print("\n✅ Check alert_system.py - alert should now CLEAR!")
    
    time.sleep(1)
    
    client.loop_stop()
    client.disconnect()
    
    print("\n" + "="*70)
    print(" ✅ Test Complete!")
    print("="*70 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Make sure you're connected to internet!")
