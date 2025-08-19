# Render Deployment Guide

This guide provides step-by-step instructions for deploying the Gen-AI Virtual Try-On Clothes application on Render.

## 🚀 Quick Deploy on Render

### Option 1: One-Click Deploy (Recommended)

1. **Click the Deploy Button**:
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

2. **Connect your GitHub repository**:
   - Fork or clone this repository to your GitHub account
   - Connect your GitHub account to Render
   - Select this repository

3. **Configure the deployment**:
   - **Name**: `gen-ai-virtual-tryon` (or your preferred name)
   - **Environment**: `Python`
   - **Build Command**: Leave empty (uses `render.yaml`)
   - **Start Command**: Leave empty (uses `render.yaml`)

4. **Set Environment Variables**:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `ENVIRONMENT`: `production`
   - `DEBUG`: `false`

5. **Deploy**: Click "Create Web Service"

### Option 2: Manual Deployment

1. **Create a new Web Service** on Render
2. **Connect your GitHub repository**
3. **Configure the service**:
   - **Environment**: Python
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `chmod +x start.sh && ./start.sh`

## 📋 Prerequisites

### 1. Google Gemini API Key
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Copy the API key for use in Render

### 2. GitHub Repository
- Ensure your code is pushed to GitHub
- Repository should be public or connected to Render

## 🔧 Configuration Files

### render.yaml
The main configuration file that tells Render how to build and deploy:

```yaml
services:
  - type: web
    name: gen-ai-virtual-tryon
    env: python
    plan: starter
    buildCommand: |
      # Install system dependencies
      apt-get update && apt-get install -y nodejs npm
      
      # Build frontend
      cd frontend
      npm install
      npm run build
      cd ..
      
      # Install Python dependencies
      cd backend
      pip install poetry
      poetry config virtualenvs.create false
      poetry install --only=main --no-root
      cd ..
    startCommand: |
      cd backend
      uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables
Set these in your Render dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `GEMINI_API_KEY` | `your_api_key_here` | Google Gemini API key |
| `ENVIRONMENT` | `production` | Application environment |
| `DEBUG` | `false` | Debug mode |
| `CORS_ORIGINS` | `https://your-app.onrender.com` | Allowed CORS origins |

## 🏗️ Build Process

The build process on Render:

1. **System Dependencies**: Install Node.js and npm
2. **Frontend Build**: Install dependencies and build React app
3. **Backend Setup**: Install Python dependencies via Poetry
4. **Static Files**: Frontend build is served by FastAPI

## 🚀 Start Process

The application starts with:
- FastAPI server on port `$PORT` (set by Render)
- Static file serving for the React frontend
- Health check endpoint at `/health`

## 📊 Monitoring

### Health Checks
- **Endpoint**: `/health`
- **Expected Response**: `{"status": "healthy", "environment": "production"}`

### Logs
- View logs in the Render dashboard
- Monitor build and runtime logs
- Check for any errors during deployment

## 🔒 Security

### Environment Variables
- Never commit API keys to your repository
- Use Render's environment variable system
- Keep sensitive data secure

### CORS Configuration
- Update `CORS_ORIGINS` to match your Render URL
- Format: `https://your-app-name.onrender.com`

## 🐛 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check if Node.js is installed
node --version

# Check if npm is available
npm --version

# Verify Python version
python3 --version
```

#### Runtime Errors
```bash
# Check application logs
# Look for missing dependencies
# Verify environment variables are set
```

#### Frontend Not Loading
- Check if `frontend/dist` directory exists
- Verify static file serving is working
- Check browser console for errors

### Debug Steps

1. **Check Build Logs**:
   - Go to your Render dashboard
   - Click on your service
   - View the "Build" tab

2. **Check Runtime Logs**:
   - Go to the "Logs" tab
   - Look for error messages
   - Check if the application started successfully

3. **Test Health Endpoint**:
   ```bash
   curl https://your-app.onrender.com/health
   ```

4. **Verify Environment Variables**:
   - Go to "Environment" tab
   - Ensure all required variables are set
   - Check for typos in variable names

## 📈 Scaling

### Render Plans
- **Starter**: Free tier, suitable for development
- **Standard**: Paid tier, better performance
- **Pro**: High-performance tier for production

### Performance Optimization
- Enable caching for static assets
- Optimize image sizes
- Use CDN for better global performance

## 🔄 Continuous Deployment

### Auto-Deploy
- Render automatically deploys on git push
- Configure branch protection rules
- Set up deployment notifications

### Manual Deploy
- Use "Manual Deploy" option for testing
- Deploy specific branches or commits
- Rollback to previous deployments

## 📞 Support

### Render Support
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Render Status](https://status.render.com)

### Application Support
- Check the main README.md for general issues
- Review the DEPLOYMENT.md for other deployment options
- Create an issue on GitHub for bugs

## 🎉 Success Checklist

- [ ] Application builds successfully
- [ ] Health endpoint returns 200
- [ ] Frontend loads correctly
- [ ] API endpoints are accessible
- [ ] Environment variables are set
- [ ] CORS is configured properly
- [ ] Google API key is working
- [ ] File uploads work (if applicable)

---

Your application should now be live at `https://your-app-name.onrender.com`! 🚀
