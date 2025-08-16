#!/bin/bash

# Frontend build script for Render deployment
set -e

echo "🚀 Starting frontend build process..."

# Check if we're in the right directory
if [ ! -d "../frontend" ]; then
    echo "❌ Frontend directory not found"
    exit 1
fi

# Navigate to frontend directory
cd ../frontend

echo "📦 Installing frontend dependencies..."
npm ci

echo "🔨 Building frontend..."
npm run build

# Check if build was successful
if [ ! -d "dist" ]; then
    echo "❌ Frontend build failed - dist directory not found"
    exit 1
fi

echo "✅ Frontend build completed successfully"
echo "📁 Build contents:"
ls -la dist/

# Navigate back to backend
cd ../backend

# Create frontend directory if it doesn't exist
mkdir -p frontend

# Copy built frontend to backend
echo "📋 Copying frontend build to backend..."
cp -r ../frontend/dist/* frontend/

echo "✅ Frontend build and copy completed"
echo "📁 Backend frontend directory contents:"
ls -la frontend/
