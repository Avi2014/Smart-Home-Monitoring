"""
Alert System Demo - Shows both alert and clear in sequence
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def demo_alert_system():
    print("\n" + "="*70)
    print(" 🚨 ALERT SYSTEM DEMONSTRATION")
    print("="*70)
    print("\nThis demo will show you:")
    print("  1. HIGH Temperature Alert (35°C)")
    print("  2. Alert Cleared (24°C)")
    print("  3. HIGH Humidity Alert (75%)")
    print("  4. Alert Cleared (50%)")
    print("  5. HIGH CO2 Alert (1500 ppm)")
    print("  6. Alert Cleared (700 ppm)")
    print("\n" + "="*70 + "\n")
    
    input("Press Enter to start demo...\n")
    
    broker = "test.mosquitto.org"
    port = 1883
    
    client = mqtt.Client(
        client_id="alert_demo",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    
    try:
        print("🔌 Connecting to MQTT broker...")
        client.connect(broker, port, 60)
        client.loop_start()
        time.sleep(1)
        print("✅ Connected!\n")
        
        # Demo 1: Temperature Alert
        print("="*70)
        print("DEMO 1: HIGH TEMPERATURE ALERT")
        print("="*70)
        print("\n📤 Sending: Temperature = 35°C (Safe range: 20-28°C)")
        
        msg = {
            'sensor_type': 'temperature',
            'value': 35.0,
            'unit': '°C',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': 100.0,
            'sensor_id': 'DEMO_TEMP',
            'message_count': 1,
            'location': 'Demo'
        }
        client.publish("hostel/room1/temperature", json.dumps(msg), qos=1)
        print("🚨 ALERT SHOULD TRIGGER! (Check alert_system.py terminal)")
        time.sleep(3)
        
        print("\n📤 Sending: Temperature = 24°C (Normal)")
        msg['value'] = 24.0
        msg['message_count'] = 2
        client.publish("hostel/room1/temperature", json.dumps(msg), qos=1)
        print("✅ ALERT SHOULD CLEAR!")
        time.sleep(3)
        
        # Demo 2: Humidity Alert
        print("\n" + "="*70)
        print("DEMO 2: HIGH HUMIDITY ALERT")
        print("="*70)
        print("\n📤 Sending: Humidity = 75% (Safe range: 40-60%)")
        
        msg = {
            'sensor_type': 'humidity',
            'value': 75.0,
            'unit': '%',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': 100.0,
            'sensor_id': 'DEMO_HUM',
            'message_count': 1,
            'location': 'Demo'
        }
        client.publish("hostel/room1/humidity", json.dumps(msg), qos=1)
        print("🚨 ALERT SHOULD TRIGGER!")
        time.sleep(3)
        
        print("\n📤 Sending: Humidity = 50% (Normal)")
        msg['value'] = 50.0
        msg['message_count'] = 2
        client.publish("hostel/room1/humidity", json.dumps(msg), qos=1)
        print("✅ ALERT SHOULD CLEAR!")
        time.sleep(3)
        
        # Demo 3: CO2 Alert
        print("\n" + "="*70)
        print("DEMO 3: HIGH CO2 ALERT")
        print("="*70)
        print("\n📤 Sending: CO2 = 1500 ppm (Safe range: 400-1000 ppm)")
        
        msg = {
            'sensor_type': 'co2',
            'value': 1500.0,
            'unit': 'ppm',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': 100.0,
            'sensor_id': 'DEMO_CO2',
            'message_count': 1,
            'location': 'Demo',
            'air_quality': 'Poor'
        }
        client.publish("hostel/room1/co2", json.dumps(msg), qos=1)
        print("🚨 ALERT SHOULD TRIGGER!")
        time.sleep(3)
        
        print("\n📤 Sending: CO2 = 700 ppm (Normal)")
        msg['value'] = 700.0
        msg['message_count'] = 2
        msg['air_quality'] = 'Good'
        client.publish("hostel/room1/co2", json.dumps(msg), qos=1)
        print("✅ ALERT SHOULD CLEAR!")
        time.sleep(2)
        
        client.loop_stop()
        client.disconnect()
        
        print("\n" + "="*70)
        print(" ✅ DEMO COMPLETE!")
        print("="*70)
        print("\n📊 Summary:")
        print("   - 3 Alerts triggered")
        print("   - 3 Alerts cleared")
        print("   - Total test messages: 6")
        print("\n💡 Check the alert_system.py terminal to see all the alerts!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("\n💡 IMPORTANT: Make sure alert_system.py is running in another terminal!")
    print("   Run this first: python alert_system.py\n")
    
    ready = input("Is alert_system.py running? (yes/no): ")
    if ready.lower() in ['yes', 'y']:
        demo_alert_system()
    else:
        print("\n👉 Please start alert_system.py first, then run this demo again.")
