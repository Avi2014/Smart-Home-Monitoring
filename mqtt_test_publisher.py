"""
MQTT Test Publisher
Simple script to test MQTT broker connection by publishing test messages
"""

import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print("✅ Successfully connected to MQTT broker!")
        print(f"📡 Connection status code: {rc}")
    else:
        print(f"❌ Failed to connect, return code: {rc}")
        print("   Return codes:")
        print("   0: Success")
        print("   1: Incorrect protocol version")
        print("   2: Invalid client ID")
        print("   3: Server unavailable")
        print("   4: Bad username or password")
        print("   5: Not authorized")

def on_publish(client, userdata, mid, properties=None):
    """Callback when message is published"""
    print(f"✅ Message {mid} published successfully")

def on_disconnect(client, userdata, rc, properties=None):
    """Callback when disconnected"""
    if rc != 0:
        print(f"⚠️  Unexpected disconnect, return code: {rc}")

def test_publisher():
    """Test MQTT publishing"""
    
    print("="*70)
    print(" 📤 MQTT PUBLISHER TEST")
    print("="*70)
    
    # Configuration
    broker = "test.mosquitto.org"  # Using public broker for testing
    port = 1883
    topic = "test/iot/temperature"
    
    print(f"\n🔧 Configuration:")
    print(f"   Broker: {broker}")
    print(f"   Port: {port}")
    print(f"   Topic: {topic}")
    print("\n" + "="*70)
    
    # Create client
    client = mqtt.Client(
        client_id="test_publisher",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    try:
        print(f"\n🔌 Connecting to MQTT broker at {broker}:{port}...")
        client.connect(broker, port, 60)
        client.loop_start()
        
        # Give it a moment to connect
        time.sleep(2)
        
        print("\n📨 Publishing test messages...")
        print("-" * 70)
        
        # Publish 5 test messages
        for i in range(1, 6):
            message = {
                "test_id": i,
                "temperature": 20 + i,
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "status": "test"
            }
            
            message_json = json.dumps(message, indent=2)
            
            print(f"\n📤 Message {i}:")
            print(f"   Topic: {topic}")
            print(f"   Payload: {message}")
            
            result = client.publish(topic, message_json, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"   ✅ Queued for publishing (mid: {result.mid})")
            else:
                print(f"   ❌ Failed to publish: {result.rc}")
            
            time.sleep(1)
        
        print("\n" + "-" * 70)
        print("⏳ Waiting for all messages to be sent...")
        time.sleep(2)
        
        print("\n✅ Test completed successfully!")
        print("="*70)
        
    except ConnectionRefusedError:
        print("\n❌ ERROR: Connection refused!")
        print("   - Is Mosquitto broker running?")
        print("   - Try: mosquitto -v")
        print("   - Or use public broker: test.mosquitto.org")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        
    finally:
        client.loop_stop()
        client.disconnect()
        print("\n👋 Disconnected from broker")

if __name__ == "__main__":
    print("\n💡 TIP: Make sure MQTT broker is running before starting!")
    print("   Local broker: mosquitto -v")
    print("   Or modify script to use public broker\n")
    
    input("Press Enter to start test... (Ctrl+C to cancel)\n")
    
    try:
        test_publisher()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test cancelled by user")
