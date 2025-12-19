# Deployment Guide - Production Quiz App

Complete deployment guide for Production Quiz App with Docker, PostgreSQL, Redis, Nginx, and CI/CD.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start (Development)](#quick-start-development)
- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [Database Management](#database-management)
- [Backup and Restore](#backup-and-restore)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended) or macOS
- **Docker**: 20.10+ with Docker Compose v2
- **Memory**: Minimum 2GB RAM, recommended 4GB+
- **Storage**: Minimum 10GB free space

### Required Software
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git curl

# macOS
brew install docker docker-compose git

# Verify installations
docker --version
docker-compose --version
```

---

## Quick Start (Development)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/production-quiz-app.git
cd production-quiz-app
```

### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env.development

# Edit environment variables
nano .env.development
```

**Minimum required variables:**
```bash
SECRET_KEY=your-secret-key-here
POSTGRES_PASSWORD=secure-database-password
REDIS_PASSWORD=secure-redis-password
```

### 3. Start Development Environment
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Run database migrations
docker-compose exec web flask db upgrade

# Seed database with sample data
docker-compose exec web python scripts/seed_data.py
```

### 4. Access Application
- **Application**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 5. Stop Services
```bash
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

---

## Production Deployment

### 1. Server Preparation

#### Update System
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

#### Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Configure Firewall
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow SSH (if not already allowed)
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable
```

### 2. Deploy Application

#### Clone Repository
```bash
cd /opt
sudo git clone https://github.com/yourusername/production-quiz-app.git
cd production-quiz-app
```

#### Configure Production Environment
```bash
# Create production environment file
sudo cp .env.example .env.production

# Edit with secure values
sudo nano .env.production
```

**Production environment template:**
```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=GENERATE-STRONG-RANDOM-KEY-HERE
DEBUG=False

# Database Configuration
POSTGRES_DB=quiz_app_prod
POSTGRES_USER=quiz_user_prod
POSTGRES_PASSWORD=STRONG-DATABASE-PASSWORD
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
DATABASE_URL=postgresql://quiz_user_prod:STRONG-DATABASE-PASSWORD@postgres:5432/quiz_app_prod

# Redis Configuration
REDIS_PASSWORD=STRONG-REDIS-PASSWORD
REDIS_URL=redis://:STRONG-REDIS-PASSWORD@redis:6379/0
SESSION_TYPE=redis
SESSION_REDIS=redis://:STRONG-REDIS-PASSWORD@redis:6379/1
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://:STRONG-REDIS-PASSWORD@redis:6379/2

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=604800

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
LOG_LEVEL=INFO

# Email (Optional)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

#### Generate Secret Key
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### SSL/TLS Certificates

**Option 1: Let's Encrypt (Recommended)**
```bash
# Install Certbot
sudo apt-get install -y certbot

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem deployment/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem deployment/nginx/ssl/key.pem
```

**Option 2: Self-Signed (Development Only)**
```bash
mkdir -p deployment/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout deployment/nginx/ssl/key.pem \
    -out deployment/nginx/ssl/cert.pem
```

### 3. Deploy with Docker Compose

```bash
# Load environment variables
set -a
source .env.production
set +a

# Build and start services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Run database migrations
docker-compose exec web flask db upgrade

# Seed initial data
docker-compose exec web python scripts/seed_data.py
```

### 4. Configure Automatic Backups

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Test backup manually
docker-compose exec web /app/scripts/backup_db.sh

# Set up cron job for daily backups at 2 AM
sudo crontab -e
```

Add this line:
```cron
0 2 * * * docker exec quiz_app_web /app/scripts/cron-backup.sh >> /var/log/backup-cron.log 2>&1
```

---

## Environment Configuration

### Development Environment (.env.development)
- SQLite or local PostgreSQL
- Debug mode enabled
- Detailed logging
- No HTTPS requirement

### Testing Environment (.env.testing)
- In-memory SQLite
- Test database isolation
- Mock external services
- Fast test execution

### Staging Environment (.env.staging)
- PostgreSQL + Redis
- Production-like setup
- Testing before production
- Separate credentials

### Production Environment (.env.production)
- PostgreSQL + Redis (production)
- HTTPS enforced
- Sentry error tracking
- Optimized performance

---

## Database Management

### Initial Setup
```bash
# Initialize database
docker-compose exec web flask db init

# Create migration
docker-compose exec web flask db migrate -m "Initial schema"

# Apply migration
docker-compose exec web flask db upgrade
```

### Migration Workflow
```bash
# After model changes, create migration
docker-compose exec web flask db migrate -m "Description of changes"

# Review migration file in migrations/versions/

# Apply migration
docker-compose exec web flask db upgrade

# Rollback if needed
docker-compose exec web flask db downgrade
```

### Seed Data
```bash
# Seed sample quizzes and questions
docker-compose exec web python scripts/seed_data.py

# Clear and reseed
docker-compose exec web python scripts/seed_data.py --clear
```

---

## Backup and Restore

### Manual Backup
```bash
# Create backup
docker-compose exec web /app/scripts/backup_db.sh /app/backups

# Backups are stored in ./backups/ directory
ls -lh backups/
```

### Restore from Backup
```bash
# List available backups
ls -lh backups/

# Restore specific backup (WARNING: Overwrites current data)
docker-compose exec web /app/scripts/restore_db.sh /app/backups/quiz_app_backup_20240101_120000.sql.gz
```

### Automated Backups
Configured via cron (see Production Deployment section).

**Backup retention:** 7 days (configurable via `RETENTION_DAYS` environment variable)

---

## Monitoring and Health Checks

### Health Check Endpoint
```bash
# Check application health
curl http://localhost:8000/health

# Response example:
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "quiz-app",
  "version": "1.0.0",
  "database": "connected",
  "cache": "connected"
}
```

### Service Status
```bash
# Check all services
docker-compose ps

# Check specific service logs
docker-compose logs -f web
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f nginx

# Monitor resource usage
docker stats
```

### Database Monitoring
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U quiz_user_prod -d quiz_app_prod

# Check database size
\l+

# List tables
\dt

# Check connections
SELECT * FROM pg_stat_activity;
```

### Redis Monitoring
```bash
# Connect to Redis
docker-compose exec redis redis-cli -a your-redis-password

# Check info
INFO

# Monitor commands in real-time
MONITOR
```

---

## CI/CD Pipeline

### GitHub Actions Workflows

**1. Continuous Integration (.github/workflows/ci.yml)**
- Runs on push to main/develop
- Executes linting (Black, isort, Flake8)
- Runs security scans (Safety, Bandit)
- Runs full test suite with coverage
- Builds Docker image
- Uploads coverage to Codecov

**2. CodeQL Security Analysis (.github/workflows/codeql.yml)**
- Runs weekly on schedule
- Scans for security vulnerabilities
- Analyzes Python and JavaScript code

### Required GitHub Secrets

Configure these in GitHub repository settings:

```
DOCKER_USERNAME       # Docker Hub username
DOCKER_PASSWORD       # Docker Hub password/token
CODECOV_TOKEN        # Codecov upload token
DEPLOY_HOST          # Production server IP/domain
DEPLOY_USER          # SSH username
DEPLOY_SSH_KEY       # SSH private key
DEPLOY_PORT          # SSH port (default: 22)
```

### Manual Deployment Trigger
```bash
# Push to main branch triggers deployment
git push origin main

# View workflow status
# Visit: https://github.com/yourusername/production-quiz-app/actions
```

---

## Troubleshooting

### Common Issues

#### 1. Container Won't Start
```bash
# Check logs
docker-compose logs web

# Restart specific service
docker-compose restart web

# Rebuild and restart
docker-compose up -d --build --force-recreate
```

#### 2. Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Verify DATABASE_URL in .env
docker-compose exec web env | grep DATABASE_URL

# Test connection manually
docker-compose exec web python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.engine.connect()"
```

#### 3. Redis Connection Failed
```bash
# Check Redis is running
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli -a your-redis-password PING

# Should return: PONG
```

#### 4. Nginx 502 Bad Gateway
```bash
# Check if web service is running
docker-compose ps web

# Check web service health
curl http://localhost:8000/health

# Check Nginx logs
docker-compose logs nginx

# Restart Nginx
docker-compose restart nginx
```

#### 5. Permission Denied Errors
```bash
# Fix ownership of directories
sudo chown -R $USER:$USER logs/ instance/ backups/

# Make scripts executable
chmod +x scripts/*.sh
```

#### 6. Migration Errors
```bash
# Check current migration status
docker-compose exec web flask db current

# Show migration history
docker-compose exec web flask db history

# Force migration stamp (if out of sync)
docker-compose exec web flask db stamp head

# Drop and recreate (WARNING: Deletes all data)
docker-compose exec web flask db downgrade base
docker-compose exec web flask db upgrade
```

### Performance Tuning

#### Gunicorn Workers
Edit `Dockerfile` CMD:
```bash
--workers 4              # CPU cores * 2 + 1
--threads 2              # Threads per worker
--worker-class gthread   # Thread worker class
--timeout 120            # Request timeout
```

#### PostgreSQL
Edit `docker-compose.yml`:
```yaml
postgres:
  command: postgres -c max_connections=200 -c shared_buffers=256MB
```

#### Redis
Edit `docker-compose.yml`:
```yaml
redis:
  command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

### Getting Help

- **Issues**: https://github.com/yourusername/production-quiz-app/issues
- **Discussions**: https://github.com/yourusername/production-quiz-app/discussions
- **Documentation**: https://github.com/yourusername/production-quiz-app/wiki

---

## Security Checklist

Before deploying to production:

- [ ] Changed all default passwords
- [ ] Generated strong SECRET_KEY
- [ ] Configured SSL/TLS certificates
- [ ] Enabled HTTPS-only (no HTTP)
- [ ] Configured firewall rules
- [ ] Set up Sentry error tracking
- [ ] Enabled automated backups
- [ ] Configured rate limiting
- [ ] Reviewed security headers
- [ ] Updated all dependencies
- [ ] Ran security scans (Bandit, Safety)
- [ ] Configured logging and monitoring
- [ ] Set up alerts for critical errors
- [ ] Documented deployment process
- [ ] Tested backup and restore procedure

---

## Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Docker Documentation**: https://docs.docker.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Nginx Documentation**: https://nginx.org/en/docs/
- **Let's Encrypt**: https://letsencrypt.org/
- **Gunicorn Documentation**: https://docs.gunicorn.org/

---

**Last Updated**: 2024-01-01
**Version**: 1.0.0
