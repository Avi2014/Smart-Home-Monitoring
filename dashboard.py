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

# Suppress the MQTT thread warning
warnings.filterwarnings('ignore', message='.*missing ScriptRunContext.*')

# Configure page
st.set_page_config(
    page_title="IoT Sensor Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
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
        self.temperature_data = deque(maxlen=50)
        self.humidity_data = deque(maxlen=50)
        self.co2_data = deque(maxlen=50)
        self.light_data = deque(maxlen=50)
        self.last_update = None
        self.message_count = 0
        self.connected = False
        self.battery_levels = {}
    
    def add_data(self, sensor_type, value, timestamp, battery):
        with self.lock:
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
            self.message_count += 1
    
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
                'connected': self.connected
            }
    
    def set_connected(self, status):
        with self.lock:
            self.connected = status
    
    def clear_all(self):
        with self.lock:
            self.temperature_data.clear()
            self.humidity_data.clear()
            self.co2_data.clear()
            self.light_data.clear()
            self.message_count = 0
            self.last_update = None

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
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
    else:
        data_store.set_connected(False)

def on_disconnect(client, userdata, disconnect_flags, rc, properties=None):
    """Callback when disconnected from MQTT broker"""
    data_store.set_connected(False)

def on_message(client, userdata, msg):
    """Callback when message is received"""
    try:
        payload = json.loads(msg.payload.decode())
        sensor_type = payload.get('sensor_type')
        value = payload.get('value')
        timestamp = payload.get('timestamp')
        battery = payload.get('battery_level', 100)
        
        data_store.add_data(sensor_type, value, timestamp, battery)
        
    except Exception as e:
        pass

# Start MQTT client in background
@st.cache_resource
def get_mqtt_client():
    """Create and start MQTT client"""
    client = mqtt.Client(
        client_id="dashboard_viewer",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        # Give it a moment to connect
        time.sleep(1)
        return client
    except Exception as e:
        data_store.set_connected(False)
        return None

# Initialize MQTT
mqtt_client = get_mqtt_client()

# Dashboard Header
st.title("🏠 Smart Home Environment Monitoring")
st.markdown("### Real-time IoT Sensor Dashboard - Hostel Room 1")

# Get current stats
stats = data_store.get_stats()

# Status bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    is_connected = stats['connected']
    status = "🟢 Connected" if is_connected else "🔴 Disconnected"
    st.metric("MQTT Status", status)
    if not is_connected:
        if st.button("🔄 Reconnect"):
            st.cache_resource.clear()
            st.rerun()
with col2:
    st.metric("Messages Received", stats['message_count'])
with col3:
    last_update = stats['last_update'].strftime("%H:%M:%S") if stats['last_update'] else "N/A"
    st.metric("Last Update", last_update)
with col4:
    st.metric("Broker", MQTT_BROKER)

st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Dashboard Settings")
    
    st.subheader("🔋 Battery Status")
    for sensor, battery in stats['battery_levels'].items():
        emoji = "🔋" if battery > 20 else "⚠️"
        st.progress(battery / 100, text=f"{emoji} {sensor.capitalize()}: {battery:.1f}%")
    
    st.divider()
    
    st.subheader("📊 Data Info")
    st.write(f"Temperature points: {len(data_store.get_data('temperature'))}")
    st.write(f"Humidity points: {len(data_store.get_data('humidity'))}")
    st.write(f"CO2 points: {len(data_store.get_data('co2'))}")
    st.write(f"Light points: {len(data_store.get_data('light'))}")
    
    st.divider()
    
    if st.button("🔄 Clear Data"):
        data_store.clear_all()
        st.rerun()
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
    
    fig.update_layout(
        title=f"{title} Trend",
        xaxis_title="Time",
        yaxis_title=unit,
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
        use_container_width=True
    )

with gauge_col2:
    hum_data = data_store.get_data('humidity')
    hum_val = hum_data[-1]['value'] if hum_data else 50
    st.plotly_chart(
        create_gauge(hum_val, "💧 Humidity", 0, 100, "%", [40, 60]),
        use_container_width=True
    )

with gauge_col3:
    co2_data = data_store.get_data('co2')
    co2_val = co2_data[-1]['value'] if co2_data else 600
    st.plotly_chart(
        create_gauge(co2_val, "🌫️ CO2", 400, 2000, "ppm", [400, 1000]),
        use_container_width=True
    )

with gauge_col4:
    light_data = data_store.get_data('light')
    light_val = light_data[-1]['value'] if light_data else 400
    st.plotly_chart(
        create_gauge(light_val, "💡 Light", 0, 1000, "lux", [200, 800]),
        use_container_width=True
    )

st.divider()

# Trend Charts Section
st.subheader("📈 Historical Trends")

trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    st.plotly_chart(
        create_trend_chart(data_store.get_data('temperature'), "Temperature", "#FF6B6B", "°C"),
        use_container_width=True
    )
    st.plotly_chart(
        create_trend_chart(data_store.get_data('co2'), "CO2 Level", "#95E1D3", "ppm"),
        use_container_width=True
    )

with trend_col2:
    st.plotly_chart(
        create_trend_chart(data_store.get_data('humidity'), "Humidity", "#4ECDC4", "%"),
        use_container_width=True
    )
    st.plotly_chart(
        create_trend_chart(data_store.get_data('light'), "Light Level", "#FFE66D", "lux"),
        use_container_width=True
    )

# Auto-refresh
st.markdown("---")
st.caption("🔄 Dashboard auto-refreshes every 2 seconds")

# Auto-refresh every 2 seconds
time.sleep(2)
st.rerun()
