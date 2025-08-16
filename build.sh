#!/bin/bash

# Build script for Render deployment
set -e

echo "🚀 Starting build process..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm ci
npm run build
cd ..

# Install backend dependencies
echo "🐍 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo "✅ Build completed successfully!"
