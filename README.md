# Gen-AI Virtual Try-On Clothes 👗✨

![Virtual Try-On](https://img.shields.io/badge/Download%20Latest%20Release-Get%20It%20Here-brightgreen)  
[![GitHub Releases](https://img.shields.io/github/release/Ownned3389/Gen-AI-Virtual-Try-On-Clothes.svg)](https://github.com/Ownned3389/Gen-AI-Virtual-Try-On-Clothes/releases)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://hub.docker.com/)
[![Deploy](https://img.shields.io/badge/Deploy-Ready-green)](https://github.com/Ownned3389/Gen-AI-Virtual-Try-On-Clothes)
[![Render](https://img.shields.io/badge/Render-Deploy%20Now-purple)](https://render.com/deploy)

Welcome to the **Gen-AI Virtual Try-On Clothes** repository! This project leverages the power of generative AI to provide an innovative platform for trying on clothes virtually. Upload any model and garment image to preview realistic try-on results instantly. Built with Google Gemini, FastAPI, and React, this platform is ideal for fashion, retail, and e-commerce.

## 🚀 Quick Start

### Using Render (Easiest - One Click Deploy)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. **Click the Deploy Button above**
2. **Connect your GitHub repository**
3. **Set Environment Variables**:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
4. **Deploy**: Click "Create Web Service"

Your app will be live at `https://your-app-name.onrender.com`!

### Using Docker (Local/Production)

1. **Clone and Deploy**:
   ```bash
   git clone https://github.com/Ownned3389/Gen-AI-Virtual-Try-On-Clothes.git
   cd Gen-AI-Virtual-Try-On-Clothes
   
   # Copy environment template and configure
   cp env.example .env
   # Edit .env with your Google API key
   
   # Deploy with Docker
   ./deploy.sh docker
   # Or on Windows: deploy.bat docker
   ```

2. **Access the Application**:
   - Open your browser and go to `http://localhost:8000`
   - The application is now ready to use!

### Production Deployment

```bash
# Deploy with nginx
./deploy.sh production

# Or deploy to Kubernetes
kubectl apply -f kubernetes/
```

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Deployment](#deployment)
5. [Usage](#usage)
6. [API Documentation](#api-documentation)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

## Features 🌟

- **Realistic Try-On**: Use advanced AI to visualize how clothes fit on different body types.
- **Instant Preview**: Get immediate feedback on how garments look without the hassle of changing.
- **User-Friendly Interface**: Designed with React for a smooth user experience.
- **Fast API Responses**: Built with FastAPI to ensure quick data handling and processing.
- **Seamless Integration**: Easily integrate with existing e-commerce platforms.
- **Production Ready**: Complete deployment setup with Docker, Kubernetes, and CI/CD.
- **Scalable Architecture**: Microservices-ready with container orchestration support.
- **Cloud Deployable**: One-click deployment on Render, Heroku, AWS, and more.

## Technologies Used 🛠️

- **Google Gemini**: For generative AI capabilities.
- **FastAPI**: To build the backend API efficiently.
- **React**: For creating an interactive frontend.
- **Python**: The core programming language for backend development.
- **Docker**: For containerization and easy deployment.
- **Kubernetes**: For container orchestration and scaling.
- **Nginx**: For reverse proxy and load balancing.
- **GitHub Actions**: For CI/CD automation.
- **Render**: For cloud deployment and hosting.

## Installation ⚙️

### Prerequisites

- **Docker & Docker Compose** (for containerized deployment)
- **Python 3.12+** (for local development)
- **Node.js 18+** (for frontend development)
- **Google Gemini API Key** (for AI functionality)

### Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ownned3389/Gen-AI-Virtual-Try-On-Clothes.git
   cd Gen-AI-Virtual-Try-On-Clothes
   ```

2. **Set Up the Backend**:
   ```bash
   cd backend
   pip install poetry
   poetry install
   cp env.example .env
   # Edit .env with your Google API key
   uvicorn main:app --reload
   ```

3. **Set Up the Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

## Deployment 🚀

### Render Deployment (Recommended)

The easiest way to deploy is using Render:

1. **One-Click Deploy**: Click the [Deploy to Render](https://render.com/deploy) button
2. **Manual Setup**: Follow the [Render Deployment Guide](render-deploy.md)
3. **Environment Variables**: Set your `GOOGLE_API_KEY` in Render dashboard

### Docker Deployment

The easiest way to deploy locally:

```bash
# Quick deployment
./deploy.sh docker

# Production deployment with nginx
./deploy.sh production

# Development setup
./deploy.sh dev

# Clean up resources
./deploy.sh cleanup
```

### Kubernetes Deployment

For production environments with Kubernetes:

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods,services,ingress
```

### Cloud Deployment

#### Heroku
```bash
# Deploy to Heroku
heroku create your-app-name
heroku config:set GOOGLE_API_KEY=your_api_key
git push heroku main
```

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker build -t gen-ai-virtual-tryon .
docker tag gen-ai-virtual-tryon:latest your-account.dkr.ecr.us-east-1.amazonaws.com/gen-ai-virtual-tryon:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/gen-ai-virtual-tryon:latest
```

#### Google Cloud Run
```bash
# Deploy to Cloud Run
gcloud builds submit --tag gcr.io/your-project/gen-ai-virtual-tryon
gcloud run deploy gen-ai-virtual-tryon --image gcr.io/your-project/gen-ai-virtual-tryon --platform managed
```

## Usage 🖼️

1. **Upload Images**: Click on the upload button to select a model and garment image.
2. **Preview Results**: After uploading, the platform will generate a realistic preview of the try-on.
3. **Save or Share**: You can save the results or share them on social media.

## API Documentation 📚

### Health Check
```bash
GET /health
```
Returns application health status.

### Try-On Endpoint
```bash
POST /api/tryon
```
Upload model and garment images for virtual try-on.

### Interactive API Docs
Visit `http://localhost:8000/docs` for interactive API documentation.

## Environment Variables 🔧

Create a `.env` file based on `env.example`:

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
```

## Monitoring & Health Checks 🏥

The application includes comprehensive health monitoring:

- **Health Endpoint**: `GET /health`
- **Docker Health Checks**: Automatic container health monitoring
- **Kubernetes Probes**: Liveness and readiness probes
- **Logging**: Structured logging for debugging and monitoring

## Security 🔒

- **HTTPS**: SSL/TLS encryption for all production deployments
- **Security Headers**: Comprehensive security headers via nginx
- **CORS**: Configurable Cross-Origin Resource Sharing
- **Input Validation**: Robust input validation and sanitization
- **Rate Limiting**: API rate limiting for abuse prevention

## Contributing 🤝

We welcome contributions! If you want to improve this project, please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeatureName
   ```
5. Open a pull request.

### Development Guidelines

- Follow the existing code style
- Add tests for new features
- Update documentation for API changes
- Ensure Docker builds successfully
- Test deployment scripts

## Troubleshooting 🔧

### Common Issues

1. **Docker Build Fails**:
   ```bash
   # Clean Docker cache
   docker system prune -a
   # Rebuild
   docker-compose build --no-cache
   ```

2. **API Key Issues**:
   - Ensure `GOOGLE_API_KEY` is set in `.env`
   - Verify the API key has proper permissions

3. **Port Conflicts**:
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   # Or change port in docker-compose.yml
   ```

4. **Frontend Build Issues**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm run build
   ```

### Render Deployment Issues

For Render-specific issues, see the [Render Deployment Guide](render-deploy.md).

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact 📬

For questions or feedback, please reach out:

- **Author**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [Your GitHub Profile](https://github.com/YourProfile)

For more information, check the [Releases](https://github.com/Ownned3389/Gen-AI-Virtual-Try-On-Clothes/releases) section.

---

Feel free to explore the code and contribute to this exciting project! Your feedback and suggestions are always welcome. Happy coding!