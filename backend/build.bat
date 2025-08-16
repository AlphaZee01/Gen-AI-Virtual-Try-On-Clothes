@echo off

REM Build script for unified frontend and backend deployment (Windows)

echo Starting build process...

REM Check if we're in the backend directory
if not exist "main.py" (
    echo Error: This script must be run from the backend directory
    exit /b 1
)

REM Check if frontend directory exists
if not exist "..\frontend" (
    echo Error: Frontend directory not found
    exit /b 1
)

REM Install frontend dependencies
echo Installing frontend dependencies...
cd ..\frontend
call npm install

REM Build frontend
echo Building frontend...
call npm run build

REM Check if build was successful
if not exist "dist" (
    echo Error: Frontend build failed - dist directory not found
    exit /b 1
)

REM Create frontend directory in backend if it doesn't exist
cd ..\backend
if not exist "frontend" mkdir frontend

REM Copy built frontend to backend
echo Copying frontend build to backend...
xcopy "..\frontend\dist\*" "frontend\" /E /Y

echo Build completed successfully!
echo You can now run: python main.py
