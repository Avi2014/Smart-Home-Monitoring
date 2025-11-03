"""
CO2 Sensor Simulator for IoT Monitoring System
Simulates realistic CO2 (air quality) readings for a hostel room
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
logger = logging.getLogger('CO2Sensor')


class CO2Sensor:
    def __init__(self, config_file='sensor_config.json'):
        """Initialize CO2 sensor with configuration"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Override MQTT config with environment variables
        self.mqtt_config = self.config['mqtt']
        self.mqtt_config['broker'] = os.getenv("MQTT_BROKER", self.mqtt_config.get('broker'))
        self.mqtt_config['port'] = int(os.getenv("MQTT_PORT", self.mqtt_config.get('port', 8883)))
        self.mqtt_config['use_tls'] = os.getenv("MQTT_USE_TLS", "true").lower() == "true"
        self.mqtt_username = os.getenv("MQTT_USERNAME", None)
        self.mqtt_password = os.getenv("MQTT_PASSWORD", None)
        
        self.sensor_config = self.config['sensors']['co2']
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
            client_id="co2_sensor_001",
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
        """Generate realistic CO2 reading with natural variations"""
        # Simulate occupancy patterns (higher CO2 when people are in room)
        hour = datetime.now().hour
        
        # Higher CO2 during sleep hours and study hours
        if 0 <= hour < 7:  # Night - people sleeping in room
            occupancy_factor = 300
        elif 7 <= hour < 9:  # Morning - getting ready
            occupancy_factor = 150
        elif 9 <= hour < 17:  # Day - room empty (classes)
            occupancy_factor = -100
        elif 17 <= hour < 23:  # Evening - studying
            occupancy_factor = 250
        else:  # Late night
            occupancy_factor = 200
        
        # Add random noise
        noise = random.gauss(0, self.sensor_config['variance'])
        
        # Occasional spikes (many people in room, poor ventilation)
        if self.config['simulation']['random_spikes'] and random.random() < self.config['simulation']['spike_probability']:
            spike = random.choice([200, 300, 400])
            logger.info(f"🌫️  CO2 spike: +{spike} ppm (poor ventilation)")
        else:
            spike = 0
        
        # Calculate new value
        base_value = 600  # Typical indoor baseline
        new_value = base_value + occupancy_factor + noise + spike
        
        # Smooth transition (CO2 changes gradually)
        self.current_value = self.current_value * 0.8 + new_value * 0.2
        
        # Clamp to realistic bounds
        self.current_value = max(
            self.sensor_config['min_value'],
            min(self.sensor_config['max_value'], self.current_value)
        )
        
        return round(self.current_value, 0)
    
    def create_message(self, co2):
        """Create MQTT message with sensor data and metadata"""
        self.message_count += 1
        
        # Determine air quality level
        if co2 < 800:
            air_quality = "Good"
        elif co2 < 1000:
            air_quality = "Moderate"
        elif co2 < 1500:
            air_quality = "Poor"
        else:
            air_quality = "Very Poor"
        
        message = {
            'sensor_id': 'CO2_001',
            'sensor_type': 'co2',
            'value': co2,
            'unit': self.sensor_config['unit'],
            'air_quality': air_quality,
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
            
            topic = self.mqtt_config['topics']['co2']
            sampling_rate = self.sensor_config['sampling_rate']
            
            logger.info(f"📡 CO2 sensor started")
            logger.info(f"📊 Publishing to topic: {topic}")
            logger.info(f"⏱️  Sampling rate: every {sampling_rate} seconds")
            logger.info(f"🔋 Battery level: {self.battery_level}%")
            print("\n" + "="*60)
            print("Press Ctrl+C to stop the sensor")
            print("="*60 + "\n")
            
            while True:  # Run continuously
                try:
                    # Generate sensor reading
                    co2 = self.generate_realistic_value()
                    
                    # Create and publish message
                    message = self.create_message(co2)
                    result = self.client.publish(
                        topic,
                        message,
                        qos=self.mqtt_config['qos']
                    )
                    
                    # Log reading
                    if co2 < 800:
                        status = "✅"
                    elif co2 < 1000:
                        status = "⚠️"
                    else:
                        status = "🚨"
                    
                    logger.info(
                        f"{status} CO2: {co2} ppm | "
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
    
    sensor = CO2Sensor(config_path)
    sensor.run()
