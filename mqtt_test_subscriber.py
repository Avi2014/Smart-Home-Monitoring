"""
MQTT Test Subscriber
Simple script to test MQTT broker connection by subscribing to test messages
"""

import paho.mqtt.client as mqtt
import json
import time

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print("✅ Successfully connected to MQTT broker!")
        print(f"📡 Connection status code: {rc}")
        
        # Subscribe to test topic
        topic = "test/iot/#"  # # is wildcard for all subtopics
        client.subscribe(topic, qos=1)
        print(f"📬 Subscribed to topic: {topic}")
        print("\n" + "="*70)
        print(" 👂 Listening for messages... (Press Ctrl+C to stop)")
        print("="*70 + "\n")
    else:
        print(f"❌ Failed to connect, return code: {rc}")

def on_message(client, userdata, msg):
    """Callback when message is received"""
    try:
        print(f"\n📨 Message Received:")
        print(f"   Topic: {msg.topic}")
        print(f"   QoS: {msg.qos}")
        print(f"   Retain: {msg.retain}")
        
        # Try to parse as JSON
        try:
            payload = json.loads(msg.payload.decode())
            print(f"   Payload (JSON):")
            for key, value in payload.items():
                print(f"      {key}: {value}")
        except json.JSONDecodeError:
            print(f"   Payload (Raw): {msg.payload.decode()}")
        
        print("-" * 70)
        
    except Exception as e:
        print(f"⚠️  Error processing message: {e}")

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """Callback when subscribed to topic"""
    print(f"✅ Subscription confirmed (mid: {mid}, QoS: {granted_qos})")

def on_disconnect(client, userdata, rc, properties=None):
    """Callback when disconnected"""
    if rc != 0:
        print(f"\n⚠️  Unexpected disconnect, return code: {rc}")
        print("   Attempting to reconnect...")

def test_subscriber():
    """Test MQTT subscribing"""
    
    print("="*70)
    print(" 📥 MQTT SUBSCRIBER TEST")
    print("="*70)
    
    # Configuration
    broker = "test.mosquitto.org"  # Using public broker for testing
    port = 1883
    
    print(f"\n🔧 Configuration:")
    print(f"   Broker: {broker}")
    print(f"   Port: {port}")
    print("\n" + "="*70)
    
    # Create client
    client = mqtt.Client(
        client_id="test_subscriber",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    
    try:
        print(f"\n🔌 Connecting to MQTT broker at {broker}:{port}...")
        client.connect(broker, port, 60)
        
        # Blocking call that processes network traffic and dispatches callbacks
        client.loop_forever()
        
    except ConnectionRefusedError:
        print("\n❌ ERROR: Connection refused!")
        print("   - Is Mosquitto broker running?")
        print("   - Try: mosquitto -v")
        print("   - Or use public broker: test.mosquitto.org")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Subscriber stopped by user")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        
    finally:
        client.disconnect()
        print("\n👋 Disconnected from broker")
        print("="*70)

if __name__ == "__main__":
    print("\n💡 TIP: Make sure MQTT broker is running before starting!")
    print("   Local broker: mosquitto -v")
    print("   Or modify script to use public broker\n")
    print("💡 TIP: Run mqtt_test_publisher.py in another terminal to send messages\n")
    
    input("Press Enter to start listening... (Ctrl+C to stop)\n")
    
    test_subscriber()
