"""
Test script to verify alarm system is working
Publishes test values that should trigger alarms
"""
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

def test_alarm():
    """Test alarm system by publishing alert-triggering values"""
    
    # Create MQTT client
    client = mqtt.Client(
        client_id="alarm_tester",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    
    print("="*70)
    print("🧪 ALARM SYSTEM TEST SUITE")
    print("="*70)
    print()
    print("🔌 Connecting to MQTT broker...")
    
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    time.sleep(2)
    
    print("✅ Connected!")
    print()
    print("🚨 Publishing test values to trigger alarms...")
    print("="*70)
    
    # Test 1: High Temperature (should trigger alarm)
    print("\n1️⃣ Test: HIGH TEMPERATURE (35°C > 28°C limit)")
    message = {
        'sensor_type': 'temperature',
        'sensor_id': 'temp_test',
        'value': 35.0,
        'unit': '°C',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/temperature', json.dumps(message))
    print("   ✅ Published temperature: 35°C")
    print("   ⏳ Waiting 3 seconds... (Check alert_system terminal for BEEP!)")
    time.sleep(3)
    
    # Test 2: Low Temperature (should trigger alarm)
    print("\n2️⃣ Test: LOW TEMPERATURE (15°C < 20°C limit)")
    message['value'] = 15.0
    client.publish('hostel/room1/temperature', json.dumps(message))
    print("   ✅ Published temperature: 15°C")
    print("   ⏳ Waiting 3 seconds...")
    time.sleep(3)
    
    # Test 3: High Humidity (should trigger alarm)
    print("\n3️⃣ Test: HIGH HUMIDITY (85% > 60% limit)")
    message = {
        'sensor_type': 'humidity',
        'sensor_id': 'humidity_test',
        'value': 85.0,
        'unit': '%',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/humidity', json.dumps(message))
    print("   ✅ Published humidity: 85%")
    print("   ⏳ Waiting 3 seconds...")
    time.sleep(3)
    
    # Test 4: High CO2 (should trigger alarm)
    print("\n4️⃣ Test: HIGH CO2 (1500 ppm > 1000 ppm limit)")
    message = {
        'sensor_type': 'co2',
        'sensor_id': 'co2_test',
        'value': 1500.0,
        'unit': 'ppm',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/co2', json.dumps(message))
    print("   ✅ Published CO2: 1500 ppm")
    print("   ⏳ Waiting 3 seconds...")
    time.sleep(3)
    
    # Test 5: Low Light (should trigger alarm)
    print("\n5️⃣ Test: LOW LIGHT (50 lux < 200 lux limit)")
    message = {
        'sensor_type': 'light',
        'sensor_id': 'light_test',
        'value': 50.0,
        'unit': 'lux',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/light', json.dumps(message))
    print("   ✅ Published light: 50 lux")
    print("   ⏳ Waiting 3 seconds...")
    time.sleep(3)
    
    # Test 6: Return to Normal (should clear all alarms)
    print("\n6️⃣ Test: NORMAL VALUES (should clear all alarms)")
    
    # Normal temperature
    message = {
        'sensor_type': 'temperature',
        'sensor_id': 'temp_test',
        'value': 24.0,
        'unit': '°C',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/temperature', json.dumps(message))
    print("   ✅ Published temperature: 24°C (NORMAL)")
    time.sleep(1)
    
    # Normal humidity
    message = {
        'sensor_type': 'humidity',
        'sensor_id': 'humidity_test',
        'value': 50.0,
        'unit': '%',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/humidity', json.dumps(message))
    print("   ✅ Published humidity: 50% (NORMAL)")
    time.sleep(1)
    
    # Normal CO2
    message = {
        'sensor_type': 'co2',
        'sensor_id': 'co2_test',
        'value': 600.0,
        'unit': 'ppm',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/co2', json.dumps(message))
    print("   ✅ Published CO2: 600 ppm (NORMAL)")
    time.sleep(1)
    
    # Normal light
    message = {
        'sensor_type': 'light',
        'sensor_id': 'light_test',
        'value': 400.0,
        'unit': 'lux',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'battery_level': 100.0,
        'location': 'hostel/room1'
    }
    client.publish('hostel/room1/light', json.dumps(message))
    print("   ✅ Published light: 400 lux (NORMAL)")
    time.sleep(2)
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE!")
    print("="*70)
    print()
    print("📋 Summary:")
    print("   - 5 alarms should have been triggered")
    print("   - 4 alarms should have been cleared")
    print("   - You should have heard 5 BEEP sounds 🔊")
    print()
    print("💡 Check the alert_system_fixed.py terminal to verify!")
    print()
    
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Make sure alert_system_fixed.py is running!")
    print("   Open another terminal and run: python alert_system_fixed.py")
    print()
    response = input("Is alert_system_fixed.py running? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        test_alarm()
    else:
        print("\n❌ Please start alert_system_fixed.py first, then run this test again.")
