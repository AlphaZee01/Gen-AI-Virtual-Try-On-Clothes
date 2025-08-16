from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import tryon
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

app = FastAPI(title="Virtual Try-On API", version="1.0.0")

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Serve static files from the frontend build directory
frontend_build_path = BASE_DIR / "frontend" / "dist"

# Check if frontend build exists and mount static files
if frontend_build_path.exists():
    print(f"✅ Frontend build found at: {frontend_build_path}")
    app.mount("/static", StaticFiles(directory=str(frontend_build_path)), name="static")
else:
    print(f"⚠️  Frontend build not found at: {frontend_build_path}")
    print("   This is normal during development or if build failed")

@app.get("/")
def root():
    # Serve the frontend index.html for the root route
    index_path = frontend_build_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    
    # Fallback response if frontend is not built
    return {
        "message": "Virtual Try-On API is running", 
        "status": "healthy",
        "frontend": "not built",
        "api_endpoints": {
            "health": "/health",
            "try_on": "/api/try-on"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "mediapipe": "available",
        "frontend_built": frontend_build_path.exists(),
        "frontend_path": str(frontend_build_path)
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
        "path_requested": full_path
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

app.include_router(tryon.router, prefix="/api")

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
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
