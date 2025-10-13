"""
Battery Life Simulation Script
Analyzes battery consumption based on message transmission rates
"""

import json
import math

class BatterySimulator:
    def __init__(self, config_file='../sensors/sensor_config.json'):
        """Initialize battery simulator"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.battery_config = self.config['battery']
        self.sensors = self.config['sensors']
    
    def calculate_battery_life(self, sensor_type, sampling_rate=None):
        """Calculate battery life for a sensor"""
        sensor_cfg = self.sensors[sensor_type]
        
        # Use custom sampling rate or default
        rate = sampling_rate if sampling_rate else sensor_cfg['sampling_rate']
        
        # Messages per hour
        messages_per_hour = 3600 / rate
        
        # Battery drain per hour
        drain_per_message = self.battery_config['drain_per_message']
        drain_per_hour = messages_per_hour * drain_per_message
        
        # Total battery life in hours
        initial_charge = self.battery_config['initial_charge']
        battery_life_hours = initial_charge / drain_per_hour
        
        # Convert to days
        battery_life_days = battery_life_hours / 24
        
        return {
            'sensor_type': sensor_type,
            'sampling_rate': rate,
            'messages_per_hour': messages_per_hour,
            'messages_per_day': messages_per_hour * 24,
            'drain_per_hour': drain_per_hour,
            'battery_life_hours': battery_life_hours,
            'battery_life_days': battery_life_days
        }
    
    def optimize_sampling_rate(self, sensor_type, target_days):
        """Find optimal sampling rate for target battery life"""
        initial_charge = self.battery_config['initial_charge']
        drain_per_message = self.battery_config['drain_per_message']
        
        # Target hours
        target_hours = target_days * 24
        
        # Calculate required drain per hour
        drain_per_hour = initial_charge / target_hours
        
        # Calculate messages per hour
        messages_per_hour = drain_per_hour / drain_per_message
        
        # Calculate sampling rate
        optimal_rate = 3600 / messages_per_hour
        
        return optimal_rate
    
    def compare_scenarios(self):
        """Compare different sampling rate scenarios"""
        print("="*80)
        print(" 🔋 BATTERY LIFE SIMULATION - IoT Monitoring System")
        print("="*80)
        print(f"\n⚙️  Configuration:")
        print(f"   Initial Battery Charge: {self.battery_config['initial_charge']}%")
        print(f"   Drain per Message:      {self.battery_config['drain_per_message']}%")
        print("\n" + "="*80)
        
        # Scenario 1: Current configuration
        print("\n📊 SCENARIO 1: Current Configuration")
        print("-" * 80)
        
        for sensor_type in self.sensors:
            if self.sensors[sensor_type]['enabled']:
                result = self.calculate_battery_life(sensor_type)
                print(f"\n{sensor_type.upper()} Sensor:")
                print(f"   Sampling Rate:      every {result['sampling_rate']} seconds")
                print(f"   Messages per Day:   {result['messages_per_day']:.0f}")
                print(f"   Battery Life:       {result['battery_life_days']:.1f} days "
                      f"({result['battery_life_hours']:.1f} hours)")
        
        # Scenario 2: Optimized for 30 days
        print("\n" + "="*80)
        print("\n📊 SCENARIO 2: Optimized for 30-Day Battery Life")
        print("-" * 80)
        
        target_days = 30
        for sensor_type in self.sensors:
            if self.sensors[sensor_type]['enabled']:
                optimal_rate = self.optimize_sampling_rate(sensor_type, target_days)
                result = self.calculate_battery_life(sensor_type, optimal_rate)
                
                print(f"\n{sensor_type.upper()} Sensor:")
                print(f"   Required Sampling Rate: every {optimal_rate:.1f} seconds")
                print(f"   Messages per Day:       {result['messages_per_day']:.0f}")
                print(f"   Battery Life:           {result['battery_life_days']:.1f} days")
        
        # Scenario 3: High-frequency monitoring (1-second intervals)
        print("\n" + "="*80)
        print("\n📊 SCENARIO 3: High-Frequency Monitoring (Every 1 Second)")
        print("-" * 80)
        
        for sensor_type in self.sensors:
            if self.sensors[sensor_type]['enabled']:
                result = self.calculate_battery_life(sensor_type, 1)
                print(f"\n{sensor_type.upper()} Sensor:")
                print(f"   Sampling Rate:      every 1 second")
                print(f"   Messages per Day:   {result['messages_per_day']:.0f}")
                print(f"   Battery Life:       {result['battery_life_days']:.2f} days "
                      f"({result['battery_life_hours']:.1f} hours)")
        
        # Scenario 4: Low-power mode (60-second intervals)
        print("\n" + "="*80)
        print("\n📊 SCENARIO 4: Low-Power Mode (Every 60 Seconds)")
        print("-" * 80)
        
        for sensor_type in self.sensors:
            if self.sensors[sensor_type]['enabled']:
                result = self.calculate_battery_life(sensor_type, 60)
                print(f"\n{sensor_type.upper()} Sensor:")
                print(f"   Sampling Rate:      every 60 seconds")
                print(f"   Messages per Day:   {result['messages_per_day']:.0f}")
                print(f"   Battery Life:       {result['battery_life_days']:.1f} days")
        
        # Recommendations
        print("\n" + "="*80)
        print("\n💡 RECOMMENDATIONS")
        print("-" * 80)
        print("\n1. For Real-time Monitoring (< 5 second intervals):")
        print("   - Expect battery replacement every 2-4 days")
        print("   - Best for: Critical monitoring, testing, demonstrations")
        
        print("\n2. For Balanced Performance (10-30 second intervals):")
        print("   - Battery life: 7-20 days")
        print("   - Best for: Regular monitoring, most applications")
        
        print("\n3. For Long Battery Life (60+ second intervals):")
        print("   - Battery life: 30+ days")
        print("   - Best for: Trend analysis, low-maintenance deployments")
        
        print("\n4. Optimization Strategies:")
        print("   - Use adaptive sampling (higher rate during events)")
        print("   - Implement sleep modes between readings")
        print("   - Compress data or send only changes")
        print("   - Use solar/rechargeable batteries for continuous operation")
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    import os
    
    # Adjust path to find config file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'sensors', 'sensor_config.json')
    
    simulator = BatterySimulator(config_path)
    simulator.compare_scenarios()
