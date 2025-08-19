# Deployment Guide

This document provides comprehensive instructions for deploying the Gen-AI Virtual Try-On Clothes application to various environments.

## 🚀 Quick Deployment Options

### 1. Docker (Recommended - Easiest)

**Prerequisites:**
- Docker Desktop installed
- Google Gemini API key

**Steps:**
```bash
# Clone the repository
git clone https://github.com/Ownned3389/Gen-AI-Virtual-Try-On-Clothes.git
cd Gen-AI-Virtual-Try-On-Clothes

# Copy and configure environment
cp env.example .env
# Edit .env with your Google API key

# Deploy (Windows)
deploy.bat docker

# Deploy (Linux/macOS)
./deploy.sh docker
```

**Access:** http://localhost:8000

### 2. Production with Nginx

```bash
# Deploy with nginx reverse proxy
deploy.bat production  # Windows
./deploy.sh production # Linux/macOS
```

**Access:** http://localhost (port 80)

### 3. Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/

# Check status
kubectl get pods,services,ingress
```

## 📋 Detailed Deployment Methods

### Local Development

#### Backend Setup
```bash
cd backend
pip install poetry
poetry install
cp env.example .env
# Edit .env with your API key
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment

#### Single Container
```bash
# Build and run
docker build -t gen-ai-virtual-tryon .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key gen-ai-virtual-tryon
```

#### Docker Compose
```bash
# Development
docker-compose up --build

# Production
docker-compose --profile production up --build -d
```

### Cloud Platforms

#### Heroku
```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GOOGLE_API_KEY=your_api_key
heroku config:set ENVIRONMENT=production

# Deploy
git push heroku main
```

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker build -t gen-ai-virtual-tryon .
docker tag gen-ai-virtual-tryon:latest your-account.dkr.ecr.us-east-1.amazonaws.com/gen-ai-virtual-tryon:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/gen-ai-virtual-tryon:latest

# Deploy to ECS
aws ecs create-cluster --cluster-name gen-ai-cluster
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster gen-ai-cluster --service-name gen-ai-service --task-definition gen-ai-virtual-tryon:1 --desired-count 2
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/gen-ai-virtual-tryon
gcloud run deploy gen-ai-virtual-tryon \
  --image gcr.io/your-project/gen-ai-virtual-tryon \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_api_key,ENVIRONMENT=production
```

#### DigitalOcean App Platform
```bash
# Create app specification
doctl apps create --spec app.yaml
```

#### Railway
```bash
# Deploy to Railway
railway login
railway init
railway up
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Application Configuration
ENVIRONMENT=production
DEBUG=false
PORT=8000

# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://your-domain.com

# File Upload Configuration
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### Nginx Configuration

The `nginx.conf` file includes:
- Security headers
- Gzip compression
- Static file serving
- API proxy configuration
- SSL/TLS support

### Kubernetes Configuration

The `kubernetes/` directory contains:
- Deployment with 3 replicas
- LoadBalancer service
- Persistent volume for uploads
- Ingress with SSL
- Health checks and resource limits

## 🏥 Monitoring & Health Checks

### Health Endpoint
```bash
GET /health
```
Returns application status and environment information.

### Docker Health Checks
```bash
# Check container health
docker ps
docker inspect <container_id> | grep Health -A 10
```

### Kubernetes Probes
```bash
# Check pod health
kubectl describe pod <pod_name>
kubectl logs <pod_name>
```

## 🔒 Security Considerations

### Production Security Checklist

- [ ] HTTPS enabled with valid SSL certificate
- [ ] Security headers configured in nginx
- [ ] CORS origins restricted to production domains
- [ ] API keys stored securely (not in code)
- [ ] Rate limiting implemented
- [ ] Input validation and sanitization
- [ ] Regular security updates
- [ ] Monitoring and alerting configured

### SSL/TLS Setup

#### Let's Encrypt with Certbot
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Self-Signed Certificate (Development)
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/private.key -out ssl/certificate.crt
```

## 🐛 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check container logs
docker-compose logs app
```

#### Port Conflicts
```bash
# Check what's using port 8000
netstat -tulpn | grep :8000  # Linux
lsof -i :8000                # macOS
netstat -ano | findstr :8000 # Windows
```

#### API Key Issues
- Verify API key is correctly set in environment
- Check API key permissions in Google Cloud Console
- Ensure billing is enabled for the project

#### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Logs and Debugging

#### Application Logs
```bash
# Docker logs
docker-compose logs -f app

# Kubernetes logs
kubectl logs -f deployment/gen-ai-virtual-tryon

# Direct application logs
tail -f app.log
```

#### Nginx Logs
```bash
# Access logs
tail -f /var/log/nginx/access.log

# Error logs
tail -f /var/log/nginx/error.log
```

## 📊 Performance Optimization

### Docker Optimization
- Multi-stage builds reduce image size
- Layer caching for faster builds
- Non-root user for security

### Frontend Optimization
- Code splitting with Vite
- Static asset caching
- Gzip compression

### Backend Optimization
- Async/await for I/O operations
- Connection pooling for databases
- Caching strategies

## 🔄 CI/CD Pipeline

### GitHub Actions
The `.github/workflows/deploy.yml` includes:
- Automated testing
- Docker image building
- Deployment to production
- Health checks

### Manual Deployment
```bash
# Test the application
./deploy.sh dev

# Build and test Docker image
docker build -t gen-ai-virtual-tryon .
docker run --rm -p 8000:8000 gen-ai-virtual-tryon

# Deploy to production
./deploy.sh production
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Kubernetes scaling
kubectl scale deployment gen-ai-virtual-tryon --replicas=5

# Docker Compose scaling
docker-compose up --scale app=3
```

### Load Balancing
- Nginx load balancer configuration
- Kubernetes service load balancing
- Cloud provider load balancers

### Database Scaling (Future)
- Read replicas
- Connection pooling
- Caching layers

## 🆘 Support

For deployment issues:
1. Check the troubleshooting section
2. Review logs and error messages
3. Verify environment configuration
4. Test with minimal setup first
5. Create an issue on GitHub with detailed information

---

This deployment guide covers all major deployment scenarios. Choose the method that best fits your infrastructure and requirements.

