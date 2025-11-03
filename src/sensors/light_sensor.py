"""
Light Sensor Simulator for IoT Monitoring System
Simulates realistic light level readings for a hostel room
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
logger = logging.getLogger('LightSensor')


class LightSensor:
    def __init__(self, config_file='sensor_config.json'):
        """Initialize light sensor with configuration"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Override MQTT config with environment variables
        self.mqtt_config = self.config['mqtt']
        self.mqtt_config['broker'] = os.getenv("MQTT_BROKER", self.mqtt_config.get('broker'))
        self.mqtt_config['port'] = int(os.getenv("MQTT_PORT", self.mqtt_config.get('port', 8883)))
        self.mqtt_config['use_tls'] = os.getenv("MQTT_USE_TLS", "true").lower() == "true"
        self.mqtt_username = os.getenv("MQTT_USERNAME", None)
        self.mqtt_password = os.getenv("MQTT_PASSWORD", None)
        
        self.sensor_config = self.config['sensors']['light']
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
            client_id="light_sensor_001",
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
        """Generate realistic light level reading with natural variations"""
        hour = datetime.now().hour
        
        # Simulate daily light cycle
        if 6 <= hour < 8:  # Dawn
            natural_light = 200 + (hour - 6) * 150
        elif 8 <= hour < 18:  # Daytime
            natural_light = 500 + math.sin((hour - 12) * math.pi / 6) * 200
        elif 18 <= hour < 20:  # Dusk
            natural_light = 500 - (hour - 18) * 200
        else:  # Night
            natural_light = 50
        
        # Artificial lighting (lights on in evening)
        if 18 <= hour < 24 or 0 <= hour < 2:
            artificial_light = 400
        elif 5 <= hour < 7:  # Early morning
            artificial_light = 200
        else:
            artificial_light = 0
        
        # Add random noise
        noise = random.gauss(0, self.sensor_config['variance'])
        
        # Occasional changes (curtains opened/closed, lights toggled)
        if self.config['simulation']['random_spikes'] and random.random() < self.config['simulation']['spike_probability']:
            spike = random.choice([-300, -200, 200, 300])
            logger.info(f"💡 Light level change: {spike:+.0f} lux")
        else:
            spike = 0
        
        # Calculate new value
        new_value = natural_light + artificial_light + noise + spike
        
        # Smooth transition
        self.current_value = self.current_value * 0.7 + new_value * 0.3
        
        # Clamp to realistic bounds
        self.current_value = max(
            self.sensor_config['min_value'],
            min(self.sensor_config['max_value'], self.current_value)
        )
        
        return round(self.current_value, 0)
    
    def create_message(self, light):
        """Create MQTT message with sensor data and metadata"""
        self.message_count += 1
        
        # Determine lighting condition
        if light < 50:
            condition = "Dark"
        elif light < 200:
            condition = "Dim"
        elif light < 500:
            condition = "Moderate"
        else:
            condition = "Bright"
        
        message = {
            'sensor_id': 'LIGHT_001',
            'sensor_type': 'light',
            'value': light,
            'unit': self.sensor_config['unit'],
            'condition': condition,
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
            
            topic = self.mqtt_config['topics']['light']
            sampling_rate = self.sensor_config['sampling_rate']
            
            logger.info(f"📡 Light sensor started")
            logger.info(f"📊 Publishing to topic: {topic}")
            logger.info(f"⏱️  Sampling rate: every {sampling_rate} seconds")
            logger.info(f"🔋 Battery level: {self.battery_level}%")
            print("\n" + "="*60)
            print("Press Ctrl+C to stop the sensor")
            print("="*60 + "\n")
            
            while True:  # Run continuously
                try:
                    # Generate sensor reading
                    light = self.generate_realistic_value()
                    
                    # Create and publish message
                    message = self.create_message(light)
                    result = self.client.publish(
                        topic,
                        message,
                        qos=self.mqtt_config['qos']
                    )
                    
                    # Log reading
                    if light < 50:
                        status = "🌙"
                    elif light < 200:
                        status = "🕯️"
                    elif light < 500:
                        status = "💡"
                    else:
                        status = "☀️"
                    
                    logger.info(
                        f"{status} Light: {light} lux | "
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
    
    sensor = LightSensor(config_path)
    sensor.run()
