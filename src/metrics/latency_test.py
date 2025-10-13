"""
Latency Test Script
Measures end-to-end latency from sensor to dashboard
"""

import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import statistics

class LatencyTester:
    def __init__(self):
        self.latencies = []
        self.received_count = 0
        self.test_duration = 60  # seconds
        
        self.client = mqtt.Client(client_id="latency_tester")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT Broker")
            # Subscribe to all sensor topics
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
        """Calculate latency when message received"""
        try:
            receive_time = datetime.utcnow()
            payload = json.loads(msg.payload.decode())
            
            # Parse timestamp from sensor
            send_time = datetime.fromisoformat(payload['timestamp'].replace('Z', ''))
            
            # Calculate latency in milliseconds
            latency = (receive_time - send_time).total_seconds() * 1000
            
            self.latencies.append(latency)
            self.received_count += 1
            
            print(f"📨 {payload['sensor_type']:12} | Latency: {latency:6.2f} ms | "
                  f"Messages: {self.received_count}")
            
        except Exception as e:
            print(f"⚠️  Error processing message: {e}")
    
    def run_test(self):
        """Run latency test for specified duration"""
        print("="*70)
        print(" 📊 LATENCY TEST - IoT Monitoring System")
        print("="*70)
        print(f"\n⏱️  Test Duration: {self.test_duration} seconds")
        print("🎯 Measuring: Time from sensor reading to MQTT reception\n")
        
        try:
            self.client.connect("localhost", 1883, 60)
            self.client.loop_start()
            
            # Run test
            start_time = time.time()
            while time.time() - start_time < self.test_duration:
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
        
        if self.latencies:
            print(f"\n📊 Total Messages Received: {self.received_count}")
            print(f"⏱️  Average Latency:        {statistics.mean(self.latencies):.2f} ms")
            print(f"📉 Minimum Latency:        {min(self.latencies):.2f} ms")
            print(f"📈 Maximum Latency:        {max(self.latencies):.2f} ms")
            print(f"📊 Median Latency:         {statistics.median(self.latencies):.2f} ms")
            print(f"📐 Std Deviation:          {statistics.stdev(self.latencies):.2f} ms")
            
            # Latency distribution
            print("\n🎯 Latency Distribution:")
            under_50 = sum(1 for l in self.latencies if l < 50)
            under_100 = sum(1 for l in self.latencies if 50 <= l < 100)
            under_200 = sum(1 for l in self.latencies if 100 <= l < 200)
            over_200 = sum(1 for l in self.latencies if l >= 200)
            
            total = len(self.latencies)
            print(f"   < 50 ms:     {under_50:4} ({under_50/total*100:.1f}%)")
            print(f"   50-100 ms:   {under_100:4} ({under_100/total*100:.1f}%)")
            print(f"   100-200 ms:  {under_200:4} ({under_200/total*100:.1f}%)")
            print(f"   > 200 ms:    {over_200:4} ({over_200/total*100:.1f}%)")
            
            # Performance rating
            avg_latency = statistics.mean(self.latencies)
            if avg_latency < 50:
                rating = "🌟 EXCELLENT"
            elif avg_latency < 100:
                rating = "✅ GOOD"
            elif avg_latency < 200:
                rating = "⚠️  ACCEPTABLE"
            else:
                rating = "❌ POOR"
            
            print(f"\n🏆 Performance Rating: {rating}")
        else:
            print("\n⚠️  No messages received during test period")
            print("   Make sure sensors are running!")
        
        print("="*70 + "\n")

if __name__ == "__main__":
    tester = LatencyTester()
    tester.run_test()
