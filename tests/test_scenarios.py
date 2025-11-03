"""
Consolidated Test Scenarios for IoT Monitoring System
Tests all major functionalities
"""
import paho.mqtt.client as mqtt
import json
import time
import ssl
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "95c2f02d61404267847ebc19552f72b0.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "true").lower() == "true"

class TestScenarios:
    def __init__(self):
        self.client = mqtt.Client(
            client_id="test_scenarios",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            protocol=mqtt.MQTTv311
        )
        self.connected = False
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            print(f"🔌 Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
            
            # Set credentials if available
            if MQTT_USERNAME and MQTT_PASSWORD:
                self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
            
            # Enable TLS if required
            if MQTT_USE_TLS:
                self.client.tls_set(
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2
                )
            
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            time.sleep(2)
            self.connected = True
            print("✅ Connected successfully!\n")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def publish_value(self, sensor_type, value, unit):
        """Publish sensor value"""
        message = {
            'sensor_type': sensor_type,
            'sensor_id': f'{sensor_type}_test',
            'value': float(value),
            'unit': unit,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': 100.0
        }
        
        topic = f'hostel/room1/{sensor_type}'
        self.client.publish(topic, json.dumps(message))
        print(f"  ✅ Published {sensor_type}: {value}{unit}")
    
    def scenario_normal(self):
        """Scenario 1: Normal conditions (all sensors in safe range)"""
        print("\n" + "="*60)
        print("🟢 SCENARIO 1: Normal Conditions")
        print("="*60)
        print("All sensors within safe ranges - No alarms expected")
        print()
        
        self.publish_value('temperature', 24, '°C')
        time.sleep(0.5)
        self.publish_value('humidity', 50, '%')
        time.sleep(0.5)
        self.publish_value('co2', 600, 'ppm')
        time.sleep(0.5)
        self.publish_value('light', 400, 'lux')
        time.sleep(2)
        
        print("\n✅ Scenario 1 complete - System should show all green")
    
    def scenario_high_temp(self):
        """Scenario 2: High temperature alert"""
        print("\n" + "="*60)
        print("🔥 SCENARIO 2: High Temperature Alert")
        print("="*60)
        print("Temperature: 35°C (exceeds 28°C limit)")
        print("🔊 BEEP sound expected!")
        print()
        
        self.publish_value('temperature', 35, '°C')
        time.sleep(3)
        
        print("\n✅ Scenario 2 complete - Check alert system for BEEP!")
    
    def scenario_low_temp(self):
        """Scenario 3: Low temperature alert"""
        print("\n" + "="*60)
        print("❄️  SCENARIO 3: Low Temperature Alert")
        print("="*60)
        print("Temperature: 15°C (below 20°C limit)")
        print("🔊 BEEP sound expected!")
        print()
        
        self.publish_value('temperature', 15, '°C')
        time.sleep(3)
        
        print("\n✅ Scenario 3 complete - Check alert system for BEEP!")
    
    def scenario_high_humidity(self):
        """Scenario 4: High humidity alert"""
        print("\n" + "="*60)
        print("💧 SCENARIO 4: High Humidity Alert")
        print("="*60)
        print("Humidity: 85% (exceeds 60% limit)")
        print("🔊 BEEP sound expected!")
        print()
        
        self.publish_value('humidity', 85, '%')
        time.sleep(3)
        
        print("\n✅ Scenario 4 complete - Check alert system for BEEP!")
    
    def scenario_high_co2(self):
        """Scenario 5: High CO2 alert"""
        print("\n" + "="*60)
        print("🌫️  SCENARIO 5: High CO2 Alert")
        print("="*60)
        print("CO2: 1500 ppm (exceeds 1000 ppm limit)")
        print("🔊 BEEP sound expected!")
        print()
        
        self.publish_value('co2', 1500, 'ppm')
        time.sleep(3)
        
        print("\n✅ Scenario 5 complete - Check alert system for BEEP!")
    
    def scenario_low_light(self):
        """Scenario 6: Low light alert"""
        print("\n" + "="*60)
        print("🌑 SCENARIO 6: Low Light Alert")
        print("="*60)
        print("Light: 50 lux (below 200 lux limit)")
        print("🔊 BEEP sound expected!")
        print()
        
        self.publish_value('light', 50, 'lux')
        time.sleep(3)
        
        print("\n✅ Scenario 6 complete - Check alert system for BEEP!")
    
    def scenario_emergency(self):
        """Scenario 7: Emergency - All sensors critical"""
        print("\n" + "="*60)
        print("🚨🚨🚨 SCENARIO 7: EMERGENCY - ALL SENSORS CRITICAL!")
        print("="*60)
        print("ALL sensors exceed limits!")
        print("🔊🔊🔊🔊 MULTIPLE BEEPS expected!")
        print()
        
        self.publish_value('temperature', 40, '°C')
        time.sleep(0.5)
        self.publish_value('humidity', 90, '%')
        time.sleep(0.5)
        self.publish_value('co2', 1800, 'ppm')
        time.sleep(0.5)
        self.publish_value('light', 1000, 'lux')
        time.sleep(5)
        
        print("\n✅ Scenario 7 complete - Check for MULTIPLE ALARMS!")
    
    def scenario_clear_all(self):
        """Scenario 8: Clear all alarms"""
        print("\n" + "="*60)
        print("✅ SCENARIO 8: Clear All Alarms")
        print("="*60)
        print("Returning all sensors to normal values")
        print()
        
        self.publish_value('temperature', 24, '°C')
        time.sleep(0.5)
        self.publish_value('humidity', 50, '%')
        time.sleep(0.5)
        self.publish_value('co2', 600, 'ppm')
        time.sleep(0.5)
        self.publish_value('light', 400, 'lux')
        time.sleep(2)
        
        print("\n✅ Scenario 8 complete - All alarms should be cleared")
    
    def run_all_scenarios(self):
        """Run all test scenarios in sequence"""
        print("\n" + "="*60)
        print("🧪 RUNNING ALL TEST SCENARIOS")
        print("="*60)
        print("\n⚠️  Make sure alert_system.py is running!")
        print("⚠️  Dashboard should be open at http://localhost:8501")
        input("\nPress Enter when ready to start...")
        
        scenarios = [
            ("Normal Conditions", self.scenario_normal),
            ("High Temperature", self.scenario_high_temp),
            ("Low Temperature", self.scenario_low_temp),
            ("High Humidity", self.scenario_high_humidity),
            ("High CO2", self.scenario_high_co2),
            ("Low Light", self.scenario_low_light),
            ("EMERGENCY", self.scenario_emergency),
            ("Clear All Alarms", self.scenario_clear_all)
        ]
        
        for i, (name, scenario) in enumerate(scenarios, 1):
            print(f"\n\n{'='*60}")
            print(f"Running test {i}/{len(scenarios)}: {name}")
            print(f"{'='*60}")
            time.sleep(2)
            scenario()
            time.sleep(3)
        
        print("\n\n" + "="*60)
        print("✅ ALL SCENARIOS COMPLETE!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"  • {len(scenarios)} scenarios executed")
        print("  • Check alert system for alarm count")
        print("  • Review dashboard for data visualization")
        print("  • All alarms should be cleared now")
        print("\n💡 Tip: Review alert_system.py terminal for detailed logs")
    
    def disconnect(self):
        """Disconnect from MQTT"""
        self.client.loop_stop()
        self.client.disconnect()
        print("\n👋 Disconnected from MQTT broker")


def main():
    """Main function"""
    print("="*60)
    print("🧪 IoT MONITORING SYSTEM - TEST SCENARIOS")
    print("="*60)
    
    tester = TestScenarios()
    
    if not tester.connect():
        return
    
    while True:
        print("\n" + "="*60)
        print("Select Test Scenario:")
        print("="*60)
        print("  1. Normal Conditions (all safe)")
        print("  2. High Temperature Alert")
        print("  3. Low Temperature Alert")
        print("  4. High Humidity Alert")
        print("  5. High CO2 Alert")
        print("  6. Low Light Alert")
        print("  7. EMERGENCY (all sensors critical)")
        print("  8. Clear All Alarms")
        print("  9. Run All Scenarios (Auto)")
        print("  0. Exit")
        print("="*60)
        
        choice = input("\nEnter choice (0-9): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            tester.scenario_normal()
        elif choice == '2':
            tester.scenario_high_temp()
        elif choice == '3':
            tester.scenario_low_temp()
        elif choice == '4':
            tester.scenario_high_humidity()
        elif choice == '5':
            tester.scenario_high_co2()
        elif choice == '6':
            tester.scenario_low_light()
        elif choice == '7':
            tester.scenario_emergency()
        elif choice == '8':
            tester.scenario_clear_all()
        elif choice == '9':
            tester.run_all_scenarios()
        else:
            print("❌ Invalid choice!")
        
        time.sleep(1)
    
    tester.disconnect()
    print("\n✅ Testing complete!")


if __name__ == "__main__":
    main()
