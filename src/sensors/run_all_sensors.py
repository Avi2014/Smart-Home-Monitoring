"""
Run All Sensors - Convenience Script
Starts all four sensor simulators in sequence
"""

import subprocess
import sys
import os
import time

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    sensors = [
        'temperature_sensor.py',
        'humidity_sensor.py',
        'co2_sensor.py',
        'light_sensor.py'
    ]
    
    print("="*70)
    print(" 🏠 SMART HOME IOT MONITORING SYSTEM - SENSOR SUITE")
    print("="*70)
    print("\n📋 Starting all sensor simulators:")
    print("   - Temperature Sensor (every 3s)")
    print("   - Humidity Sensor (every 3s)")
    print("   - CO2 Sensor (every 3s)")
    print("   - Light Sensor (every 3s)")
    print("\n⚡ Auto-starting sensors now...")
    print("="*70 + "\n")
    
    time.sleep(1)  # Brief pause for display
    
    for sensor in sensors:
        sensor_path = os.path.join(script_dir, sensor)
        print(f"\n🚀 Starting {sensor}...")
        
        # Start each sensor in a new terminal window (PowerShell)
        subprocess.Popen([
            'powershell.exe',
            '-NoExit',
            '-Command',
            f'python "{sensor_path}"'
        ])
        
        time.sleep(1)  # Small delay between starting sensors
    
    print("\n" + "="*70)
    print("✅ All sensors started!")
    print("="*70)
    print("\n📊 Check the terminal windows to see sensor data")
    print("🌐 Data is being published to MQTT broker")
    print("👀 Monitor in Node-RED: http://localhost:1880")
    print("\n💡 To stop all sensors: Close each terminal window or press Ctrl+C")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Startup cancelled by user")
        sys.exit(0)
