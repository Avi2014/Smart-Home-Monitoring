"""
Interactive IoT Sensor Control Panel
Manually control sensor values to test the dashboard and alarm system
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import random

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

class InteractiveSensorControl:
    def __init__(self):
        self.client = mqtt.Client(
            client_id="interactive_control",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.on_connect = self.on_connect
        self.connected = False
        
        # Current values
        self.values = {
            'temperature': 22.0,
            'humidity': 50.0,
            'co2': 600.0,
            'light': 400.0
        }
        
        # Topics
        self.topics = {
            'temperature': 'hostel/room1/temperature',
            'humidity': 'hostel/room1/humidity',
            'co2': 'hostel/room1/co2',
            'light': 'hostel/room1/light'
        }
    
    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.connected = True
            print("✅ Connected to MQTT Broker successfully!")
        else:
            print(f"❌ Connection failed with code {rc}")
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            print(f"📡 Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            time.sleep(2)  # Wait for connection
            return self.connected
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def publish_value(self, sensor_type, value):
        """Publish a sensor value to MQTT"""
        if not self.connected:
            print("❌ Not connected to MQTT broker!")
            return False
        
        self.values[sensor_type] = value
        
        message = {
            'sensor_type': sensor_type,
            'sensor_id': f'{sensor_type}_manual',
            'value': float(value),
            'unit': self.get_unit(sensor_type),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': 100.0,
            'location': 'hostel/room1'
        }
        
        topic = self.topics[sensor_type]
        self.client.publish(topic, json.dumps(message))
        
        emoji = self.get_emoji(sensor_type)
        unit = self.get_unit(sensor_type)
        print(f"✅ {emoji} Published {sensor_type}: {value}{unit}")
        return True
    
    def get_emoji(self, sensor_type):
        emojis = {
            'temperature': '🌡️',
            'humidity': '💧',
            'co2': '🌫️',
            'light': '💡'
        }
        return emojis.get(sensor_type, '📊')
    
    def get_unit(self, sensor_type):
        units = {
            'temperature': '°C',
            'humidity': '%',
            'co2': 'ppm',
            'light': 'lux'
        }
        return units.get(sensor_type, '')
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║        🎛️  INTERACTIVE IoT SENSOR CONTROL PANEL            ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n📡 Connected to MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        print("\nSelect an option:")
        print("  1. 🌡️  Set Temperature")
        print("  2. 💧 Set Humidity")
        print("  3. 🌫️  Set CO2 Level")
        print("  4. 💡 Set Light Level")
        print("  5. 🚀 Quick Test Scenarios")
        print("  6. 🔄 Continuous Mode (Auto-change values)")
        print("  7. 📊 View Current Values")
        print("  8. ❌ Exit")
        print("="*60)
    
    def set_temperature(self):
        """Set temperature manually"""
        print("\n🌡️  TEMPERATURE CONTROL")
        print("   Normal range: 20-28°C")
        print("   🚨 Alarm triggers: <20°C or >28°C")
        try:
            value = float(input("   Enter temperature (15-40°C): "))
            if 15 <= value <= 40:
                self.publish_value('temperature', value)
                if value < 20 or value > 28:
                    print("   ⚠️  WARNING: Value outside normal range! Alarm should trigger!")
            else:
                print("   ❌ Invalid range!")
        except ValueError:
            print("   ❌ Invalid input!")
    
    def set_humidity(self):
        """Set humidity manually"""
        print("\n💧 HUMIDITY CONTROL")
        print("   Normal range: 40-60%")
        print("   🚨 Alarm triggers: <40% or >60%")
        try:
            value = float(input("   Enter humidity (0-100%): "))
            if 0 <= value <= 100:
                self.publish_value('humidity', value)
                if value < 40 or value > 60:
                    print("   ⚠️  WARNING: Value outside normal range! Alarm should trigger!")
            else:
                print("   ❌ Invalid range!")
        except ValueError:
            print("   ❌ Invalid input!")
    
    def set_co2(self):
        """Set CO2 level manually"""
        print("\n🌫️  CO2 CONTROL")
        print("   Normal range: 400-1000 ppm")
        print("   🚨 Alarm triggers: >1000 ppm")
        try:
            value = float(input("   Enter CO2 (300-2000 ppm): "))
            if 300 <= value <= 2000:
                self.publish_value('co2', value)
                if value > 1000:
                    print("   ⚠️  WARNING: Value above normal! Alarm should trigger!")
            else:
                print("   ❌ Invalid range!")
        except ValueError:
            print("   ❌ Invalid input!")
    
    def set_light(self):
        """Set light level manually"""
        print("\n💡 LIGHT CONTROL")
        print("   Normal range: 200-800 lux")
        print("   🚨 Alarm triggers: <200 lux or >800 lux")
        try:
            value = float(input("   Enter light level (0-1000 lux): "))
            if 0 <= value <= 1000:
                self.publish_value('light', value)
                if value < 200 or value > 800:
                    print("   ⚠️  WARNING: Value outside normal range! Alarm should trigger!")
            else:
                print("   ❌ Invalid range!")
        except ValueError:
            print("   ❌ Invalid input!")
    
    def quick_scenarios(self):
        """Quick test scenarios"""
        print("\n🚀 QUICK TEST SCENARIOS")
        print("  1. ✅ Normal conditions (all sensors in safe range)")
        print("  2. 🔥 High temperature alert (35°C)")
        print("  3. ❄️  Low temperature alert (15°C)")
        print("  4. 💧 High humidity alert (80%)")
        print("  5. 🌵 Low humidity alert (25%)")
        print("  6. 🌫️  High CO2 alert (1500 ppm)")
        print("  7. 💡 Bright light alert (950 lux)")
        print("  8. 🌑 Low light alert (50 lux)")
        print("  9. 🚨 Emergency! (All sensors critical)")
        print("  0. ← Back to main menu")
        
        try:
            choice = input("\nSelect scenario (0-9): ")
            
            scenarios = {
                '1': {'temperature': 24, 'humidity': 50, 'co2': 600, 'light': 400},
                '2': {'temperature': 35, 'humidity': 50, 'co2': 600, 'light': 400},
                '3': {'temperature': 15, 'humidity': 50, 'co2': 600, 'light': 400},
                '4': {'temperature': 24, 'humidity': 80, 'co2': 600, 'light': 400},
                '5': {'temperature': 24, 'humidity': 25, 'co2': 600, 'light': 400},
                '6': {'temperature': 24, 'humidity': 50, 'co2': 1500, 'light': 400},
                '7': {'temperature': 24, 'humidity': 50, 'co2': 600, 'light': 950},
                '8': {'temperature': 24, 'humidity': 50, 'co2': 600, 'light': 50},
                '9': {'temperature': 40, 'humidity': 90, 'co2': 1800, 'light': 1000}
            }
            
            if choice in scenarios:
                print(f"\n📤 Publishing scenario {choice}...")
                for sensor, value in scenarios[choice].items():
                    self.publish_value(sensor, value)
                    time.sleep(0.2)
                print("\n✅ Scenario published! Check dashboard and alert system!")
                if choice in ['2', '3', '4', '5', '6', '7', '8', '9']:
                    print("🚨 This should trigger alarms!")
            elif choice == '0':
                return
            else:
                print("❌ Invalid choice!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def continuous_mode(self):
        """Continuous mode - gradually change values"""
        print("\n🔄 CONTINUOUS MODE")
        print("   Values will change gradually every 2 seconds")
        print("   Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Gradually increase temperature
                self.values['temperature'] = min(40, self.values['temperature'] + random.uniform(0.5, 2))
                self.publish_value('temperature', round(self.values['temperature'], 1))
                
                # Gradually increase humidity
                self.values['humidity'] = min(100, self.values['humidity'] + random.uniform(1, 5))
                self.publish_value('humidity', round(self.values['humidity'], 1))
                
                # Gradually increase CO2
                self.values['co2'] = min(2000, self.values['co2'] + random.uniform(50, 150))
                self.publish_value('co2', round(self.values['co2'], 0))
                
                # Random light changes
                self.values['light'] = max(0, min(1000, self.values['light'] + random.uniform(-100, 100)))
                self.publish_value('light', round(self.values['light'], 0))
                
                print("---")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Continuous mode stopped")
    
    def view_current_values(self):
        """Display current sensor values"""
        print("\n📊 CURRENT SENSOR VALUES")
        print("="*60)
        print(f"  🌡️  Temperature: {self.values['temperature']:.1f}°C")
        print(f"  💧 Humidity: {self.values['humidity']:.1f}%")
        print(f"  🌫️  CO2: {self.values['co2']:.0f} ppm")
        print(f"  💡 Light: {self.values['light']:.0f} lux")
        print("="*60)
    
    def run(self):
        """Main control loop"""
        # Connect to MQTT
        if not self.connect():
            print("❌ Failed to connect to MQTT broker. Exiting...")
            return
        
        print("\n✅ Interactive Control Panel Ready!")
        print("💡 Tip: Start the alert_system.py to hear alarms when limits are exceeded!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.set_temperature()
            elif choice == '2':
                self.set_humidity()
            elif choice == '3':
                self.set_co2()
            elif choice == '4':
                self.set_light()
            elif choice == '5':
                self.quick_scenarios()
            elif choice == '6':
                self.continuous_mode()
            elif choice == '7':
                self.view_current_values()
            elif choice == '8':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid choice! Please select 1-8")
        
        # Cleanup
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    print("🎛️  Starting Interactive IoT Sensor Control Panel...")
    controller = InteractiveSensorControl()
    controller.run()