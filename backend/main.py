from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
import sys
import threading
import time

# Add detailed logging for debugging
print("🚀 Starting Virtual Try-On API initialization...")
print(f"📁 Current working directory: {os.getcwd()}")
print(f"📁 Python version: {sys.version}")
print(f"📁 Environment variables: PORT={os.environ.get('PORT', 'Not set')}")

app = FastAPI(title="Virtual Try-On API", version="1.0.0")

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
print(f"📁 Base directory: {BASE_DIR}")

# Serve static files from the frontend build directory
frontend_build_path = BASE_DIR / "frontend" / "dist"
print(f"📁 Looking for frontend build at: {frontend_build_path}")

# Check if frontend build exists and mount static files
if frontend_build_path.exists():
    print(f"✅ Frontend build found at: {frontend_build_path}")
    print(f"📁 Frontend contents: {list(frontend_build_path.iterdir())}")
    app.mount("/static", StaticFiles(directory=str(frontend_build_path)), name="static")
else:
    print(f"⚠️  Frontend build not found at: {frontend_build_path}")
    print("   This is normal during development or if build failed")
    
    # Check if the frontend directory exists at all
    frontend_dir = BASE_DIR / "frontend"
    if frontend_dir.exists():
        print(f"📁 Frontend directory exists: {list(frontend_dir.iterdir())}")
    else:
        print(f"❌ Frontend directory not found at: {frontend_dir}")

# Global flag for MediaPipe initialization
mediapipe_ready = False
mediapipe_initializing = False

def initialize_mediapipe():
    """Initialize MediaPipe in background thread"""
    global mediapipe_ready, mediapipe_initializing
    mediapipe_initializing = True
    print("🔄 Initializing MediaPipe in background...")
    
    try:
        # Import and initialize MediaPipe
        import mediapipe as mp
        print("✅ MediaPipe imported successfully")
        mediapipe_ready = True
        print("✅ MediaPipe initialization completed")
    except Exception as e:
        print(f"❌ MediaPipe initialization failed: {e}")
        mediapipe_ready = False
    finally:
        mediapipe_initializing = False

@app.get("/")
def root():
    # Serve the frontend index.html for the root route
    index_path = frontend_build_path / "index.html"
    if index_path.exists():
        print(f"✅ Serving frontend from: {index_path}")
        return FileResponse(str(index_path))
    
    # Fallback response if frontend is not built
    print(f"⚠️  Frontend index.html not found at: {index_path}")
    return {
        "message": "Virtual Try-On API is running", 
        "status": "healthy",
        "frontend": "not built",
        "api_endpoints": {
            "health": "/health",
            "try_on": "/api/try-on"
        },
        "debug_info": {
            "frontend_build_path": str(frontend_build_path),
            "frontend_exists": frontend_build_path.exists(),
            "current_dir": os.getcwd(),
            "base_dir": str(BASE_DIR)
        }
    }

@app.get("/startup")
def startup_check():
    """Simple startup check for Render port detection"""
    return {"status": "starting", "message": "Application is starting up"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "mediapipe": "ready" if mediapipe_ready else "initializing" if mediapipe_initializing else "not_ready",
        "frontend_built": frontend_build_path.exists(),
        "frontend_path": str(frontend_build_path),
        "port": os.environ.get("PORT", "Not set"),
        "current_dir": os.getcwd(),
        "api_endpoints": {
            "try_on": "/api/try-on",
            "health": "/health"
        }
    }

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working", "timestamp": "2024-01-16"}

# Catch-all route to serve frontend routes
@app.get("/{full_path:path}")
def serve_frontend(full_path: str, request: Request):
    # Skip API routes
    if full_path.startswith("api/"):
        return {"error": "API endpoint not found"}
    
    # Try to serve static files first
    static_file_path = frontend_build_path / full_path
    if static_file_path.exists() and static_file_path.is_file():
        return FileResponse(str(static_file_path))
    
    # For SPA routing, serve index.html for all other routes
    index_path = frontend_build_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    
    # Fallback for when frontend is not built
    return {
        "error": "Frontend not available",
        "message": "Please ensure the frontend is built and available",
        "path_requested": full_path,
        "debug_info": {
            "frontend_build_path": str(frontend_build_path),
            "frontend_exists": frontend_build_path.exists()
        }
    }

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # Local backend
        "https://uwear-ai-virtual-try-on-clothes.onrender.com",  # Deployed backend
        "*"  # Allow all origins for now
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Import and include router immediately
try:
    print("🔄 Attempting to import tryon router...")
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    print(f"📁 Added to Python path: {current_dir}")
    
    from routers import tryon
    print("✅ Tryon router imported successfully")
    app.include_router(tryon.router, prefix="/api")
    print("✅ Try-on router included successfully")
except ImportError as e:
    print(f"❌ Import error for tryon router: {e}")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📁 Python path: {sys.path}")
except Exception as e:
    print(f"❌ Failed to include try-on router: {e}")
    import traceback
    traceback.print_exc()

# Server configuration for deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Virtual Try-On API on port {port}")
    print(f"📁 Environment: PORT={os.environ.get('PORT', '8000')}")
    print(f"📁 Frontend build path: {frontend_build_path}")
    print(f"📁 Frontend build exists: {frontend_build_path.exists()}")
    
    if frontend_build_path.exists():
        print("✅ Frontend will be served from static files")
    else:
        print("⚠️  Frontend not built - API only mode")
    
    print(f"🌐 Binding to port {port}...")
    print(f"🔗 Application will be available at: http://0.0.0.0:{port}")
    
    # Start MediaPipe initialization in background
    mediapipe_thread = threading.Thread(target=initialize_mediapipe, daemon=True)
    mediapipe_thread.start()
    
    try:
        # Start server immediately
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port, 
            log_level="info",
            access_log=True,
            server_header=False
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
