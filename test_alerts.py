"""
Alert Test Script
Manually sends test data to trigger alerts
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

def send_test_alert(sensor_type, value, description):
    """Send a test message that will trigger an alert"""
    
    # MQTT Configuration
    broker = "test.mosquitto.org"
    port = 1883
    topic = f"hostel/room1/{sensor_type}"
    
    # Create client
    client = mqtt.Client(
        client_id=f"alert_tester_{sensor_type}",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    
    try:
        # Connect
        client.connect(broker, port, 60)
        client.loop_start()
        
        # Create message
        message = {
            'sensor_id': f'TEST_{sensor_type.upper()}_001',
            'sensor_type': sensor_type,
            'value': value,
            'unit': get_unit(sensor_type),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': 100.0,
            'message_count': 1,
            'location': 'Hostel Room 1 - TEST'
        }
        
        # Publish
        print(f"📤 Sending: {description}")
        print(f"   Sensor: {sensor_type}")
        print(f"   Value: {value} {get_unit(sensor_type)}")
        
        client.publish(topic, json.dumps(message), qos=1)
        time.sleep(1)
        
        client.loop_stop()
        client.disconnect()
        
        print("   ✅ Sent!\n")
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")

def get_unit(sensor_type):
    """Get unit for sensor type"""
    units = {
        'temperature': '°C',
        'humidity': '%',
        'co2': 'ppm',
        'light': 'lux'
    }
    return units.get(sensor_type, '')

def run_alert_tests():
    """Run a series of alert tests"""
    
    print("="*70)
    print(" 🧪 ALERT SYSTEM TEST SUITE")
    print("="*70)
    print("\nThis will send test data to trigger alerts.")
    print("Make sure the alert_system.py is running in another terminal!\n")
    print("="*70 + "\n")
    
    input("Press Enter to start tests... (Ctrl+C to cancel)\n")
    
    tests = [
        # Temperature alerts
        {
            'sensor': 'temperature',
            'value': 35.0,
            'description': '🔥 Temperature TOO HIGH (35°C)'
        },
        {
            'sensor': 'temperature',
            'value': 15.0,
            'description': '❄️  Temperature TOO LOW (15°C)'
        },
        {
            'sensor': 'temperature',
            'value': 24.0,
            'description': '✅ Temperature NORMAL (24°C)'
        },
        
        # Humidity alerts
        {
            'sensor': 'humidity',
            'value': 75.0,
            'description': '💧 Humidity TOO HIGH (75%)'
        },
        {
            'sensor': 'humidity',
            'value': 30.0,
            'description': '🏜️  Humidity TOO LOW (30%)'
        },
        {
            'sensor': 'humidity',
            'value': 50.0,
            'description': '✅ Humidity NORMAL (50%)'
        },
        
        # CO2 alerts
        {
            'sensor': 'co2',
            'value': 1500.0,
            'description': '🌫️  CO2 TOO HIGH (1500 ppm)'
        },
        {
            'sensor': 'co2',
            'value': 350.0,
            'description': '🌿 CO2 TOO LOW (350 ppm)'
        },
        {
            'sensor': 'co2',
            'value': 700.0,
            'description': '✅ CO2 NORMAL (700 ppm)'
        },
        
        # Light alerts
        {
            'sensor': 'light',
            'value': 950.0,
            'description': '☀️  Light TOO HIGH (950 lux)'
        },
        {
            'sensor': 'light',
            'value': 50.0,
            'description': '🌙 Light TOO LOW (50 lux)'
        },
        {
            'sensor': 'light',
            'value': 500.0,
            'description': '✅ Light NORMAL (500 lux)'
        }
    ]
    
    print("🧪 Running tests...\n")
    print("-" * 70 + "\n")
    
    for i, test in enumerate(tests, 1):
        print(f"Test {i}/{len(tests)}:")
        send_test_alert(test['sensor'], test['value'], test['description'])
        time.sleep(2)  # Wait between tests
    
    print("-" * 70)
    print("\n✅ All tests completed!")
    print("\nCheck the alert_system.py terminal to see the alerts!")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        run_alert_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests cancelled by user")
