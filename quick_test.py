"""Quick MQTT test to see if sensors are publishing"""
import paho.mqtt.client as mqtt
import json
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT", 8883))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

received = []

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"✅ Connected! Code: {rc}")
    topics = [
        "hostel/room1/temperature",
        "hostel/room1/humidity", 
        "hostel/room1/co2",
        "hostel/room1/light"
    ]
    for topic in topics:
        client.subscribe(topic, qos=1)
        print(f"📡 Subscribed to: {topic}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        sensor = payload.get('sensor_type')
        value = payload.get('value')
        print(f"📨 {sensor}: {value}")
        received.append(sensor)
    except Exception as e:
        print(f"❌ Error: {e}")

client = mqtt.Client(
    client_id="test_123",
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

print(f"🔌 Connecting to {BROKER}:{PORT}...")
client.connect(BROKER, PORT, keepalive=60)

import time
client.loop_start()
print("⏱️  Waiting 15 seconds for messages...")
time.sleep(15)
client.loop_stop()

print(f"\n📊 Received {len(received)} messages from sensors: {set(received)}")
if len(received) == 0:
    print("❌ NO MESSAGES RECEIVED - Sensors may not be running!")
else:
    print("✅ Sensors ARE publishing data!")
