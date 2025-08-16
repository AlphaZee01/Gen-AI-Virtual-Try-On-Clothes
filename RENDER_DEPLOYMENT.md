# Render.com Deployment Guide

This guide will help you deploy the Uwear AI Virtual Try-On application to Render.com.

## Prerequisites

- A GitHub repository with your code
- A Render.com account
- The repository should be public or connected to Render

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your repository has the following structure:
```
Gen-AI-Virtual-Try-On-Clothes/
├── frontend/
├── backend/
├── package.json
└── README.md
```

### 2. Create a Render Web Service

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create an account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account if not already connected
   - Select your repository

3. **Configure the Service**

   **Basic Settings:**
   - **Name**: `uwear-virtual-try-on` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose the region closest to your users
   - **Branch**: `main` (or your default branch)

   **Build & Deploy Settings:**
   - **Build Command**: `cd ../frontend && npm ci && npm run build && cd ../backend`
   - **Start Command**: `python main.py`
   - **Health Check Path**: `/health`

   **Environment Variables (Optional):**
   - `PYTHON_VERSION`: `3.11.9`
   - `NODE_VERSION`: `18.0.0`

4. **Create the Service**
   - Click "Create Web Service"
   - Render will start building your application

### 3. Monitor the Build Process

The build process will:
1. Install Node.js 18.0.0
2. Install Python 3.11.9
3. Install frontend dependencies (`npm ci`)
4. Build the frontend (`npm run build`)
5. Install Python dependencies
6. Start the application

**Expected Build Time**: 5-10 minutes

### 4. Verify Deployment

Once the build completes successfully:

1. **Check the Health Endpoint**
   ```
   https://your-app-name.onrender.com/health
   ```
   Should return:
   ```json
   {
     "status": "healthy",
     "mediapipe": "available",
     "frontend_built": true,
     "frontend_path": "/app/backend/frontend/dist"
   }
   ```

2. **Visit Your Application**
   ```
   https://your-app-name.onrender.com
   ```
   Should show the virtual try-on interface

3. **Test the API**
   ```
   https://your-app-name.onrender.com/api/try-on
   ```
   Should return API information

## Troubleshooting

### Build Failures

**Common Issues:**

1. **Node.js Installation Failed**
   - **Solution**: Ensure `NODE_VERSION=18.0.0` is set in environment variables

2. **Frontend Build Failed**
   - **Solution**: Check if all frontend dependencies are in `package.json`
   - **Solution**: Verify the build command is correct

3. **Python Dependencies Failed**
   - **Solution**: Check if `requirements.txt` is in the backend directory
   - **Solution**: Verify Python version compatibility

**Debug Steps:**
1. Check the build logs in Render dashboard
2. Look for specific error messages
3. Test the build locally first

### Runtime Issues

**Common Issues:**

1. **Application Won't Start**
   - **Check**: Start command is `python main.py`
   - **Check**: All dependencies are installed
   - **Check**: Port is correctly configured

2. **Frontend Not Loading**
   - **Check**: Frontend build completed successfully
   - **Check**: `/health` endpoint shows `frontend_built: true`
   - **Check**: Static files are being served

3. **API Endpoints Not Working**
   - **Check**: CORS settings are correct
   - **Check**: API routes are properly configured
   - **Check**: MediaPipe dependencies are installed

### Performance Issues

**Cold Starts:**
- Render has cold starts for free tier
- Consider upgrading to paid plan for better performance

**Memory Issues:**
- MediaPipe can be memory-intensive
- Consider upgrading to a plan with more RAM

## Environment Variables

You can add these environment variables in Render dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.11.9` | Python version to use |
| `NODE_VERSION` | `18.0.0` | Node.js version to use |
| `PORT` | `8000` | Port for the application |

## Monitoring

### Health Checks
- Render automatically checks `/health` endpoint
- If health check fails, Render will restart the service

### Logs
- View real-time logs in Render dashboard
- Logs show build process and runtime information

### Metrics
- Monitor CPU, memory, and network usage
- Set up alerts for performance issues

## Updating Your Application

1. **Push Changes to GitHub**
   ```bash
   git add .
   git commit -m "Update application"
   git push origin main
   ```

2. **Render Auto-Deploy**
   - Render automatically detects changes
   - Triggers new build and deployment
   - No manual intervention required

3. **Manual Deploy (if needed)**
   - Go to Render dashboard
   - Click "Manual Deploy"
   - Select branch to deploy

## Cost Optimization

**Free Tier:**
- 750 hours per month
- Cold starts on inactivity
- Limited resources

**Paid Plans:**
- Always-on instances
- Better performance
- More resources

## Support

If you encounter issues:

1. **Check Render Documentation**: [docs.render.com](https://docs.render.com)
2. **View Build Logs**: Detailed error information in dashboard
3. **Community Support**: [Render Community](https://community.render.com)
4. **Contact Support**: Available for paid plans

## Example Successful Deployment

A successful deployment will show:
- ✅ Build completed successfully
- ✅ Health check passing
- ✅ Application accessible at your URL
- ✅ Frontend and API both working

Your application URL will be: `https://your-app-name.onrender.com`
