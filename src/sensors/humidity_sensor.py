"""
Humidity Sensor Simulator for IoT Monitoring System
Simulates realistic humidity readings for a hostel room
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import math
import ssl
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HumiditySensor')


class HumiditySensor:
    def __init__(self, config_file='sensor_config.json'):
        """Initialize humidity sensor with configuration"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Override MQTT config with environment variables
        self.mqtt_config = self.config['mqtt']
        self.mqtt_config['broker'] = os.getenv("MQTT_BROKER", self.mqtt_config.get('broker'))
        self.mqtt_config['port'] = int(os.getenv("MQTT_PORT", self.mqtt_config.get('port', 8883)))
        self.mqtt_config['use_tls'] = os.getenv("MQTT_USE_TLS", "true").lower() == "true"
        self.mqtt_username = os.getenv("MQTT_USERNAME", None)
        self.mqtt_password = os.getenv("MQTT_PASSWORD", None)
        
        self.sensor_config = self.config['sensors']['humidity']
        self.battery_config = self.config['battery']
        
        # Sensor state
        self.current_value = random.uniform(
            self.sensor_config['normal_range'][0],
            self.sensor_config['normal_range'][1]
        )
        self.battery_level = self.battery_config['initial_charge']
        self.message_count = 0
        
        # MQTT client
        self.client = mqtt.Client(
            client_id="humidity_sensor_001",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            protocol=mqtt.MQTTv311
        )
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        
        # Set credentials if available
        if self.mqtt_username and self.mqtt_password:
            self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        
        # Enable TLS if required
        if self.mqtt_config.get('use_tls', False):
            self.client.tls_set(
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
        
    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            logger.info(f"✅ Connected to MQTT Broker at {self.mqtt_config['broker']}:{self.mqtt_config['port']}")
        else:
            logger.error(f"❌ Failed to connect, return code {rc}")
    
    def on_publish(self, client, userdata, mid, reason_code=None, properties=None):
        """Callback when message is published (paho-mqtt 2.x compatible)"""
        logger.debug(f"Message {mid} published successfully")
    
    def generate_realistic_value(self):
        """Generate realistic humidity reading with natural variations"""
        # Simulate daily humidity cycle (higher at night, lower during day)
        hour = datetime.now().hour
        daily_cycle = -math.sin((hour - 6) * math.pi / 12) * 8  # ±8% variation
        
        # Add random noise
        noise = random.gauss(0, self.sensor_config['variance'])
        
        # Occasional spikes (shower, rain, ventilation)
        if self.config['simulation']['random_spikes'] and random.random() < self.config['simulation']['spike_probability']:
            spike = random.choice([-10, -8, 8, 12, 15])
            logger.info(f"💧 Humidity spike: {spike:+.1f}%")
        else:
            spike = 0
        
        # Calculate new value
        target_value = (self.sensor_config['normal_range'][0] + 
                       self.sensor_config['normal_range'][1]) / 2
        new_value = target_value + daily_cycle + noise + spike
        
        # Smooth transition
        self.current_value = self.current_value * 0.75 + new_value * 0.25
        
        # Clamp to realistic bounds
        self.current_value = max(
            self.sensor_config['min_value'],
            min(self.sensor_config['max_value'], self.current_value)
        )
        
        return round(self.current_value, 2)
    
    def create_message(self, humidity):
        """Create MQTT message with sensor data and metadata"""
        self.message_count += 1
        
        message = {
            'sensor_id': 'HUM_001',
            'sensor_type': 'humidity',
            'value': humidity,
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
            
            topic = self.mqtt_config['topics']['humidity']
            sampling_rate = self.sensor_config['sampling_rate']
            
            logger.info(f"📡 Humidity sensor started")
            logger.info(f"📊 Publishing to topic: {topic}")
            logger.info(f"⏱️  Sampling rate: every {sampling_rate} seconds")
            logger.info(f"🔋 Battery level: {self.battery_level}%")
            print("\n" + "="*60)
            print("Press Ctrl+C to stop the sensor")
            print("="*60 + "\n")
            
            while True:  # Run continuously
                try:
                    # Generate sensor reading
                    humidity = self.generate_realistic_value()
                    
                    # Create and publish message
                    message = self.create_message(humidity)
                    result = self.client.publish(
                        topic,
                        message,
                        qos=self.mqtt_config['qos']
                    )
                    
                    # Log reading
                    status = "💧" if humidity > 60 else "🏜️" if humidity < 40 else "✅"
                    logger.info(
                        f"{status} Humidity: {humidity}% | "
                        f"Battery: {self.battery_level:.1f}% | "
                        f"Messages: {self.message_count}"
                    )
                    
                    # Update battery (simulate drain but don't stop)
                    self.update_battery()
                    
                    # Wait for next reading
                    time.sleep(sampling_rate)
                except Exception as e:
                    logger.error(f"Error in sensor loop: {e}")
                    time.sleep(1)  # Brief pause before retry
                    continue
                
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
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'sensor_config.json')
    
    sensor = HumiditySensor(config_path)
    sensor.run()
