"""
System Verification Script
Verifies that all components are properly configured for HiveMQ Cloud
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n" + "="*70)
    print("📋 Checking .env Configuration")
    print("="*70)
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found!")
        print("💡 Create a .env file with your HiveMQ credentials")
        return False
    
    print("✅ .env file exists")
    
    # Load and check variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        "MQTT_BROKER": "HiveMQ broker URL",
        "MQTT_PORT": "MQTT port (8883 for TLS)",
        "MQTT_USERNAME": "HiveMQ username",
        "MQTT_PASSWORD": "HiveMQ password",
        "MQTT_USE_TLS": "TLS/SSL enabled (true/false)"
    }
    
    all_present = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask password
            if var == "MQTT_PASSWORD":
                display_value = "*" * len(value)
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set ({description})")
            all_present = False
    
    return all_present

def check_dependencies():
    """Check if all required Python packages are installed"""
    print("\n" + "="*70)
    print("📦 Checking Python Dependencies")
    print("="*70)
    
    required_packages = {
        "paho-mqtt": "paho.mqtt.client",
        "streamlit": "streamlit",
        "plotly": "plotly",
        "pandas": "pandas",
        "numpy": "numpy",
        "python-dotenv": "dotenv"
    }
    
    all_installed = True
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name.split('.')[0])
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Not installed")
            all_installed = False
    
    return all_installed

def check_file_updates():
    """Check if critical files have been updated with .env support"""
    print("\n" + "="*70)
    print("📄 Checking File Updates")
    print("="*70)
    
    files_to_check = {
        "dashboard.py": ["load_dotenv", "os.getenv"],
        "alert_system.py": ["load_dotenv", "os.getenv", "ssl"],
        "interactive_control.py": ["load_dotenv", "os.getenv", "ssl"],
        "src/sensors/temperature_sensor.py": ["load_dotenv", "os.getenv", "ssl"],
        "src/sensors/humidity_sensor.py": ["load_dotenv", "os.getenv", "ssl"],
        "src/sensors/co2_sensor.py": ["load_dotenv", "os.getenv", "ssl"],
        "src/sensors/light_sensor.py": ["load_dotenv", "os.getenv", "ssl"]
    }
    
    all_updated = True
    for file_path, required_imports in files_to_check.items():
        if Path(file_path).exists():
            try:
                # Use utf-8 encoding to avoid charmap errors
                content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
                file_ok = all(imp in content for imp in required_imports)
                if file_ok:
                    print(f"✅ {file_path}")
                else:
                    print(f"⚠️  {file_path} - May need updates")
                    all_updated = False
            except Exception as e:
                print(f"⚠️  {file_path} - Could not read file: {e}")
                all_updated = False
        else:
            print(f"❌ {file_path} - File not found")
            all_updated = False
    
    return all_updated

def test_mqtt_connection():
    """Quick MQTT connection test"""
    print("\n" + "="*70)
    print("🔌 Testing MQTT Connection")
    print("="*70)
    
    try:
        import paho.mqtt.client as mqtt
        import ssl
        from dotenv import load_dotenv
        import time
        
        load_dotenv()
        
        broker = os.getenv("MQTT_BROKER")
        port = int(os.getenv("MQTT_PORT", 8883))
        username = os.getenv("MQTT_USERNAME")
        password = os.getenv("MQTT_PASSWORD")
        use_tls = os.getenv("MQTT_USE_TLS", "true").lower() == "true"
        
        print(f"📡 Broker: {broker}")
        print(f"🔌 Port: {port}")
        print(f"🔐 TLS: {'Enabled' if use_tls else 'Disabled'}")
        print(f"🔑 Auth: {'Enabled' if username else 'Disabled'}")
        
        connected = False
        connection_error = None
        
        def on_connect(client, userdata, flags, rc, properties=None):
            nonlocal connected, connection_error
            if rc == 0:
                connected = True
            else:
                connection_error = f"Connection failed with code {rc}"
        
        client = mqtt.Client(
            client_id="verification_test",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            protocol=mqtt.MQTTv311
        )
        client.on_connect = on_connect
        
        if username and password:
            client.username_pw_set(username, password)
        
        if use_tls:
            client.tls_set(
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
        
        print("\n⏳ Connecting...")
        client.connect(broker, port, 60)
        client.loop_start()
        
        timeout = 10
        start = time.time()
        while not connected and not connection_error and (time.time() - start) < timeout:
            time.sleep(0.1)
        
        client.loop_stop()
        client.disconnect()
        
        if connected:
            print("✅ MQTT connection successful!")
            return True
        else:
            print(f"❌ MQTT connection failed: {connection_error or 'Timeout'}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        return False

def main():
    """Run all verification checks"""
    print("\n" + "="*70)
    print("🔍 HIVEMQ CLOUD SYSTEM VERIFICATION")
    print("="*70)
    
    results = {
        ".env Configuration": check_env_file(),
        "Python Dependencies": check_dependencies(),
        "File Updates": check_file_updates(),
        "MQTT Connection": test_mqtt_connection()
    }
    
    print("\n" + "="*70)
    print("📊 VERIFICATION SUMMARY")
    print("="*70)
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check}")
    
    print("\n" + "="*70)
    
    if all(results.values()):
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your system is ready to use HiveMQ Cloud")
        print("\n💡 Next steps:")
        print("   1. Run: .\\scripts\\start_all.ps1")
        print("   2. Open dashboard: http://localhost:8501")
        print("   3. Test alerts with interactive control")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("❌ Please fix the issues above before proceeding")
        print("\n💡 Common fixes:")
        print("   1. Create/update .env file with HiveMQ credentials")
        print("   2. Install missing packages: pip install -r requirements.txt")
        print("   3. Verify HiveMQ cluster is active")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)