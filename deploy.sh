#!/bin/bash

# Deployment script for Uwear AI Virtual Try-On Clothes
# This script builds the frontend and prepares the backend for deployment

set -e  # Exit on any error

echo "🚀 Starting deployment process for Uwear AI Virtual Try-On Clothes..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the correct directory
if [ ! -f "package.json" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    print_error "This script must be run from the root directory of the project"
    exit 1
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18.0.0 or higher."
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm 8.0.0 or higher."
    exit 1
fi

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.11.9 or higher."
    exit 1
fi

print_success "Prerequisites check passed"

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
npm install
print_success "Frontend dependencies installed"

# Build frontend
print_status "Building frontend..."
npm run build
print_success "Frontend built successfully"

# Check if build was successful
if [ ! -d "dist" ]; then
    print_error "Frontend build failed - dist directory not found"
    exit 1
fi

# Go back to root
cd ..

# Create frontend directory in backend if it doesn't exist
print_status "Preparing backend for deployment..."
cd backend
mkdir -p frontend

# Copy built frontend to backend
print_status "Copying frontend build to backend..."
cp -r ../frontend/dist/* frontend/

# Check if copy was successful
if [ ! -f "frontend/index.html" ]; then
    print_error "Failed to copy frontend files to backend"
    exit 1
fi

print_success "Frontend files copied to backend"

# Install backend dependencies
print_status "Installing backend dependencies..."
pip install -r requirements.txt
print_success "Backend dependencies installed"

# Go back to root
cd ..

print_success "🎉 Deployment preparation completed successfully!"
echo ""
print_status "You can now deploy the application:"
echo ""
echo "  Option 1: Run locally"
echo "    cd backend"
echo "    python main.py"
echo ""
echo "  Option 2: Deploy to Render.com"
echo "    - Build Command: cd ../frontend && npm install && npm run build && cd ../backend"
echo "    - Start Command: python main.py"
echo ""
echo "  Option 3: Deploy to other platforms"
echo "    - Ensure the backend/frontend/ directory contains the built frontend"
echo "    - Install Python dependencies: pip install -r requirements.txt"
echo "    - Start the application: python main.py"
echo ""
print_status "The application will be available at the configured port (default: 8000)"
