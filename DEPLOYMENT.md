# Deployment Guide - Cryptocurrency Payment Gateway

## Quick Start (Development)

1. **Install dependencies**
```bash
pip install -r requirments.txt
```

2. **Configure wallet addresses**
```bash
cp .env.example .env
# Edit .env with your wallet addresses
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
```
http://localhost:5000
```

## Production Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Create Heroku app**
```bash
heroku create your-app-name
```

3. **Add Procfile**
```bash
echo "web: python app.py" > Procfile
```

4. **Set environment variables**
```bash
heroku config:set BTC_WALLET_ADDRESS=your_btc_address
heroku config:set ETH_WALLET_ADDRESS=your_eth_address
heroku config:set USDT_WALLET_ADDRESS=your_usdt_address
```

5. **Deploy**
```bash
git push heroku main
```

### Option 2: Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

2. **Build and run**
```bash
docker build -t housing-payment-gateway .
docker run -p 5000:5000 \
  -e BTC_WALLET_ADDRESS=your_btc_address \
  -e ETH_WALLET_ADDRESS=your_eth_address \
  -e USDT_WALLET_ADDRESS=your_usdt_address \
  housing-payment-gateway
```

### Option 3: DigitalOcean App Platform

1. **Create app.yaml**
```yaml
name: housing-payment-gateway
services:
- name: web
  github:
    repo: your-username/Housing-price-prediction
    branch: main
  run_command: python app.py
  envs:
  - key: BTC_WALLET_ADDRESS
    value: your_btc_address
  - key: ETH_WALLET_ADDRESS
    value: your_eth_address
  - key: USDT_WALLET_ADDRESS
    value: your_usdt_address
```

2. **Deploy**
```bash
doctl apps create --spec app.yaml
```

### Option 4: AWS EC2

1. **Launch EC2 instance** (Ubuntu 20.04)

2. **SSH into instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip nginx
```

4. **Clone repository**
```bash
git clone https://github.com/your-username/Housing-price-prediction.git
cd Housing-price-prediction
```

5. **Setup application**
```bash
pip3 install -r requirments.txt
cp .env.example .env
# Edit .env with your wallet addresses
```

6. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

7. **Setup systemd service**
```ini
[Unit]
Description=Housing Payment Gateway
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Housing-price-prediction
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

8. **Start service**
```bash
sudo systemctl enable housing-gateway
sudo systemctl start housing-gateway
```

## Security Checklist

- [ ] Change default wallet addresses in .env
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall (allow only 80, 443, 22)
- [ ] Implement rate limiting
- [ ] Add database for persistent storage
- [ ] Set up monitoring and logging
- [ ] Regular backups
- [ ] Integrate with blockchain APIs for verification
- [ ] Add DDoS protection
- [ ] Keep dependencies updated

## Payment Gateway Integration

For production, integrate with one of these services:

### CoinGate
```bash
pip install coingate-python
```

### CoinPayments
```bash
pip install coinpayments
```

### NOWPayments
```bash
# Use their REST API
```

## Monitoring

### Add Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Add Error Tracking (Sentry)
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

## Database Setup (Production)

Replace in-memory storage with PostgreSQL:

```bash
pip install psycopg2-binary flask-sqlalchemy
```

Update app.py to use SQLAlchemy for persistent storage.

## Testing

Run tests before deployment:
```bash
python test_api.py
```

## Support

For deployment issues, contact:
- Email: ashkanam6731@gmail.com
- GitHub Issues: https://github.com/ashkanam26/Housing-price-prediction/issues
