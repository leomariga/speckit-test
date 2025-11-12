# Deployment Guide

This guide covers deploying the Markdown to PDF Converter to production environments.

## Pre-Deployment Checklist

### 1. Security Configuration

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set up Google OAuth credentials for production domain
- [ ] Configure HTTPS/SSL certificates
- [ ] Update `ALLOWED_ORIGINS` to production domains only
- [ ] Enable `Strict-Transport-Security` header
- [ ] Review and adjust rate limiting settings

### 2. Environment Variables

Create production `.env` files:

**Backend** (`backend/.env`):
```env
APP_NAME="Markdown to PDF Converter"
APP_VERSION="1.0.0"
DEBUG=false

# MongoDB
MONGODB_URI=mongodb://username:password@mongodb-host:27017/markdown_pdf?authSource=admin
MONGODB_DB=markdown_pdf

# Google OAuth
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/v1/auth/google/callback

# Security
SECRET_KEY=generate-a-secure-random-key-here
RATE_LIMIT_PER_MINUTE=60

# URLs
FRONTEND_URL=https://yourdomain.com
BACKEND_URL=https://api.yourdomain.com

# CORS
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

**Frontend** (`frontend/.env.production`):
```env
VITE_BACKEND_URL=https://api.yourdomain.com/api/v1
VITE_GOOGLE_CLIENT_ID=your-production-client-id
```

### 3. Database Setup

```bash
# Create MongoDB user
docker exec -it mongodb mongosh
use admin
db.createUser({
  user: "markdown_user",
  pwd: "secure-password",
  roles: [{ role: "readWrite", db: "markdown_pdf" }]
})

# Create indexes
use markdown_pdf
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "oauth_user_id": 1 }, { unique: true })
db.conversions.createIndex({ "user_id": 1 })
db.conversions.createIndex({ "converted_at": -1 })
```

## Deployment Options

### Option 1: Docker Compose (Recommended for Small-Medium Scale)

1. **Build and start services**:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

2. **Create production compose file** (`docker-compose.prod.yml`):
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: mongodb_prod
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    networks:
      - app-network

  backend:
    build: ./backend
    container_name: backend_prod
    restart: always
    env_file:
      - backend/.env
    depends_on:
      - mongodb
    networks:
      - app-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`api.yourdomain.com`)"
      - "traefik.http.services.backend.loadbalancer.server.port=8000"

  frontend:
    build: 
      context: ./frontend
      args:
        - VITE_BACKEND_URL=https://api.yourdomain.com/api/v1
    container_name: frontend_prod
    restart: always
    networks:
      - app-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`yourdomain.com`)"
      - "traefik.http.services.frontend.loadbalancer.server.port=80"

  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik:/etc/traefik
    networks:
      - app-network

volumes:
  mongodb_data:

networks:
  app-network:
    driver: bridge
```

3. **Configure reverse proxy (Nginx or Traefik)**

### Option 2: Kubernetes (For Large Scale)

See `k8s/` directory for Kubernetes manifests.

### Option 3: Cloud Platforms

#### AWS (ECS + RDS)
1. Push Docker images to ECR
2. Deploy using ECS Fargate
3. Use DocumentDB for MongoDB
4. Configure ALB for load balancing

#### Google Cloud (Cloud Run + Cloud SQL)
1. Build and push to GCR
2. Deploy to Cloud Run
3. Use MongoDB Atlas
4. Configure Cloud CDN

#### Azure (Container Instances + Cosmos DB)
1. Push to ACR
2. Deploy to Container Instances
3. Use Cosmos DB with MongoDB API
4. Configure Application Gateway

## Monitoring & Logging

### 1. Set up Application Monitoring

**Option A: Prometheus + Grafana**
```yaml
# Add to docker-compose.prod.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3001:3000"
  depends_on:
    - prometheus
```

**Option B: Cloud monitoring**
- AWS CloudWatch
- Google Cloud Monitoring
- Azure Monitor

### 2. Centralized Logging

