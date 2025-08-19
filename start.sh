#!/bin/bash

# Start script for Render deployment
set -e

echo "🚀 Starting Gen-AI Virtual Try-On application..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:${PWD}/backend"
export PORT="${PORT:-8000}"

# Navigate to backend directory
cd backend

echo "📍 Starting FastAPI server on port $PORT..."
echo "🌐 Environment: ${ENVIRONMENT:-development}"
echo "🔧 Debug mode: ${DEBUG:-false}"

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port $PORT

