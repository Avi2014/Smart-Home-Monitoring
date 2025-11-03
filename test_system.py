"""
Quick System Test - Verify sensors are publishing and dashboard can receive
"""
import paho.mqtt.client as mqtt
import json
import time
import os
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "95c2f02d61404267847ebc19552f72b0.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "true").lower() == "true"

MQTT_TOPICS = [
    "hostel/room1/temperature",
    "hostel/room1/humidity",
    "hostel/room1/co2",
    "hostel/room1/light"
]

# Message counter
messages_received = {topic: 0 for topic in MQTT_TOPICS}

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print(f"✅ Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        print(f"📡 Subscribing to topics:")
        for topic in MQTT_TOPICS:
            result = client.subscribe(topic, qos=1)
            print(f"   - {topic}")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Callback when message is received"""
    try:
        payload = json.loads(msg.payload.decode())
        sensor_type = payload.get('sensor_type')
        value = payload.get('value')
        battery = payload.get('battery_level', 100)
        
        messages_received[msg.topic] += 1
        
        print(f"📨 [{msg.topic}] {sensor_type}: {value} (Battery: {battery}%) - Message #{messages_received[msg.topic]}")
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def main():
    print("="*70)
    print(" 🧪 IoT System Test - MQTT Message Listener")
    print("="*70)
    print("\nThis test will listen for sensor messages for 30 seconds...")
    print("If sensors are running, you should see messages appearing.\n")
    
    # Create MQTT client
    client = mqtt.Client(
        client_id=f"test_listener_{int(time.time())}",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        protocol=mqtt.MQTTv311
    )
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Set credentials
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # Enable TLS
    if MQTT_USE_TLS:
        client.tls_set(
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
    
    # Connect
    print(f"🔌 Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()
    
    # Wait for messages
    print("\n⏱️  Listening for 30 seconds...\n")
    time.sleep(30)
    
    # Stop and show results
    client.loop_stop()
    client.disconnect()
    
    print("\n" + "="*70)
    print(" 📊 TEST RESULTS")
    print("="*70)
    
    total_messages = sum(messages_received.values())
    
    if total_messages == 0:
        print("❌ NO MESSAGES RECEIVED!")
        print("\nPossible issues:")
        print("1. Sensors are not running (run: .\\start.ps1)")
        print("2. MQTT credentials are wrong (check .env file)")
        print("3. Firewall is blocking port 8883")
        print("4. Sensors are publishing to different topics")
    else:
        print(f"✅ Received {total_messages} total messages:\n")
        for topic, count in messages_received.items():
            status = "✅" if count > 0 else "❌"
            sensor_name = topic.split('/')[-1].capitalize()
            print(f"   {status} {sensor_name}: {count} messages")
        
        print(f"\n🎉 System is working! Dashboard should show data.")
    
    print("="*70)

if __name__ == "__main__":
    main()
