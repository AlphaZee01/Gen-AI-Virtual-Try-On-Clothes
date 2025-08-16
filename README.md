# Uwear AI Virtual Try-On Clothes

An AI-powered virtual try-on application that allows users to see how clothes look on them while preserving their original background and lighting.

## Features

- **AI-Powered Virtual Try-On**: Upload your photo and garment to see how it looks on you
- **Background Preservation**: Your original background and lighting are preserved
- **Advanced Texture Preservation**: Clothing textures, patterns, and design details are maintained
- **Multiple Garment Types**: Support for shirts, pants, jackets, dresses, and t-shirts
- **Style Customization**: Choose from various styles and model types
- **Real-time Processing**: Fast AI processing with progress indicators
- **History Tracking**: View and manage your previous try-on results
- **Dark/Light Mode**: Toggle between dark and light themes
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Unified Architecture

This application is now set up as a unified frontend and backend system where:
- The backend serves both API endpoints and the frontend static files
- Single deployment handles both frontend and backend
- No need for separate hosting of frontend and backend

## Quick Start

### Prerequisites

- Python 3.11.9 or higher
- Node.js 18.0.0 or higher
- npm 8.0.0 or higher

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Gen-AI-Virtual-Try-On-Clothes
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   npm install
   
   # Or install separately
   npm run install:frontend
   npm run install:backend
   ```

3. **Build the frontend**
   ```bash
   npm run build:frontend
   ```

4. **Start the development server**
   ```bash
   # Start both frontend and backend in development mode
   npm run dev
   
   # Or start separately
   npm run dev:backend  # Backend on http://localhost:8000
   npm run dev:frontend # Frontend on http://localhost:5173
   ```

### Production Deployment

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Start the production server**
   ```bash
   npm start
   ```

The application will be available at `http://localhost:8000`

### Alternative Build Methods

#### Using Build Scripts

**Linux/Mac:**
```bash
cd backend
chmod +x build.sh
./build.sh
python main.py
```

**Windows:**
```bash
cd backend
build.bat
python main.py
```

#### Manual Build

```bash
# Build frontend
cd frontend
npm install
npm run build

# Copy to backend
cd ../backend
mkdir -p frontend
cp -r ../frontend/dist/* frontend/

# Start backend
python main.py
```

## Render.com Deployment

This application is optimized for deployment on Render.com. Follow these steps:

### 1. Connect Your Repository

1. Go to [Render.com](https://render.com) and create an account
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select the repository containing this project

### 2. Configure the Service

**Basic Settings:**
- **Name**: `uwear-virtual-try-on` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy Settings:**
- **Build Command**: `cd ../frontend && npm ci && npm run build && cd ../backend`
- **Start Command**: `python main.py`
- **Health Check Path**: `/health`

**Environment Variables:**
- `PYTHON_VERSION`: `3.11.9`
- `NODE_VERSION`: `18.0.0`

### 3. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install Node.js and Python
   - Build the frontend
   - Install Python dependencies
   - Start the application

### 4. Verify Deployment

Once deployed, you can:
- Visit your app at the provided URL
- Check the health endpoint: `https://your-app.onrender.com/health`
- Test the API: `https://your-app.onrender.com/api/try-on`

### Troubleshooting Render Deployment

**If the build fails:**
1. Check the build logs in Render dashboard
2. Ensure all files are committed to your repository
3. Verify the build command is correct

**If the app doesn't start:**
1. Check the start logs in Render dashboard
2. Verify the start command: `python main.py`
3. Check if all dependencies are installed

**If frontend is not loading:**
1. Check if the frontend build completed successfully
2. Verify the `/health` endpoint shows `frontend_built: true`
3. Check the build logs for any frontend build errors

## API Endpoints

- `GET /` - Serves the frontend application
- `GET /health` - Health check endpoint
- `GET /test` - Test endpoint
- `POST /api/try-on` - Virtual try-on endpoint

## Project Structure

```
Gen-AI-Virtual-Try-On-Clothes/
├── frontend/                 # React frontend application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/                  # FastAPI backend application
│   ├── main.py              # Main application entry point
│   ├── routers/             # API route handlers
│   ├── utils/               # Utility functions
│   ├── frontend/            # Built frontend files (generated)
│   ├── requirements.txt
│   ├── build.sh             # Linux/Mac build script
│   ├── build.bat            # Windows build script
│   ├── Procfile             # Render deployment configuration
│   └── render.yaml          # Render service configuration
├── package.json             # Root package.json for unified management
└── README.md
```

## Environment Variables

The application automatically detects the environment:
- **Development**: Uses `http://localhost:8000` for API calls
- **Production**: Uses relative URLs when served from the same domain

## Development

### Frontend Development

- Built with React 18 and Vite
- Uses Tailwind CSS for styling
- Includes Radix UI components
- Supports hot reloading in development

### Backend Development

- Built with FastAPI
- Uses MediaPipe for AI processing
- Includes CORS middleware for development
- Supports both API and static file serving

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.