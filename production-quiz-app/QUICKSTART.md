# Quick Start Guide - Production Quiz App

Get the application running in under 5 minutes!

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Git** installed
- **8GB RAM** recommended
- **10GB disk space** available

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/production-quiz-app.git
cd production-quiz-app
```

## 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env.development

# Edit .env.development (optional - defaults work for development)
nano .env.development
```

**Minimal .env.development:**
```bash
SECRET_KEY=dev-secret-key-change-in-production
POSTGRES_PASSWORD=devpassword123
REDIS_PASSWORD=devredis123
```

## 3. Start Services

```bash
# Build and start all services (PostgreSQL, Redis, Flask, Nginx)
docker-compose up -d

# Wait 30 seconds for services to initialize
```

## 4. Initialize Database

```bash
# Run database migrations
docker-compose exec web flask db upgrade

# Seed sample data (3 quizzes, 40 questions)
docker-compose exec web python scripts/seed_data.py
```

## 5. Access Application

- **Application**: http://localhost (or http://localhost:8000)
- **Health Check**: http://localhost:8000/health
- **API Docs**: Coming soon

## 6. Test the Application

### Create Test Account
1. Visit http://localhost/auth/register
2. Fill in:
   - Username: testuser
   - Email: test@example.com
   - Password: TestPass123
3. Click "Register"
4. Skip email verification (development mode)

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f nginx
```

## 7. Stop Services

```bash
# Stop services
docker-compose down

# Stop and remove data (WARNING: Deletes database)
docker-compose down -v
```

---

## Useful Commands

### Service Management
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart web

# View service status
docker-compose ps

# View resource usage
docker stats
```

### Database Operations
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U quiz_user -d quiz_app

# Backup database
docker-compose exec web /app/scripts/backup_db.sh

# Restore database
docker-compose exec web /app/scripts/restore_db.sh /app/backups/quiz_app_backup_20240101_120000.sql.gz

# Run migrations
docker-compose exec web flask db upgrade

# Create new migration
docker-compose exec web flask db migrate -m "Description"

# Seed data
docker-compose exec web python scripts/seed_data.py
```

### Testing
```bash
# Run all tests
docker-compose exec web pytest tests/ -v

# Run with coverage
docker-compose exec web pytest tests/ --cov=app --cov-report=html

# Run specific test file
docker-compose exec web pytest tests/unit/test_models.py -v

# Open coverage report
# Windows: start htmlcov/index.html
# Mac: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

### Application Shell
```bash
# Flask shell (interactive Python)
docker-compose exec web flask shell

# Bash shell in container
docker-compose exec web bash

# PostgreSQL shell
docker-compose exec postgres psql -U quiz_user -d quiz_app

# Redis CLI
docker-compose exec redis redis-cli -a your-redis-password
```

---

## Common Issues

### Port Already in Use
```bash
# Check what's using port 80
# Windows:
netstat -ano | findstr :80

# Linux/Mac:
lsof -i :80

# Change ports in docker-compose.yml if needed
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Permission Denied
```bash
# Fix directory permissions
sudo chown -R $USER:$USER logs/ instance/ backups/

# Make scripts executable
chmod +x scripts/*.sh
```

### Services Won't Start
```bash
# View logs for errors
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up -d --build --force-recreate

# Clear all Docker resources (WARNING: Nuclear option)
docker system prune -a --volumes
```

---

## Development Workflow

### 1. Make Code Changes
Edit files in `app/` directory. Changes are reflected immediately (hot reload enabled in development).

### 2. Add Database Changes
```bash
# Modify models in app/models/
# Create migration
docker-compose exec web flask db migrate -m "Add new field"

# Apply migration
docker-compose exec web flask db upgrade
```

### 3. Run Tests
```bash
docker-compose exec web pytest tests/ -v
```

### 4. Check Code Quality
```bash
# Format code
docker-compose exec web black app/ tests/

# Sort imports
docker-compose exec web isort app/ tests/

# Lint
docker-compose exec web flake8 app/ tests/
```

### 5. Commit Changes
```bash
git add .
git commit -m "Description of changes"
git push origin your-branch
```

---

## API Endpoints

### Authentication
- `POST /auth/register` - Create account
- `POST /auth/login` - Login
- `GET /auth/logout` - Logout
- `GET /auth/verify/<token>` - Verify email
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password/<token>` - Reset password
- `GET /auth/profile` - View profile
- `POST /auth/profile` - Update profile
- `POST /auth/change-password` - Change password

### System
- `GET /` - Root endpoint
- `GET /health` - Health check

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Flask secret key |
| `FLASK_ENV` | No | development | Environment (development/production) |
| `DATABASE_URL` | No | PostgreSQL | Database connection string |
| `REDIS_URL` | No | Redis | Redis connection string |
| `POSTGRES_DB` | No | quiz_app | PostgreSQL database name |
| `POSTGRES_USER` | No | quiz_user | PostgreSQL username |
| `POSTGRES_PASSWORD` | Yes | - | PostgreSQL password |
| `REDIS_PASSWORD` | Yes | - | Redis password |
| `LOG_LEVEL` | No | INFO | Logging level |
| `SENTRY_DSN` | No | - | Sentry error tracking DSN |

---

## Next Steps

- **Add Quiz Content**: Run `/quiz-content-agent` to generate more questions
- **Customize Templates**: Edit files in `app/templates/`
- **Add Features**: Use `/backend-agent` for new functionality
- **Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment

---

## Getting Help

- **Documentation**: [README.md](README.md), [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: GitHub Issues
- **Logs**: `docker-compose logs -f`
- **Health Check**: http://localhost:8000/health

---

**Enjoy building with Production Quiz App!** 🚀
