"""
Automated MQTT Connection Test
Tests MQTT broker connectivity without user interaction
"""

import paho.mqtt.client as mqtt
import time
import json
import ssl
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mqtt_connection():
    """Test if we can connect to MQTT broker"""
    
    print("="*70)
    print(" 🔌 MQTT CONNECTION TEST")
    print("="*70)
    
    broker = os.getenv("MQTT_BROKER", "95c2f02d61404267847ebc19552f72b0.s1.eu.hivemq.cloud")
    port = int(os.getenv("MQTT_PORT", 8883))
    username = os.getenv("MQTT_USERNAME", None)
    password = os.getenv("MQTT_PASSWORD", None)
    use_tls = os.getenv("MQTT_USE_TLS", "true").lower() == "true"
    
    print(f"\n🌐 Broker: {broker}")
    print(f"🔌 Port: {port}")
    print(f"🔐 TLS: {'✅ Enabled' if use_tls else '❌ Disabled'}")
    print(f"🔑 Auth: {'✅ Enabled' if username else '❌ Disabled'}")
    print("\n" + "-"*70)
    
    connected = False
    
    def on_connect(client, userdata, flags, rc, properties=None):
        nonlocal connected
        if rc == 0:
            print("✅ Successfully connected to MQTT broker!")
            connected = True
        else:
            print(f"❌ Connection failed with code: {rc}")
    
    try:
        print("⏳ Attempting to connect...")
        
        client = mqtt.Client(
            client_id="connection_tester",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            protocol=mqtt.MQTTv311
        )
        client.on_connect = on_connect
        
        # Set credentials if available
        if username and password:
            client.username_pw_set(username, password)
        
        # Enable TLS if required
        if use_tls:
            client.tls_set(
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
        
        client.connect(broker, port, 60)
        client.loop_start()
        
        # Wait up to 10 seconds for connection (TLS takes longer)
        timeout = 10
        start = time.time()
        while not connected and (time.time() - start) < timeout:
            time.sleep(0.1)
        
        if connected:
            print("🎉 MQTT broker is reachable and working!")
            print("\n📊 Connection Details:")
            print(f"   - Broker: {broker}")
            print(f"   - Port: {port}")
            print(f"   - Protocol: MQTT v5.0")
            print(f"   - Connection time: {time.time() - start:.2f} seconds")
            
            # Test publish
            print("\n📤 Testing message publish...")
            test_topic = "iot/test/connection"
            test_message = {
                "test": "connection_check",
                "timestamp": datetime.utcnow().isoformat() + 'Z'
            }
            
            result = client.publish(test_topic, json.dumps(test_message), qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("   ✅ Message published successfully!")
            else:
                print(f"   ⚠️  Publish returned code: {result.rc}")
            
            time.sleep(1)
            
            client.loop_stop()
            client.disconnect()
            
            print("\n" + "="*70)
            print(" ✅ MQTT CONNECTION TEST PASSED")
            print("="*70)
            print("\n✨ You can now run your sensor simulators!")
            print("   Example: python sensors\\temperature_sensor.py")
            print("\n")
            return True
            
        else:
            print(f"❌ Connection timeout after {timeout} seconds")
            print("\n🔍 Troubleshooting:")
            print("   - Check your internet connection")
            print("   - Try another public broker:")
            print("     • broker.hivemq.com")
            print("     • mqtt.eclipseprojects.io")
            print("   - Check firewall settings")
            client.loop_stop()
            client.disconnect()
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔍 Possible issues:")
        print("   - No internet connection")
        print("   - Firewall blocking MQTT (port 1883)")
        print("   - Public broker might be down")
        return False

if __name__ == "__main__":
    success = test_mqtt_connection()
    exit(0 if success else 1)
