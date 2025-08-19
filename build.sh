#!/bin/bash

# Build script for Render deployment
set -e

echo "🚀 Starting build process for Gen-AI Virtual Try-On..."

# Install system dependencies
echo "📦 Installing system dependencies..."
apt-get update && apt-get install -y nodejs npm curl

# Verify installations
echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"
echo "✅ Python version: $(python3 --version)"

# Build frontend
echo "🔨 Building frontend..."
cd frontend
npm install
npm run build
echo "✅ Frontend build completed"
cd ..

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd backend
pip install poetry
poetry config virtualenvs.create false
poetry install --only=main --no-root
echo "✅ Python dependencies installed"
cd ..

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo "🎉 Build process completed successfully!"
echo "📁 Frontend build location: frontend/dist"
echo "📁 Backend location: backend/"
echo "📁 Uploads directory: uploads/"

