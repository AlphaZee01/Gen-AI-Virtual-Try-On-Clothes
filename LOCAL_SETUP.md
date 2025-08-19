# Local Setup Guide for Windows

This guide will help you set up and run the Gen-AI Virtual Try-On Clothes application locally on Windows without Docker.

## Prerequisites

1. **Python 3.12+** - Download from [python.org](https://www.python.org/downloads/)
2. **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
3. **Google Gemini API Key** - Get from [Google AI Studio](https://aistudio.google.com/)

## Quick Start (Recommended)

1. **Double-click** `start-local.bat` to automatically set up and start both servers
2. Open your browser and go to `http://localhost:3000`

## Manual Setup

### Step 1: Set up the Backend

1. Open Command Prompt and navigate to the project directory:
   ```cmd
   cd C:\Users\Kingsman007\Desktop\Gen-AI-Virtual-Try-On-Clothes\Gen-AI-Virtual-Try-On-Clothes
   ```

2. Install backend dependencies:
   ```cmd
   cd backend
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```cmd
   copy ..\env.example .env
   ```

4. Edit `backend\.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. Start the backend server:
   ```cmd
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Step 2: Set up the Frontend

1. Open a new Command Prompt window and navigate to the frontend directory:
   ```cmd
   cd C:\Users\Kingsman007\Desktop\Gen-AI-Virtual-Try-On-Clothes\Gen-AI-Virtual-Try-On-Clothes\frontend
   ```

2. Install frontend dependencies:
   ```cmd
   npm install
   ```

3. Start the frontend development server:
   ```cmd
   npm run dev
   ```

## Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Getting a Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" or go to "API keys" section
4. Create a new API key
5. Copy the key and paste it in your `backend\.env` file

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Backend: Change port in `uvicorn` command: `--port 8001`
   - Frontend: Change port in `vite.config.js` or use `npm run dev -- --port 3001`

2. **Python not found**:
   - Make sure Python is installed and added to PATH
   - Try using `python3` instead of `python`

3. **Node.js not found**:
   - Make sure Node.js is installed and added to PATH
   - Restart Command Prompt after installation

4. **API Key issues**:
   - Verify your Google Gemini API key is correct
   - Check that the key has proper permissions
   - Ensure the key is not expired

### Stopping the Servers

- **Backend**: Press `Ctrl+C` in the backend Command Prompt window
- **Frontend**: Press `Ctrl+C` in the frontend Command Prompt window

## File Structure

```
Gen-AI-Virtual-Try-On-Clothes/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application file
│   ├── routers/            # API routes
│   ├── utils/              # Utility functions
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/                # Source code
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── start-local.bat         # Quick start script
└── LOCAL_SETUP.md          # This file
```

## Next Steps

1. Upload a person image and a garment image
2. Select the appropriate options (model type, gender, etc.)
3. Click "Try On" to generate the virtual try-on result
4. View the AI-generated result and description

Enjoy using the Virtual Try-On application!
