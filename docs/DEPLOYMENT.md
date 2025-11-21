# Deployment Guide

This guide covers various deployment scenarios for OmniForge.

## Table of Contents

- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Configuration](#environment-configuration)

---

## Local Development

### Quick Start

```bash
# Install dependencies
./scripts/install.sh

# Start development server
./scripts/start.sh --gui
```

Access:
- API: http://localhost:8000
- GUI: http://localhost:5173

---

## Production Deployment

### Prerequisites

- Python 3.8+
- Node.js 18+
- Reverse proxy (nginx recommended)
- SSL certificate

### Setup Steps

1. **Install OmniForge**

```bash
git clone https://github.com/MASSIVEMAGNETICS/build_me.git
cd build_me
./scripts/install.sh
```

2. **Configure Environment**

```bash
cp .env.example .env
# Edit .env with production settings
nano .env
```

Production settings:
```bash
DEBUG_MODE=false
API_HOST=0.0.0.0
API_PORT=8000
PARALLEL_WORKERS=8
CACHE_ENABLED=true
```

3. **Build Frontend**

```bash
npm run build
```

4. **Setup Systemd Service**

Create `/etc/systemd/system/omniforge.service`:

```ini
[Unit]
Description=OmniForge API Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/omniforge
Environment="PATH=/opt/omniforge/venv/bin"
ExecStart=/opt/omniforge/venv/bin/uvicorn src.core.api:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start Service**

```bash
sudo systemctl daemon-reload
sudo systemctl enable omniforge
sudo systemctl start omniforge
```

6. **Configure Nginx**

Create `/etc/nginx/sites-available/omniforge`:

```nginx
server {
    listen 80;
    server_name omniforge.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /opt/omniforge/static;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/omniforge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

7. **Setup SSL with Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d omniforge.yourdomain.com
```

---

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements
COPY requirements.txt .
COPY package.json .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install

# Copy application
COPY . .

# Build frontend
RUN npm run build

EXPOSE 8000

CMD ["uvicorn", "src.core.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  omniforge:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG_MODE=false
      - PARALLEL_WORKERS=4
    volumes:
      - ./logs:/app/logs
      - ./cache:/app/cache
      - ./reports:/app/reports
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - omniforge
    restart: unless-stopped
```

### Deploy with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Cloud Deployment

### AWS EC2

1. Launch EC2 instance (Ubuntu 22.04 LTS)
2. Configure security groups (ports 80, 443, 8000)
3. SSH into instance
4. Follow production deployment steps above

### AWS ECS/Fargate

1. Build and push Docker image to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure Application Load Balancer

### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/omniforge

# Deploy
gcloud run deploy omniforge \
  --image gcr.io/PROJECT_ID/omniforge \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku

```bash
# Login
heroku login

# Create app
heroku create omniforge-app

# Add buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs

# Deploy
git push heroku main
```

---

## Environment Configuration

### Production Environment Variables

```bash
# Core
DEBUG_MODE=false
API_HOST=0.0.0.0
API_PORT=8000

# Performance
PARALLEL_WORKERS=8
CACHE_ENABLED=true

# Security (if using AI features)
OPENAI_API_KEY=your_production_key
ANTHROPIC_API_KEY=your_production_key

# Monitoring
LOG_LEVEL=INFO
```

### Security Best Practices

1. **Environment Variables**
   - Never commit secrets to version control
   - Use secret management services (AWS Secrets Manager, HashiCorp Vault)
   - Rotate API keys regularly

2. **Network Security**
   - Use HTTPS in production
   - Configure firewall rules
   - Implement rate limiting
   - Use VPC/private networks

3. **Application Security**
   - Keep dependencies updated
   - Run security scans regularly
   - Implement authentication if needed
   - Use CORS appropriately

### Monitoring

1. **Logs**
```bash
# View application logs
tail -f logs/omniforge.log

# Systemd logs
journalctl -u omniforge -f
```

2. **Health Checks**
```bash
# API health
curl http://localhost:8000/health

# Detailed status
curl http://localhost:8000/api/info
```

3. **Metrics**
- Monitor CPU/memory usage
- Track request rates
- Monitor error rates
- Set up alerts

---

## Migration Guide

### From Development to Production

1. **Database** (if applicable)
   - Export development data
   - Import to production
   - Run migrations

2. **Configuration**
   - Update API endpoints
   - Configure production URLs
   - Set production secrets

3. **Testing**
   - Run full test suite
   - Perform load testing
   - Security audit

4. **Deployment**
   - Deploy backend
   - Deploy frontend
   - Update DNS
   - Test all endpoints

### Rollback Procedure

1. Keep previous version tagged
2. Revert to previous Docker image
3. Restore database backup if needed
4. Update load balancer

---

## Troubleshooting

### Common Issues

**Issue**: Server won't start
```bash
# Check logs
journalctl -u omniforge -n 50

# Verify ports
sudo netstat -tlnp | grep 8000
```

**Issue**: High memory usage
```bash
# Check processes
top
# Reduce PARALLEL_WORKERS in .env
```

**Issue**: Permission errors
```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/omniforge

# Fix permissions
chmod +x scripts/*.sh
```

---

## Support

For deployment issues:
- Check logs first
- Review configuration
- Open GitHub issue
- Contact support team

---

**Remember**: Always test deployments in staging environment first!
