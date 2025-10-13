# 🚀 Deployment Guide - Smart Home IoT Monitoring System

## 📋 Deployment Options

This guide covers multiple deployment scenarios for your IoT monitoring system.

---

## 🏠 Option 1: Local Deployment (Development/Testing)

### Best For:
- Testing and development
- Lab demonstrations
- Educational purposes

### Setup:

```powershell
# Clone repository
git clone https://github.com/YOUR_USERNAME/Smart-Home-Monitoring.git
cd Smart-Home-Monitoring

# Install dependencies
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start system
.\scripts\start_all.ps1
```

### Access:
- **Dashboard**: http://localhost:8501
- **Local network**: http://YOUR_IP:8501

---

## ☁️ Option 2: Streamlit Cloud (Free Dashboard Hosting)

### Best For:
- Remote access
- Sharing with others
- Portfolio projects

### Steps:

1. **Prepare Repository**
   ```powershell
   # Ensure all files are committed
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `Smart-Home-Monitoring`
   - Main file path: `dashboard.py`
   - Click "Deploy"

3. **Configure Secrets** (if using private MQTT broker)
   - Settings → Secrets
   - Add MQTT credentials:
     ```toml
     [mqtt]
     broker = "your-broker.com"
     port = 1883
     username = "your_username"
     password = "your_password"
     ```

### Access:
- **Public URL**: https://your-app.streamlit.app

### Limitations:
- Dashboard only (sensors must run locally)
- Free tier: 1 GB RAM, 1 CPU core
- App sleeps after inactivity

---

## 🐳 Option 3: Docker Deployment

### Best For:
- Production environments
- Consistent deployment
- Multi-platform support

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Start dashboard
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - MQTT_BROKER=test.mosquitto.org
      - MQTT_PORT=1883
    restart: unless-stopped

  alert-system:
    build: .
    command: python alert_system.py
    environment:
      - MQTT_BROKER=test.mosquitto.org
      - MQTT_PORT=1883
    restart: unless-stopped

  sensors:
    build: .
    command: python src/sensors/run_all_sensors.py
    environment:
      - MQTT_BROKER=test.mosquitto.org
      - MQTT_PORT=1883
    restart: unless-stopped
```

### Deploy:

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Access:
- **Dashboard**: http://localhost:8501
- **Production**: Use reverse proxy (nginx) for custom domain

---

## 🌐 Option 4: Cloud VM Deployment

### Best For:
- Full system deployment
- Production use
- Complete control

### Platforms:
- AWS EC2
- Google Cloud Compute Engine
- Azure Virtual Machine
- DigitalOcean Droplet

### Setup (Ubuntu 22.04):

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/Smart-Home-Monitoring.git
cd Smart-Home-Monitoring

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install PM2 for process management
sudo npm install -g pm2

# Create PM2 ecosystem file
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'dashboard',
      script: 'venv/bin/streamlit',
      args: 'run dashboard.py --server.address=0.0.0.0',
      autorestart: true
    },
    {
      name: 'alert-system',
      script: 'venv/bin/python',
      args: 'alert_system.py',
      autorestart: true
    },
    {
      name: 'sensors',
      script: 'venv/bin/python',
      args: 'src/sensors/run_all_sensors.py',
      autorestart: true
    }
  ]
};
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Configure firewall
sudo ufw allow 8501/tcp
sudo ufw enable
```

### Access:
- **Dashboard**: http://YOUR_VM_IP:8501

### Optional: Setup Domain & SSL

```bash
# Install Nginx
sudo apt install nginx -y

# Configure reverse proxy
sudo nano /etc/nginx/sites-available/iot-dashboard

# Add configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/iot-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Install SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Access:
- **Dashboard**: https://your-domain.com

---

## 🔐 Option 5: Private MQTT Broker

### Best For:
- Production environments
- Data privacy
- Custom configurations

### Install Mosquitto MQTT Broker:

**Ubuntu:**
```bash
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

**Windows:**
- Download from https://mosquitto.org/download/
- Install and run as service

### Configure Authentication:

```bash
# Create password file
sudo mosquitto_passwd -c /etc/mosquitto/passwd iot_user

# Edit config
sudo nano /etc/mosquitto/mosquitto.conf

# Add:
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd

# Restart
sudo systemctl restart mosquitto
```

### Update Configuration:

Edit `src/sensors/sensor_config.json`:

```json
{
  "mqtt": {
    "broker": "your-broker-ip",
    "port": 1883,
    "username": "iot_user",
    "password": "your_password",
    "use_auth": true
  }
}
```

---

## 📊 Performance Optimization

### For Large Scale Deployment:

1. **Use Redis for Caching**
   ```bash
   pip install redis
   ```

2. **Database for Historical Data**
   ```bash
   pip install influxdb-client
   ```

3. **Load Balancing** (multiple dashboard instances)
   - Use nginx upstream
   - Session sticky enabled

4. **CDN for Static Assets**
   - CloudFlare
   - AWS CloudFront

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example:

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python tests/mqtt_connection_test.py
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd Smart-Home-Monitoring
          git pull
          pm2 restart all
```

---

## 📈 Monitoring & Maintenance

### Application Monitoring:

**PM2 Dashboard:**
```bash
pm2 monit
```

**Logs:**
```bash
pm2 logs dashboard
pm2 logs alert-system
pm2 logs sensors
```

### System Monitoring:

**Install Prometheus + Grafana** (optional):
```bash
# Add monitoring metrics
pip install prometheus-client

# Configure Grafana dashboards for:
# - System resources
# - Message throughput
# - Alert frequency
# - Sensor uptime
```

---

## 🐛 Troubleshooting

### Common Issues:

**Port 8501 already in use:**
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run dashboard.py --server.port=8502
```

**MQTT connection timeout:**
- Check firewall rules
- Verify broker is running
- Test with: `mosquitto_pub -h BROKER -t test -m "hello"`

**High memory usage:**
- Reduce data retention (maxlen in dashboard.py)
- Use database for historical data
- Increase server resources

---

## ✅ Pre-Deployment Checklist

- [ ] All tests passing (`python tests/test_scenarios.py`)
- [ ] Environment variables configured
- [ ] MQTT broker accessible
- [ ] Firewall rules configured
- [ ] SSL certificate installed (if HTTPS)
- [ ] Monitoring set up
- [ ] Backup strategy defined
- [ ] Documentation updated
- [ ] Performance tested under load

---

## 📞 Support

For deployment issues:
1. Check logs: `pm2 logs` or `docker-compose logs`
2. Review configuration files
3. Test MQTT connectivity
4. Verify port availability
5. Check system resources

---

**🎉 Choose the deployment option that best fits your needs!**

For questions, see [SETUP_GUIDE.md](SETUP_GUIDE.md) or [USER_GUIDE.md](USER_GUIDE.md)
