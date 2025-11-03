"""
Real-time IoT Sensor Dashboard
Displays live sensor data from MQTT in a beautiful web interface
"""

import streamlit as st
import paho.mqtt.client as mqtt
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
from collections import deque
import threading
import warnings
import os
import ssl
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Suppress the MQTT thread warning
warnings.filterwarnings('ignore', message='.*missing ScriptRunContext.*')

# Configure page
st.set_page_config(
    page_title="IoT Sensor Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MQTT Configuration - Load from environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER", "95c2f02d61404267847ebc19552f72b0.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)
MQTT_USE_TLS = os.getenv("MQTT_USE_TLS", "true").lower() == "true"

MQTT_TOPICS = [
    "hostel/room1/temperature",
    "hostel/room1/humidity",
    "hostel/room1/co2",
    "hostel/room1/light"
]

# Global data storage (thread-safe using threading.Lock)
class DataStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.temperature_data = deque(maxlen=100)
        self.humidity_data = deque(maxlen=100)
        self.co2_data = deque(maxlen=100)
        self.light_data = deque(maxlen=100)
        self.last_update = None
        self.message_count = 0
        self.connected = False
        self.battery_levels = {}
        self.last_message_time = datetime.now()
        self.reconnect_count = 0
    
    def add_data(self, sensor_type, value, timestamp, battery):
        with self.lock:
            try:
                data_point = {
                    'time': datetime.fromisoformat(timestamp.replace('Z', '')),
                    'value': value
                }
                
                if sensor_type == 'temperature':
                    self.temperature_data.append(data_point)
                    self.battery_levels['temperature'] = battery
                elif sensor_type == 'humidity':
                    self.humidity_data.append(data_point)
                    self.battery_levels['humidity'] = battery
                elif sensor_type == 'co2':
                    self.co2_data.append(data_point)
                    self.battery_levels['co2'] = battery
                elif sensor_type == 'light':
                    self.light_data.append(data_point)
                    self.battery_levels['light'] = battery
                
                self.last_update = datetime.now()
                self.last_message_time = datetime.now()
                self.message_count += 1
            except Exception as e:
                print(f"Error adding data: {e}")
    
    def get_data(self, sensor_type):
        with self.lock:
            if sensor_type == 'temperature':
                return list(self.temperature_data)
            elif sensor_type == 'humidity':
                return list(self.humidity_data)
            elif sensor_type == 'co2':
                return list(self.co2_data)
            elif sensor_type == 'light':
                return list(self.light_data)
            return []
    
    def get_stats(self):
        with self.lock:
            return {
                'message_count': self.message_count,
                'last_update': self.last_update,
                'battery_levels': self.battery_levels.copy(),
                'connected': self.connected,
                'last_message_time': self.last_message_time,
                'reconnect_count': self.reconnect_count
            }
    
    def set_connected(self, status):
        with self.lock:
            self.connected = status
    
    def increment_reconnect(self):
        with self.lock:
            self.reconnect_count += 1
    
    def clear_all(self):
        with self.lock:
            self.temperature_data.clear()
            self.humidity_data.clear()
            self.co2_data.clear()
            self.light_data.clear()
            self.message_count = 0
            self.last_update = None
            self.battery_levels.clear()

# Create global data store
@st.cache_resource
def get_data_store():
    return DataStore()

data_store = get_data_store()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        data_store.set_connected(True)
        print(f"✅ Connected to MQTT broker successfully")
        for topic in MQTT_TOPICS:
            result = client.subscribe(topic, qos=1)
            print(f"Subscribed to {topic}: {result}")
    else:
        data_store.set_connected(False)
        print(f"❌ Connection failed with code {rc}")

def on_disconnect(client, userdata, disconnect_flags, rc, properties=None):
    """Callback when disconnected from MQTT broker"""
    data_store.set_connected(False)
    print(f"⚠️ Disconnected with code {rc}")
    
    # Auto-reconnect with backoff
    if rc != 0:
        data_store.increment_reconnect()
        print("🔄 Attempting to reconnect...")
        try:
            time.sleep(2)  # Wait before reconnecting
            client.reconnect()
            print("✅ Reconnected successfully")
        except Exception as e:
            print(f"❌ Reconnection failed: {e}")

def on_message(client, userdata, msg):
    """Callback when message is received"""
    try:
        payload = json.loads(msg.payload.decode())
        sensor_type = payload.get('sensor_type')
        value = payload.get('value')
        timestamp = payload.get('timestamp')
        battery = payload.get('battery_level', 100)
        
        # Debug print (only every 10th message to reduce spam)
        if data_store.get_stats()['message_count'] % 10 == 0:
            print(f"📊 Message #{data_store.get_stats()['message_count']}: {sensor_type} = {value}")
        
        data_store.add_data(sensor_type, value, timestamp, battery)
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

# Start MQTT client in background
@st.cache_resource
def get_mqtt_client():
    """Create and start MQTT client with TLS support"""
    try:
        # Use a unique client ID with timestamp to avoid conflicts
        client_id = f"dashboard_viewer_{int(time.time())}"
        
        client = mqtt.Client(
            client_id=client_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            protocol=mqtt.MQTTv311
            # Remove: clean_start=True  # This only works with MQTT v5
        )
        
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        
        # Set username and password if provided
        if MQTT_USERNAME and MQTT_PASSWORD:
            client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        
        # Enable TLS if required (for HiveMQ Cloud)
        if MQTT_USE_TLS:
            client.tls_set(
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
        
        # Increase keepalive and set reconnect delay
        print(f"📡 Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=120)  # Increased keepalive
        client.reconnect_delay_set(min_delay=1, max_delay=120)
        
        client.loop_start()
        
        # Wait for connection
        timeout = 10
        start = time.time()
        while not data_store.get_stats()['connected'] and (time.time() - start) < timeout:
            time.sleep(0.1)
        
        if data_store.get_stats()['connected']:
            print("✅ MQTT client started successfully")
        else:
            print("⚠️ MQTT client started but not connected yet")
        
        return client
        
    except Exception as e:
        st.error(f"MQTT Connection Error: {e}")
        print(f"❌ MQTT Error: {e}")
        data_store.set_connected(False)
        return None

# Initialize MQTT
mqtt_client = get_mqtt_client()

# Dashboard Header
st.title("🏠 Smart Home Environment Monitoring")
st.markdown("### Real-time IoT Sensor Dashboard - Hostel Room 1")

# Get current stats
stats = data_store.get_stats()

# Check if we're receiving messages
time_since_last = (datetime.now() - stats['last_message_time']).total_seconds() if stats['last_message_time'] else float('inf')

# Connection status warning
if time_since_last > 30 and mqtt_client:
    st.warning(f"⚠️ No messages received for {int(time_since_last)} seconds. Connection may be stale.")
    col_warn1, col_warn2 = st.columns(2)
    with col_warn1:
        if st.button("🔄 Force Reconnect", key="force_reconnect"):
            if mqtt_client:
                try:
                    mqtt_client.reconnect()
                    st.success("Reconnection initiated...")
                    time.sleep(2)
                except Exception as e:
                    st.error(f"Reconnect failed: {e}")
    with col_warn2:
        if st.button("🔃 Restart MQTT Client", key="restart_mqtt"):
            st.cache_resource.clear()
            st.rerun()

# Status bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    is_connected = stats['connected']
    status = "🟢 Connected" if is_connected else "🔴 Disconnected"
    st.metric("MQTT Status", status)
with col2:
    st.metric("Messages Received", stats['message_count'])
with col3:
    last_update = stats['last_update'].strftime("%H:%M:%S") if stats['last_update'] else "N/A"
    st.metric("Last Update", last_update)
with col4:
    st.metric("Reconnects", stats['reconnect_count'])

st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Dashboard Settings")
    
    # MQTT Configuration Display
    st.subheader("📡 MQTT Configuration")
    st.text(f"Broker: {MQTT_BROKER[:30]}...")
    st.text(f"Port: {MQTT_PORT}")
    st.text(f"TLS: {'✅ Enabled' if MQTT_USE_TLS else '❌ Disabled'}")
    if MQTT_USERNAME:
        st.text(f"User: {MQTT_USERNAME}")
        st.text(f"Auth: ✅ Enabled")
    
    st.divider()
    
    st.subheader("🔋 Battery Status")
    if stats['battery_levels']:
        for sensor, battery in stats['battery_levels'].items():
            emoji = "🔋" if battery > 20 else "⚠️"
            st.progress(battery / 100, text=f"{emoji} {sensor.capitalize()}: {battery:.1f}%")
    else:
        st.info("No sensor data yet")
    
    st.divider()
    
    st.subheader("📊 Data Info")
    st.write(f"Temperature: {len(data_store.get_data('temperature'))} points")
    st.write(f"Humidity: {len(data_store.get_data('humidity'))} points")
    st.write(f"CO2: {len(data_store.get_data('co2'))} points")
    st.write(f"Light: {len(data_store.get_data('light'))} points")
    
    st.divider()
    
    # Auto-refresh control
    st.subheader("🔄 Refresh Settings")
    refresh_rate = st.slider("Refresh Rate (seconds)", 1, 10, 3)
    
    st.divider()
    
    if st.button("🗑️ Clear Data"):
        data_store.clear_all()
        st.success("Data cleared!")
        time.sleep(1)
        st.rerun()
    
    st.divider()
    st.info("💡 **Tip:** Run sensor simulators to see live data!")

# Helper function to create gauge chart
def create_gauge(value, title, min_val, max_val, unit, thresholds):
    """Create a gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{title}<br><span style='font-size:0.8em'>{unit}</span>"},
        delta={'reference': (thresholds[0] + thresholds[1]) / 2},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [min_val, thresholds[0]], 'color': "lightgray"},
                {'range': [thresholds[0], thresholds[1]], 'color': "lightgreen"},
                {'range': [thresholds[1], max_val], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'size': 12}
    )
    
    return fig

# Helper function to create trend chart
def create_trend_chart(data, title, color, unit):
    """Create a trend line chart"""
    if len(data) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No data yet. Start sensors to see live data!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="gray")
        )
    else:
        df = pd.DataFrame(list(data))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['value'],
            mode='lines+markers',
            name=title,
            line=dict(color=color, width=2),
            marker=dict(size=6)
        ))
    
    # Set Y-axis range based on sensor type
    y_ranges = {
        'Temperature': [15, 40],
        'Humidity': [0, 100],
        'CO2 Level': [300, 2000],
        'Light Level': [0, 1000]
    }
    
    y_range = y_ranges.get(title, None)
    
    fig.update_layout(
        title=f"{title} Trend",
        xaxis_title="Time",
        yaxis_title=unit,
        yaxis=dict(range=y_range) if y_range else {},
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode='x unified',
        showlegend=False
    )
    
    return fig

# Current Values Section
st.subheader("📊 Current Sensor Readings")

gauge_col1, gauge_col2, gauge_col3, gauge_col4 = st.columns(4)

with gauge_col1:
    temp_data = data_store.get_data('temperature')
    temp_val = temp_data[-1]['value'] if temp_data else 22
    st.plotly_chart(
        create_gauge(temp_val, "🌡️ Temperature", 15, 40, "°C", [20, 28]),
        use_container_width=True,
        key="gauge_temp"
    )

with gauge_col2:
    hum_data = data_store.get_data('humidity')
    hum_val = hum_data[-1]['value'] if hum_data else 50
    st.plotly_chart(
        create_gauge(hum_val, "💧 Humidity", 0, 100, "%", [40, 60]),
        use_container_width=True,
        key="gauge_hum"
    )

with gauge_col3:
    co2_data = data_store.get_data('co2')
    co2_val = co2_data[-1]['value'] if co2_data else 600
    st.plotly_chart(
        create_gauge(co2_val, "🌫️ CO2", 400, 2000, "ppm", [400, 1000]),
        use_container_width=True,
        key="gauge_co2"
    )

with gauge_col4:
    light_data = data_store.get_data('light')
    light_val = light_data[-1]['value'] if light_data else 400
    st.plotly_chart(
        create_gauge(light_val, "💡 Light", 0, 1000, "lux", [200, 800]),
        use_container_width=True,
        key="gauge_light"
    )

st.divider()

# Trend Charts Section
st.subheader("📈 Historical Trends")

trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    st.plotly_chart(
        create_trend_chart(data_store.get_data('temperature'), "Temperature", "#FF6B6B", "°C"),
        use_container_width=True,
        key="trend_temp"
    )
    st.plotly_chart(
        create_trend_chart(data_store.get_data('co2'), "CO2 Level", "#95E1D3", "ppm"),
        use_container_width=True,
        key="trend_co2"
    )

with trend_col2:
    st.plotly_chart(
        create_trend_chart(data_store.get_data('humidity'), "Humidity", "#4ECDC4", "%"),
        use_container_width=True,
        key="trend_hum"
    )
    st.plotly_chart(
        create_trend_chart(data_store.get_data('light'), "Light Level", "#FFE66D", "lux"),
        use_container_width=True,
        key="trend_light"
    )

# Auto-refresh footer
st.markdown("---")
st.caption(f"🔄 Dashboard auto-refreshes every {refresh_rate} seconds | Last refresh: {datetime.now().strftime('%H:%M:%S')}")

# Auto-refresh with configurable rate
time.sleep(refresh_rate)
st.rerun()