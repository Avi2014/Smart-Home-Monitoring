"""
Interactive Sensor Control Panel
Manually control sensor values to test dashboard and alert system
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time
import os

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

# Sensor Thresholds (for reference)
THRESHOLDS = {
    'temperature': {'min': 20, 'max': 28, 'unit': '°C'},
    'humidity': {'min': 40, 'max': 60, 'unit': '%'},
    'co2': {'min': 400, 'max': 1000, 'unit': 'ppm'},
    'light': {'min': 200, 'max': 800, 'unit': 'lux'}
}

class InteractiveSensorControl:
    def __init__(self):
        self.client = mqtt.Client(
            client_id="interactive_controller",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.on_connect = self.on_connect
        self.connected = False
        
    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            print("✅ Connected to MQTT Broker")
        else:
            print(f"❌ Connection failed with code {rc}")
    
    def connect(self):
        """Connect to MQTT broker"""
        print(f"🔌 Connecting to {MQTT_BROKER}...")
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()
        time.sleep(1)
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish_sensor_data(self, sensor_type, value):
        """Publish sensor data to MQTT"""
        topic = f"hostel/room1/{sensor_type}"
        
        message = {
            'sensor_id': f'{sensor_type.upper()}_MANUAL',
            'sensor_type': sensor_type,
            'value': value,
            'unit': THRESHOLDS[sensor_type]['unit'],
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': 100.0,
            'message_count': 1,
            'location': 'Hostel Room 1',
            'mode': 'manual'
        }
        
        payload = json.dumps(message)
        result = self.client.publish(topic, payload)
        
        # Check if value is out of threshold
        threshold = THRESHOLDS[sensor_type]
        if value < threshold['min'] or value > threshold['max']:
            status = "🚨 ALERT!"
        else:
            status = "✅ Normal"
        
        print(f"📤 Published: {sensor_type.capitalize()} = {value}{threshold['unit']} {status}")
        return result
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display interactive menu"""
        self.clear_screen()
        print("=" * 70)
        print("🎛️  INTERACTIVE SENSOR CONTROL PANEL")
        print("=" * 70)
        print()
        print("📊 Current Thresholds:")
        print(f"  🌡️  Temperature:  {THRESHOLDS['temperature']['min']}-{THRESHOLDS['temperature']['max']}°C")
        print(f"  💧 Humidity:     {THRESHOLDS['humidity']['min']}-{THRESHOLDS['humidity']['max']}%")
        print(f"  🌫️  CO2:          {THRESHOLDS['co2']['min']}-{THRESHOLDS['co2']['max']} ppm")
        print(f"  💡 Light:        {THRESHOLDS['light']['min']}-{THRESHOLDS['light']['max']} lux")
        print()
        print("=" * 70)
        print("Select Sensor to Control:")
        print("  1️⃣  Temperature")
        print("  2️⃣  Humidity")
        print("  3️⃣  CO2")
        print("  4️⃣  Light")
        print()
        print("  5️⃣  Quick Test Scenarios")
        print("  6️⃣  Continuous Mode (Keep sending values)")
        print("  0️⃣  Exit")
        print("=" * 70)
        print()
    
    def get_sensor_value(self, sensor_type):
        """Get value input from user"""
        threshold = THRESHOLDS[sensor_type]
        print()
        print(f"🎯 {sensor_type.capitalize()} Control")
        print(f"   Safe range: {threshold['min']}-{threshold['max']}{threshold['unit']}")
        print(f"   Below {threshold['min']}{threshold['unit']} or above {threshold['max']}{threshold['unit']} will trigger alarm!")
        print()
        
        while True:
            try:
                value_str = input(f"Enter value ({threshold['unit']}): ")
                if value_str.lower() in ['q', 'quit', 'exit']:
                    return None
                value = float(value_str)
                return value
            except ValueError:
                print("❌ Invalid input! Please enter a number.")
    
    def quick_scenarios(self):
        """Run quick test scenarios"""
        self.clear_screen()
        print("=" * 70)
        print("🚀 QUICK TEST SCENARIOS")
        print("=" * 70)
        print()
        print("  1️⃣  Normal conditions (all sensors in safe range)")
        print("  2️⃣  High temperature alert (35°C)")
        print("  3️⃣  Low temperature alert (15°C)")
        print("  4️⃣  High humidity alert (85%)")
        print("  5️⃣  High CO2 alert (1500 ppm)")
        print("  6️⃣  Low light alert (50 lux)")
        print("  7️⃣  Multiple alerts (temperature + CO2 high)")
        print("  8️⃣  Emergency scenario (all sensors critical)")
        print("  0️⃣  Back to main menu")
        print()
        print("=" * 70)
        
        choice = input("\nSelect scenario: ")
        
        scenarios = {
            '1': [('temperature', 24), ('humidity', 50), ('co2', 600), ('light', 400)],
            '2': [('temperature', 35)],
            '3': [('temperature', 15)],
            '4': [('humidity', 85)],
            '5': [('co2', 1500)],
            '6': [('light', 50)],
            '7': [('temperature', 32), ('co2', 1400)],
            '8': [('temperature', 38), ('humidity', 90), ('co2', 2000), ('light', 10)]
        }
        
        if choice in scenarios:
            print(f"\n🚀 Running scenario {choice}...")
            print()
            for sensor_type, value in scenarios[choice]:
                self.publish_sensor_data(sensor_type, value)
                time.sleep(0.5)
            print()
            print("✅ Scenario complete! Check dashboard and alert system.")
            input("\nPress Enter to continue...")
    
    def continuous_mode(self):
        """Continuous mode - keep sending values"""
        self.clear_screen()
        print("=" * 70)
        print("🔄 CONTINUOUS MODE")
        print("=" * 70)
        print()
        print("Select sensor:")
        print("  1. Temperature")
        print("  2. Humidity")
        print("  3. CO2")
        print("  4. Light")
        print()
        
        sensor_map = {
            '1': 'temperature',
            '2': 'humidity',
            '3': 'co2',
            '4': 'light'
        }
        
        choice = input("Select sensor: ")
        if choice not in sensor_map:
            return
        
        sensor_type = sensor_map[choice]
        
        try:
            interval = float(input("Enter interval in seconds (e.g., 2): "))
        except ValueError:
            interval = 2
        
        print()
        print(f"🔄 Starting continuous mode for {sensor_type}")
        print(f"📊 Sending data every {interval} seconds")
        print("⌨️  Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                value = self.get_sensor_value(sensor_type)
                if value is None:
                    break
                
                self.publish_sensor_data(sensor_type, value)
                print(f"⏳ Waiting {interval} seconds... (Ctrl+C to stop)")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Continuous mode stopped")
            input("Press Enter to continue...")
    
    def run(self):
        """Main control loop"""
        self.connect()
        
        if not self.connected:
            print("❌ Failed to connect to MQTT broker. Exiting...")
            return
        
        sensor_map = {
            '1': 'temperature',
            '2': 'humidity',
            '3': 'co2',
            '4': 'light'
        }
        
        try:
            while True:
                self.display_menu()
                choice = input("Enter your choice: ")
                
                if choice == '0':
                    print("\n👋 Exiting...")
                    break
                elif choice == '5':
                    self.quick_scenarios()
                elif choice == '6':
                    self.continuous_mode()
                elif choice in sensor_map:
                    sensor_type = sensor_map[choice]
                    value = self.get_sensor_value(sensor_type)
                    if value is not None:
                        self.publish_sensor_data(sensor_type, value)
                        input("\nPress Enter to continue...")
                else:
                    print("❌ Invalid choice!")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user")
        finally:
            self.disconnect()
            print("✅ Disconnected from MQTT broker")


if __name__ == "__main__":
    controller = InteractiveSensorControl()
    controller.run()