**Option A: ELK Stack**
```yaml
elasticsearch:
  image: elasticsearch:8.11.0
  
logstash:
  image: logstash:8.11.0
  
kibana:
  image: kibana:8.11.0
  ports:
    - "5601:5601"
```

**Option B: Cloud logging**
- AWS CloudWatch Logs
- Google Cloud Logging
- Azure Log Analytics

### 3. Error Tracking

Integrate Sentry:

```python
# backend/src/app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    environment="production",
)
```

## Backup & Disaster Recovery

### 1. Database Backups

**Automated MongoDB backups**:
```bash
# Add to cron
0 2 * * * docker exec mongodb mongodump --out /backup/$(date +\%Y\%m\%d)
```

**Backup to S3**:
```bash
aws s3 sync /backup s3://your-backup-bucket/mongodb/
```

### 2. Application State

- Store user files in S3/GCS/Azure Blob
- Enable versioning on storage buckets
- Implement point-in-time recovery

## Performance Optimization

### 1. Frontend

- Enable CDN for static assets
- Configure browser caching
- Implement service workers for offline support
- Compress assets (Gzip/Brotli)

### 2. Backend

- Enable connection pooling for MongoDB
- Implement Redis for session storage
- Add API response caching
- Use CDN for API endpoints

### 3. Database

- Create appropriate indexes
- Monitor slow queries
- Enable MongoDB profiling
- Consider read replicas for scaling

## Security Hardening

### 1. Network Security

- Configure firewall rules
- Use private networks for services
- Enable DDoS protection
- Implement WAF (Web Application Firewall)

### 2. Secrets Management

Use secrets management service:
- AWS Secrets Manager
- Google Secret Manager
- Azure Key Vault
- HashiCorp Vault

### 3. Container Security

- Scan images for vulnerabilities
- Use non-root users in containers
- Keep base images updated
- Implement pod security policies (K8s)

## Scaling Strategy

### Horizontal Scaling

1. **Backend**: Multiple FastAPI instances behind load balancer
2. **Frontend**: CDN + multiple Nginx instances
3. **Database**: MongoDB replica set with sharding

### Vertical Scaling

- Increase container resources (CPU/Memory)
- Optimize database queries
- Implement caching layers

## Health Checks

Configure health checks for all services:

```yaml
# docker-compose.prod.yml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker images
        run: docker-compose build
      
      - name: Push to registry
        run: |
          docker tag backend:latest registry.example.com/backend:latest
          docker push registry.example.com/backend:latest
      
      - name: Deploy to production
        run: |
          ssh production "cd /app && docker-compose pull && docker-compose up -d"
```

## Post-Deployment

### 1. Smoke Tests

```bash
# Check health endpoints
curl https://api.yourdomain.com/api/v1/health

# Test authentication
curl https://api.yourdomain.com/api/v1/auth/google

# Test conversion (with auth token)
curl -X POST https://api.yourdomain.com/api/v1/conversions \
  -H "Authorization: Bearer token" \
  -d '{"input_type":"text","page_count":1,"conversion_method":"client"}'
```

### 2. Monitoring Setup

- Configure alerts for error rates
- Set up uptime monitoring
- Monitor resource usage
- Track API response times

### 3. Documentation

- Update API documentation
- Document deployment procedures
- Create runbooks for common issues
- Update changelog

## Rollback Plan

In case of issues:

```bash
# Quick rollback using Docker tags
docker-compose down
docker-compose -f docker-compose.prod.yml up -d --no-deps backend:previous-version

# Or using git
git revert HEAD
docker-compose up -d --build
```

## Support & Maintenance

### Regular Tasks

- [ ] Weekly: Review error logs
- [ ] Weekly: Check database backups
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review security advisories
- [ ] Quarterly: Performance audit
- [ ] Quarterly: Cost optimization review

### Incident Response

1. Receive alert
2. Check monitoring dashboards
3. Review recent logs
4. Identify root cause
5. Apply fix or rollback
6. Post-mortem documentation

## Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vue 3 Production Deployment](https://vuejs.org/guide/best-practices/production-deployment.html)
- [MongoDB Production Checklist](https://docs.mongodb.com/manual/administration/production-checklist/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)

