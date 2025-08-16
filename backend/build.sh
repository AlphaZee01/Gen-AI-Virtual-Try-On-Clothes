#!/bin/bash

# Build script for unified frontend and backend deployment

echo "Starting build process..."

# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    echo "Error: This script must be run from the backend directory"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "../frontend" ]; then
    echo "Error: Frontend directory not found"
    exit 1
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd ../frontend
npm install

# Build frontend
echo "Building frontend..."
npm run build

# Check if build was successful
if [ ! -d "dist" ]; then
    echo "Error: Frontend build failed - dist directory not found"
    exit 1
fi

# Create frontend directory in backend if it doesn't exist
cd ../backend
mkdir -p frontend

# Copy built frontend to backend
echo "Copying frontend build to backend..."
cp -r ../frontend/dist/* frontend/

echo "Build completed successfully!"
echo "You can now run: python main.py"
