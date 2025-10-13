"""
Temperature Sensor Simulator for IoT Monitoring System
Simulates realistic temperature readings for a hostel room
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import math
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TemperatureSensor')


class TemperatureSensor:
    def __init__(self, config_file='sensor_config.json'):
        """Initialize temperature sensor with configuration"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.mqtt_config = self.config['mqtt']
        self.sensor_config = self.config['sensors']['temperature']
        self.battery_config = self.config['battery']
        
        # Sensor state
        self.current_value = random.uniform(
            self.sensor_config['normal_range'][0],
            self.sensor_config['normal_range'][1]
        )
        self.battery_level = self.battery_config['initial_charge']
        self.message_count = 0
        
        # MQTT client
        self.client = mqtt.Client(client_id="temp_sensor_001")
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            logger.info(f"✅ Connected to MQTT Broker at {self.mqtt_config['broker']}:{self.mqtt_config['port']}")
        else:
            logger.error(f"❌ Failed to connect, return code {rc}")
    
    def on_publish(self, client, userdata, mid):
        """Callback when message is published"""
        logger.debug(f"Message {mid} published successfully")
    
    def generate_realistic_value(self):
        """Generate realistic temperature reading with natural variations"""
        # Simulate daily temperature cycle (cooler at night, warmer during day)
        hour = datetime.now().hour
        daily_cycle = math.sin((hour - 6) * math.pi / 12) * 3  # ±3°C variation
        
        # Add random noise
        noise = random.gauss(0, self.sensor_config['variance'])
        
        # Occasional spikes (window opened, AC turned on, etc.)
        if self.config['simulation']['random_spikes'] and random.random() < self.config['simulation']['spike_probability']:
            spike = random.choice([-4, -3, 3, 4])
            logger.info(f"🌡️  Temperature spike: {spike:+.1f}°C")
        else:
            spike = 0
        
        # Calculate new value
        target_value = (self.sensor_config['normal_range'][0] + 
                       self.sensor_config['normal_range'][1]) / 2
        new_value = target_value + daily_cycle + noise + spike
        
        # Smooth transition (sensor inertia)
        self.current_value = self.current_value * 0.7 + new_value * 0.3
        
        # Clamp to realistic bounds
        self.current_value = max(
            self.sensor_config['min_value'],
            min(self.sensor_config['max_value'], self.current_value)
        )
        
        return round(self.current_value, 2)
    
    def create_message(self, temperature):
        """Create MQTT message with sensor data and metadata"""
        self.message_count += 1
        
        message = {
            'sensor_id': 'TEMP_001',
            'sensor_type': 'temperature',
            'value': temperature,
            'unit': self.sensor_config['unit'],
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'battery_level': round(self.battery_level, 2),
            'message_count': self.message_count,
            'location': 'Hostel Room 1'
        }
        
        return json.dumps(message)
    
    def update_battery(self):
        """Simulate battery drain"""
        drain = self.battery_config['drain_per_message']
        self.battery_level = max(0, self.battery_level - drain)
        
        if self.battery_level < 20:
            logger.warning(f"⚠️  Low battery: {self.battery_level:.1f}%")
        elif self.battery_level == 0:
            logger.error("🔋 Battery depleted! Sensor would shut down.")
    
    def run(self):
        """Main sensor loop"""
        try:
            # Connect to MQTT broker
            logger.info(f"Connecting to MQTT broker {self.mqtt_config['broker']}...")
            self.client.connect(
                self.mqtt_config['broker'],
                self.mqtt_config['port'],
                self.mqtt_config['keepalive']
            )
            self.client.loop_start()
            
            topic = self.mqtt_config['topics']['temperature']
            sampling_rate = self.sensor_config['sampling_rate']
            
            logger.info(f"📡 Temperature sensor started")
            logger.info(f"📊 Publishing to topic: {topic}")
            logger.info(f"⏱️  Sampling rate: every {sampling_rate} seconds")
            logger.info(f"🔋 Battery level: {self.battery_level}%")
            print("\n" + "="*60)
            print("Press Ctrl+C to stop the sensor")
            print("="*60 + "\n")
            
            while self.battery_level > 0:
                # Generate sensor reading
                temperature = self.generate_realistic_value()
                
                # Create and publish message
                message = self.create_message(temperature)
                result = self.client.publish(
                    topic,
                    message,
                    qos=self.mqtt_config['qos']
                )
                
                # Log reading
                status = "🔥" if temperature > 28 else "❄️" if temperature < 20 else "✅"
                logger.info(
                    f"{status} Temperature: {temperature}°C | "
                    f"Battery: {self.battery_level:.1f}% | "
                    f"Messages: {self.message_count}"
                )
                
                # Update battery
                self.update_battery()
                
                # Wait for next reading
                time.sleep(sampling_rate)
                
        except KeyboardInterrupt:
            logger.info("\n⏹️  Sensor stopped by user")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("👋 Disconnected from MQTT broker")
            logger.info(f"📊 Total messages sent: {self.message_count}")


if __name__ == "__main__":
    import os
    
    # Change to project directory to find config file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'sensor_config.json')
    
    sensor = TemperatureSensor(config_path)
    sensor.run()
