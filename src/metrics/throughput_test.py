"""
Throughput Test Script
Measures message throughput (messages per second)
"""

import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime

class ThroughputTester:
    def __init__(self):
        self.message_count = 0
        self.test_duration = 60  # seconds
        self.message_timestamps = []
        self.sensor_counts = {
            'temperature': 0,
            'humidity': 0,
            'co2': 0,
            'light': 0
        }
        
        self.client = mqtt.Client(client_id="throughput_tester")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT Broker")
            topics = [
                "hostel/room1/temperature",
                "hostel/room1/humidity",
                "hostel/room1/co2",
                "hostel/room1/light"
            ]
            for topic in topics:
                client.subscribe(topic)
            print(f"📡 Subscribed to {len(topics)} topics\n")
    
    def on_message(self, client, userdata, msg):
        """Count messages"""
        try:
            self.message_count += 1
            self.message_timestamps.append(time.time())
            
            payload = json.loads(msg.payload.decode())
            sensor_type = payload.get('sensor_type', 'unknown')
            
            if sensor_type in self.sensor_counts:
                self.sensor_counts[sensor_type] += 1
            
            # Print every 10 messages
            if self.message_count % 10 == 0:
                elapsed = time.time() - self.start_time
                current_rate = self.message_count / elapsed if elapsed > 0 else 0
                print(f"📨 Messages: {self.message_count:4} | "
                      f"Rate: {current_rate:.2f} msg/s | "
                      f"Elapsed: {elapsed:.1f}s")
            
        except Exception as e:
            print(f"⚠️  Error: {e}")
    
    def run_test(self):
        """Run throughput test"""
        print("="*70)
        print(" 📊 THROUGHPUT TEST - IoT Monitoring System")
        print("="*70)
        print(f"\n⏱️  Test Duration: {self.test_duration} seconds")
        print("🎯 Measuring: Messages received per second\n")
        
        try:
            self.client.connect("localhost", 1883, 60)
            self.client.loop_start()
            
            self.start_time = time.time()
            
            # Run test
            while time.time() - self.start_time < self.test_duration:
                time.sleep(0.1)
            
            self.client.loop_stop()
            self.client.disconnect()
            
            # Calculate statistics
            self.print_results()
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Test stopped by user")
            self.print_results()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def print_results(self):
        """Print test results"""
        print("\n" + "="*70)
        print(" 📈 TEST RESULTS")
        print("="*70)
        
        elapsed = time.time() - self.start_time
        
        print(f"\n📊 Total Messages Received: {self.message_count}")
        print(f"⏱️  Test Duration:          {elapsed:.2f} seconds")
        print(f"📈 Average Throughput:      {self.message_count/elapsed:.2f} messages/second")
        
        print("\n📡 Messages by Sensor Type:")
        for sensor, count in self.sensor_counts.items():
            rate = count / elapsed if elapsed > 0 else 0
            print(f"   {sensor:12}: {count:4} messages ({rate:.2f} msg/s)")
        
        # Calculate throughput over time (5-second windows)
        if self.message_timestamps:
            print("\n📊 Throughput Over Time (5-second windows):")
            window_size = 5
            start = self.message_timestamps[0]
            end = self.message_timestamps[-1]
            
            current_window = start
            while current_window < end:
                window_end = current_window + window_size
                count = sum(1 for t in self.message_timestamps 
                           if current_window <= t < window_end)
                rate = count / window_size
                
                elapsed_from_start = current_window - start
                bar = "█" * int(rate * 2)
                print(f"   {elapsed_from_start:5.0f}s - {elapsed_from_start+window_size:5.0f}s: "
                      f"{rate:5.2f} msg/s {bar}")
                
                current_window = window_end
        
        # Performance rating
        avg_throughput = self.message_count / elapsed if elapsed > 0 else 0
        if avg_throughput >= 1.0:
            rating = "🌟 EXCELLENT"
        elif avg_throughput >= 0.5:
            rating = "✅ GOOD"
        elif avg_throughput >= 0.2:
            rating = "⚠️  ACCEPTABLE"
        else:
            rating = "❌ POOR"
        
        print(f"\n🏆 Performance Rating: {rating}")
        
        # Data rate estimate
        if self.message_count > 0:
            avg_message_size = 250  # bytes (approximate)
            data_rate_bytes = avg_throughput * avg_message_size
            data_rate_kb = data_rate_bytes / 1024
            print(f"📡 Estimated Data Rate: {data_rate_kb:.2f} KB/s")
        
        print("="*70 + "\n")

if __name__ == "__main__":
    tester = ThroughputTester()
    tester.run_test()
