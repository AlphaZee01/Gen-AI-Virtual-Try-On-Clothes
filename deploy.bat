@echo off
REM Gen-AI Virtual Try-On Clothes Deployment Script for Windows
REM This script helps deploy the application to various environments

setlocal enabledelayedexpansion

REM Colors for output (Windows doesn't support ANSI colors by default)
set "GREEN=[INFO]"
set "YELLOW=[WARNING]"
set "RED=[ERROR]"

REM Function to print colored output
:print_status
echo %GREEN% %~1
goto :eof

:print_warning
echo %YELLOW% %~1
goto :eof

:print_error
echo %RED% %~1
goto :eof

REM Check if Docker is installed
:check_docker
docker --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not installed. Please install Docker Desktop first."
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit /b 1
)
goto :eof

REM Check if .env file exists
:check_env
if not exist .env (
    call :print_warning ".env file not found. Creating from template..."
    if exist env.example (
        copy env.example .env >nul
        call :print_status "Created .env file from template. Please update with your configuration."
    ) else (
        call :print_error "env.example not found. Please create a .env file manually."
        exit /b 1
    )
)
goto :eof

REM Build and run with Docker Compose
:deploy_docker
call :print_status "Building and deploying with Docker Compose..."

REM Stop existing containers
docker-compose down

REM Build and start
docker-compose up --build -d

call :print_status "Application deployed successfully!"
call :print_status "Access the application at: http://localhost:8000"
goto :eof

REM Deploy to production with nginx
:deploy_production
call :print_status "Deploying to production with nginx..."

REM Stop existing containers
docker-compose down

REM Build and start with production profile
docker-compose --profile production up --build -d

call :print_status "Production deployment completed!"
call :print_status "Access the application at: http://localhost"
goto :eof

REM Development deployment
:deploy_dev
call :print_status "Setting up development environment..."

REM Backend setup
cd backend
if exist pyproject.toml (
    poetry install
) else (
    pip install -r requirements.txt 2>nul || pip install -e .
)
cd ..

REM Frontend setup
cd frontend
npm install
cd ..

call :print_status "Development environment ready!"
call :print_status "Run 'cd backend ^&^& uvicorn main:app --reload' for backend"
call :print_status "Run 'cd frontend ^&^& npm run dev' for frontend"
goto :eof

REM Clean up
:cleanup
call :print_status "Cleaning up Docker resources..."
docker-compose down --volumes --remove-orphans
docker system prune -f
call :print_status "Cleanup completed!"
goto :eof

REM Show usage
:usage
echo Usage: %~nx0 [OPTION]
echo.
echo Options:
echo   docker      Deploy using Docker Compose
echo   production  Deploy to production with nginx
echo   dev         Setup development environment
echo   cleanup     Clean up Docker resources
echo   help        Show this help message
echo.
echo Examples:
echo   %~nx0 docker      # Deploy with Docker
echo   %~nx0 production  # Deploy to production
echo   %~nx0 dev         # Setup development environment
goto :eof

REM Main script
:main
if "%1"=="" goto usage
if "%1"=="help" goto usage
if "%1"=="docker" (
    call :check_docker
    if errorlevel 1 exit /b 1
    call :check_env
    if errorlevel 1 exit /b 1
    call :deploy_docker
    goto :eof
)
if "%1"=="production" (
    call :check_docker
    if errorlevel 1 exit /b 1
    call :check_env
    if errorlevel 1 exit /b 1
    call :deploy_production
    goto :eof
)
if "%1"=="dev" (
    call :deploy_dev
    goto :eof
)
if "%1"=="cleanup" (
    call :cleanup
    goto :eof
)
goto usage
