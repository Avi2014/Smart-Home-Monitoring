"""
IoT Alert System
Monitors sensor data and triggers alarms when thresholds are exceeded
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import winsound  # Windows sound library
import time

class IoTAlertSystem:
    def __init__(self):
        # Threshold configurations
        self.thresholds = {
            'temperature': {
                'min': 20,
                'max': 28,
                'unit': '°C',
                'name': 'Temperature'
            },
            'humidity': {
                'min': 40,
                'max': 60,
                'unit': '%',
                'name': 'Humidity'
            },
            'co2': {
                'min': 400,
                'max': 1000,
                'unit': 'ppm',
                'name': 'CO2 Level'
            },
            'light': {
                'min': 200,
                'max': 800,
                'unit': 'lux',
                'name': 'Light Level'
            }
        }
        
        self.alerts_triggered = {
            'temperature': False,
            'humidity': False,
            'co2': False,
            'light': False
        }
        
        self.alert_count = 0
        
        # MQTT setup
        self.client = mqtt.Client(
            client_id="alert_system",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            print("="*70)
            print(" 🚨 IoT ALERT SYSTEM - ACTIVE")
            print("="*70)
            print(f"\n✅ Connected to MQTT broker")
            
            # Subscribe to all sensor topics
            topics = [
                "hostel/room1/temperature",
                "hostel/room1/humidity",
                "hostel/room1/co2",
                "hostel/room1/light"
            ]
            
            for topic in topics:
                client.subscribe(topic)
            
            print(f"📡 Monitoring {len(topics)} sensor topics")
            print("\n📊 Threshold Configuration:")
            print("-" * 70)
            
            for sensor, config in self.thresholds.items():
                print(f"   {config['name']:15} : {config['min']:>6} - {config['max']:>6} {config['unit']}")
            
            print("\n" + "="*70)
            print(" 👂 Listening for sensor data... (Press Ctrl+C to stop)")
            print("="*70 + "\n")
    
    def on_message(self, client, userdata, msg):
        """Callback when message is received"""
        try:
            payload = json.loads(msg.payload.decode())
            sensor_type = payload.get('sensor_type')
            value = payload.get('value')
            timestamp = payload.get('timestamp')
            
            if sensor_type in self.thresholds:
                self.check_threshold(sensor_type, value, timestamp)
        
        except Exception as e:
            print(f"⚠️  Error processing message: {e}")
    
    def check_threshold(self, sensor_type, value, timestamp):
        """Check if value exceeds thresholds and trigger alert"""
        config = self.thresholds[sensor_type]
        min_val = config['min']
        max_val = config['max']
        
        # Check if value is out of range
        if value < min_val or value > max_val:
            # Only trigger alert if not already active for this sensor
            if not self.alerts_triggered[sensor_type]:
                self.trigger_alert(sensor_type, value, min_val, max_val, timestamp)
                self.alerts_triggered[sensor_type] = True
        else:
            # Value back to normal
            if self.alerts_triggered[sensor_type]:
                self.clear_alert(sensor_type, value, timestamp)
                self.alerts_triggered[sensor_type] = False
    
    def trigger_alert(self, sensor_type, value, min_val, max_val, timestamp):
        """Trigger an alert"""
        self.alert_count += 1
        config = self.thresholds[sensor_type]
        
        # Determine if too high or too low
        if value < min_val:
            alert_type = "TOO LOW"
            emoji = "❄️"
        else:
            alert_type = "TOO HIGH"
            emoji = "🔥"
        
        print("\n" + "🚨" * 35)
        print(f"\n  ⚠️  ALERT #{self.alert_count} - {alert_type}")
        print(f"  📊 Sensor: {config['name']}")
        print(f"  📈 Current Value: {value} {config['unit']}")
        print(f"  ✅ Safe Range: {min_val} - {max_val} {config['unit']}")
        print(f"  ⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"\n{'🚨' * 35}\n")
        
        # Play alert sound (Windows beep)
        try:
            # Play system beep: frequency, duration
            winsound.Beep(1000, 500)  # 1000 Hz for 500ms
        except:
            print("🔇 (Sound not available)")
    
    def clear_alert(self, sensor_type, value, timestamp):
        """Clear an alert when value returns to normal"""
        config = self.thresholds[sensor_type]
        
        print("\n" + "✅" * 35)
        print(f"\n  ✅ ALERT CLEARED")
        print(f"  📊 Sensor: {config['name']}")
        print(f"  📈 Current Value: {value} {config['unit']}")
        print(f"  ⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"\n{'✅' * 35}\n")
        
        # Play success sound
        try:
            winsound.Beep(2000, 200)  # Higher pitch, shorter
        except:
            pass
    
    def run(self):
        """Start the alert system"""
        try:
            self.client.connect("test.mosquitto.org", 1883, 60)
            self.client.loop_forever()
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Alert system stopped by user")
            print(f"\n📊 Total alerts triggered: {self.alert_count}")
            print("="*70)
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            self.client.disconnect()

if __name__ == "__main__":
    print("\n💡 TIP: Run sensors in other terminals to test alerts!")
    print("   Alerts trigger when values go outside safe ranges:\n")
    print("   - Temperature: Outside 20-28°C")
    print("   - Humidity: Outside 40-60%")
    print("   - CO2: Above 1000 ppm")
    print("   - Light: Outside 200-800 lux\n")
    
    input("Press Enter to start alert system... (Ctrl+C to stop)\n")
    
    alert_system = IoTAlertSystem()
    alert_system.run()
