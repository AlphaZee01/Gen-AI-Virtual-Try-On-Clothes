#!/bin/bash

# Gen-AI Virtual Try-On Clothes Deployment Script
# This script helps deploy the application to various environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        if [ -f env.example ]; then
            cp env.example .env
            print_status "Created .env file from template. Please update with your configuration."
        else
            print_error "env.example not found. Please create a .env file manually."
            exit 1
        fi
    fi
}

# Build and run with Docker Compose
deploy_docker() {
    print_status "Building and deploying with Docker Compose..."
    
    # Stop existing containers
    docker-compose down
    
    # Build and start
    docker-compose up --build -d
    
    print_status "Application deployed successfully!"
    print_status "Access the application at: http://localhost:8000"
}

# Deploy to production with nginx
deploy_production() {
    print_status "Deploying to production with nginx..."
    
    # Stop existing containers
    docker-compose down
    
    # Build and start with production profile
    docker-compose --profile production up --build -d
    
    print_status "Production deployment completed!"
    print_status "Access the application at: http://localhost"
}

# Development deployment
deploy_dev() {
    print_status "Setting up development environment..."
    
    # Backend setup
    cd backend
    if command -v poetry &> /dev/null; then
        poetry install --no-root
    else
        pip install -r requirements.txt 2>/dev/null || pip install -e .
    fi
    cd ..
    
    # Frontend setup
    cd frontend
    npm install
    cd ..
    
    print_status "Development environment ready!"
    print_status "Run 'cd backend && uvicorn main:app --reload' for backend"
    print_status "Run 'cd frontend && npm run dev' for frontend"
}

# Clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down --volumes --remove-orphans
    docker system prune -f
    print_status "Cleanup completed!"
}

# Show usage
usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker      Deploy using Docker Compose"
    echo "  production  Deploy to production with nginx"
    echo "  dev         Setup development environment"
    echo "  cleanup     Clean up Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docker      # Deploy with Docker"
    echo "  $0 production  # Deploy to production"
    echo "  $0 dev         # Setup development environment"
}

# Main script
main() {
    case "${1:-help}" in
        docker)
            check_docker
            check_env
            deploy_docker
            ;;
        production)
            check_docker
            check_env
            deploy_production
            ;;
        dev)
            deploy_dev
            ;;
        cleanup)
            cleanup
            ;;
        help|*)
            usage
            ;;
    esac
}

# Run main function
main "$@"
