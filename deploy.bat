@echo off
setlocal enabledelayedexpansion

REM Deployment script for Uwear AI Virtual Try-On Clothes (Windows)
REM This script builds the frontend and prepares the backend for deployment

echo 🚀 Starting deployment process for Uwear AI Virtual Try-On Clothes...

REM Check if we're in the correct directory
if not exist "package.json" (
    echo [ERROR] This script must be run from the root directory of the project
    exit /b 1
)

if not exist "frontend" (
    echo [ERROR] Frontend directory not found
    exit /b 1
)

if not exist "backend" (
    echo [ERROR] Backend directory not found
    exit /b 1
)

REM Check prerequisites
echo [INFO] Checking prerequisites...

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18.0.0 or higher.
    exit /b 1
)

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed. Please install npm 8.0.0 or higher.
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python is not installed. Please install Python 3.11.9 or higher.
        exit /b 1
    )
)

echo [SUCCESS] Prerequisites check passed

REM Install frontend dependencies
echo [INFO] Installing frontend dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies
    exit /b 1
)
echo [SUCCESS] Frontend dependencies installed

REM Build frontend
echo [INFO] Building frontend...
call npm run build
if errorlevel 1 (
    echo [ERROR] Frontend build failed
    exit /b 1
)
echo [SUCCESS] Frontend built successfully

REM Check if build was successful
if not exist "dist" (
    echo [ERROR] Frontend build failed - dist directory not found
    exit /b 1
)

REM Go back to root
cd ..

REM Create frontend directory in backend if it doesn't exist
echo [INFO] Preparing backend for deployment...
cd backend
if not exist "frontend" mkdir frontend

REM Copy built frontend to backend
echo [INFO] Copying frontend build to backend...
xcopy "..\frontend\dist\*" "frontend\" /E /Y /Q
if errorlevel 1 (
    echo [ERROR] Failed to copy frontend files to backend
    exit /b 1
)

REM Check if copy was successful
if not exist "frontend\index.html" (
    echo [ERROR] Failed to copy frontend files to backend
    exit /b 1
)

echo [SUCCESS] Frontend files copied to backend

REM Install backend dependencies
echo [INFO] Installing backend dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies
    exit /b 1
)
echo [SUCCESS] Backend dependencies installed

REM Go back to root
cd ..

echo [SUCCESS] 🎉 Deployment preparation completed successfully!
echo.
echo [INFO] You can now deploy the application:
echo.
echo   Option 1: Run locally
echo     cd backend
echo     python main.py
echo.
echo   Option 2: Deploy to Render.com
echo     - Build Command: cd ../frontend ^&^& npm install ^&^& npm run build ^&^& cd ../backend
echo     - Start Command: python main.py
echo.
echo   Option 3: Deploy to other platforms
echo     - Ensure the backend/frontend/ directory contains the built frontend
echo     - Install Python dependencies: pip install -r requirements.txt
echo     - Start the application: python main.py
echo.
echo [INFO] The application will be available at the configured port (default: 8000)
