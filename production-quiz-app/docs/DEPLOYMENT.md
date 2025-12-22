# Deployment Guide

This guide covers deploying the Production Quiz App to various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Docker Deployment](#docker-deployment)
- [Manual Deployment](#manual-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Database Migration](#database-migration)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum:**
- 2 CPU cores
- 2GB RAM
- 20GB disk space
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+

**Recommended:**
- 4 CPU cores
- 4GB RAM
- 50GB SSD
- Ubuntu 22.04 LTS

### Software Dependencies

- **Docker** 20.10+ and Docker Compose 2.0+
- **PostgreSQL** 15+
- **Redis** 7+
- **Nginx** 1.18+
- **Python** 3.9+

### Domain & SSL

- Domain name (e.g., `quiz-app.com`)
- SSL certificate (Let's Encrypt recommended)

---

## Environment Configuration

### 1. Create Environment Files

```bash
# Production environment
cp .env.example .env.production
```

### 2. Configure `.env.production`

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
DEBUG=False

# Database
DATABASE_URL=postgresql://quiz_user:secure_password@postgres:5432/quiz_app_prod
SQLALCHEMY_ECHO=False

# Redis
REDIS_URL=redis://redis:6379/0

# Session
SESSION_TYPE=redis
SESSION_PERMANENT=True
SESSION_USE_SIGNER=True
PERMANENT_SESSION_LIFETIME=604800  # 7 days in seconds

# Security
CSRF_ENABLED=True
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=None

# Email (configure for your provider)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@quiz-app.com

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://redis:6379/1
RATELIMIT_STRATEGY=fixed-window

# Sentry (optional - for error tracking)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project

# Application
APP_NAME="Production Quiz App"
APP_URL=https://quiz-app.com
```

### 3. Generate Secure Keys

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Generate database password
openssl rand -base64 32
```

---

## Docker Deployment

### Option 1: Docker Compose (Recommended)

**1. Clone Repository**

```bash
git clone https://github.com/your-username/production-quiz-app.git
cd production-quiz-app
```

**2. Configure Environment**

```bash
cp .env.example .env.production
nano .env.production  # Edit configuration
```

**3. Start Services**

```bash
# Pull latest images
docker-compose -f deployment/docker/docker-compose.yml pull

# Start all services
docker-compose -f deployment/docker/docker-compose.yml up -d

# View logs
docker-compose -f deployment/docker/docker-compose.yml logs -f
```

**4. Run Database Migrations**

```bash
docker-compose -f deployment/docker/docker-compose.yml exec web flask db upgrade
```

**5. Seed Initial Data (Optional)**

```bash
docker-compose -f deployment/docker/docker-compose.yml exec web python scripts/seed_data.py
```

**6. Create Admin User**

```bash
docker-compose -f deployment/docker/docker-compose.yml exec web flask create-admin \
  --username admin \
  --email admin@quiz-app.com \
  --password SecureAdminPass123
```

### Option 2: Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c deployment/docker/docker-compose.yml quiz-app

# Check services
docker service ls

# Scale web service
docker service scale quiz-app_web=3
```

### Option 3: Kubernetes

```bash
# Apply configurations
kubectl apply -f deployment/kubernetes/

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/quiz-app-web
```

---

## Manual Deployment

### 1. Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip \
  postgresql-15 postgresql-contrib redis-server nginx

# Start services
sudo systemctl start postgresql redis-server nginx
sudo systemctl enable postgresql redis-server nginx
```

### 2. Create Database

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE quiz_app_prod;
CREATE USER quiz_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE quiz_app_prod TO quiz_user;
\q
```

### 3. Setup Application

```bash
# Create application user
sudo useradd -m -s /bin/bash quiz-app
sudo su - quiz-app

# Clone repository
git clone https://github.com/your-username/production-quiz-app.git
cd production-quiz-app

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements/production.txt

# Configure environment
cp .env.example .env.production
nano .env.production  # Edit configuration

# Run migrations
export FLASK_APP=run.py
flask db upgrade

# Seed data
python scripts/seed_data.py
```

### 4. Configure Gunicorn

Create `/etc/systemd/system/quiz-app.service`:

```ini
[Unit]
Description=Production Quiz App
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=quiz-app
Group=quiz-app
WorkingDirectory=/home/quiz-app/production-quiz-app
Environment="PATH=/home/quiz-app/production-quiz-app/venv/bin"
Environment="FLASK_ENV=production"
EnvironmentFile=/home/quiz-app/production-quiz-app/.env.production
ExecStart=/home/quiz-app/production-quiz-app/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/home/quiz-app/production-quiz-app/quiz-app.sock \
    --access-logfile /var/log/quiz-app/access.log \
    --error-logfile /var/log/quiz-app/error.log \
    --log-level info \
    "app:create_app('production')"
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
KillSignal=SIGQUIT
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Start service:**

```bash
# Create log directory
sudo mkdir -p /var/log/quiz-app
sudo chown quiz-app:quiz-app /var/log/quiz-app

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable quiz-app
sudo systemctl start quiz-app
sudo systemctl status quiz-app
```

### 5. Configure Nginx

Create `/etc/nginx/sites-available/quiz-app`:

```nginx
upstream quiz_app {
    server unix:/home/quiz-app/production-quiz-app/quiz-app.sock fail_timeout=0;
}

server {
    listen 80;
    server_name quiz-app.com www.quiz-app.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name quiz-app.com www.quiz-app.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/quiz-app.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/quiz-app.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Client upload size
    client_max_body_size 10M;

    # Static files
    location /static {
        alias /home/quiz-app/production-quiz-app/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Application
    location / {
        proxy_pass http://quiz_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/quiz-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d quiz-app.com -d www.quiz-app.com

# Test renewal
sudo certbot renew --dry-run
```

---

## Cloud Platforms

### AWS (EC2 + RDS + ElastiCache)

**1. Launch EC2 Instance**
- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.medium
- Security Group: Allow 80, 443, 22

**2. Create RDS Database**
```
Engine: PostgreSQL 15
Instance: db.t3.micro
Storage: 20GB SSD
```

**3. Create ElastiCache**
```
Engine: Redis 7.x
Node Type: cache.t3.micro
```

**4. Deploy Application**
```bash
# SSH to EC2
ssh -i key.pem ubuntu@ec2-instance

# Follow manual deployment steps above
# Update DATABASE_URL and REDIS_URL to AWS endpoints
```

### Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create production-quiz-app

# Add addons
heroku addons:create heroku-postgresql:mini
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Deploy
git push heroku main

# Run migrations
heroku run flask db upgrade

# Open app
heroku open
```

### DigitalOcean App Platform

**1. Create App**
- Connect GitHub repository
- Select Python buildpack
- Add PostgreSQL and Redis databases

**2. Environment Variables**
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=${db.DATABASE_URL}
REDIS_URL=${redis.REDIS_URL}
```

**3. Deploy**
- Auto-deploys on push to main

### Google Cloud Platform (GCP)

```bash
# Install gcloud CLI
# Deploy to Cloud Run
gcloud run deploy quiz-app \
  --image gcr.io/project-id/quiz-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Database Migration

### From SQLite to PostgreSQL

```bash
# Export SQLite data
python scripts/migrate_sqlite_to_pg.py --export

# Import to PostgreSQL
python scripts/migrate_sqlite_to_pg.py --import
```

### Zero-Downtime Migrations

```bash
# 1. Create backup
pg_dump quiz_app_prod > backup_$(date +%Y%m%d).sql

# 2. Test migrations
flask db upgrade --dry-run

# 3. Run migrations
flask db upgrade

# 4. Verify
flask db current
```

---

## Monitoring & Logging

### Application Logs

```bash
# Docker
docker-compose logs -f web

# Systemd
sudo journalctl -u quiz-app -f

# Log rotation
sudo nano /etc/logrotate.d/quiz-app
```

### Database Monitoring

```bash
# PostgreSQL stats
psql -U quiz_user -d quiz_app_prod -c "SELECT * FROM pg_stat_database WHERE datname='quiz_app_prod';"

# Slow queries
psql -U quiz_user -d quiz_app_prod -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
```

### Redis Monitoring

```bash
redis-cli INFO
redis-cli MONITOR
```

### Health Checks

```bash
# Application
curl https://quiz-app.com/health

# Database
pg_isready -h localhost -U quiz_user

# Redis
redis-cli ping
```

---

## Troubleshooting

### Common Issues

**1. Application won't start**
```bash
# Check logs
docker-compose logs web
sudo journalctl -u quiz-app -n 50

# Verify environment variables
env | grep FLASK

# Test database connection
psql $DATABASE_URL -c "SELECT 1;"
```

**2. Database connection errors**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify credentials
psql -U quiz_user -d quiz_app_prod -W

# Check connections
SELECT count(*) FROM pg_stat_activity;
```

**3. High memory usage**
```bash
# Reduce Gunicorn workers
--workers 2

# Enable connection pooling
# In config.py:
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 10
```

**4. Slow performance**
```bash
# Enable query logging
SQLALCHEMY_ECHO = True

# Add database indexes
flask db revision -m "add indexes"

# Increase Gunicorn workers
--workers $(( 2 * $(nproc) + 1 ))
```

---

## Rollback Procedure

```bash
# 1. Stop application
sudo systemctl stop quiz-app

# 2. Restore database
psql quiz_app_prod < backup_$(date +%Y%m%d).sql

# 3. Revert code
git checkout previous-stable-commit

# 4. Restart
sudo systemctl start quiz-app
```

---

## Security Checklist

- [ ] SECRET_KEY is randomly generated
- [ ] Database passwords are strong (20+ characters)
- [ ] SSL/TLS enabled (HTTPS only)
- [ ] Firewall configured (only ports 80, 443, 22 open)
- [ ] SSH key authentication (password auth disabled)
- [ ] Regular security updates (`apt update && apt upgrade`)
- [ ] Database backups automated
- [ ] Sentry configured for error tracking
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] Security headers configured
- [ ] Environment variables not in version control
- [ ] `.env` files have restrictive permissions (600)

---

## Backup Strategy

```bash
# Daily database backup
0 2 * * * pg_dump quiz_app_prod | gzip > /backups/quiz_app_$(date +\%Y\%m\%d).sql.gz

# Keep 30 days of backups
find /backups -name "quiz_app_*.sql.gz" -mtime +30 -delete

# Backup to S3
aws s3 sync /backups s3://quiz-app-backups/
```

---

## Next Steps

1. Set up monitoring with Prometheus/Grafana
2. Configure CDN (Cloudflare, AWS CloudFront)
3. Implement autoscaling
4. Set up staging environment
5. Configure CI/CD pipeline
6. Implement blue-green deployment

---

## Support

For deployment issues:
- Check logs first: `/var/log/quiz-app/`
- Review [Troubleshooting](#troubleshooting) section
- Open an issue with `deployment` label
