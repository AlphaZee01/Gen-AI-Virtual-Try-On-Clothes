#!/usr/bin/env python3
"""
Minimal server that starts immediately for Render port detection
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create minimal FastAPI app
app = FastAPI(title="Virtual Try-On API", version="1.0.0")

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
frontend_build_path = BASE_DIR / "frontend" / "dist"

# Check if frontend build exists and mount static files
if frontend_build_path.exists():
    print(f"✅ Frontend build found at: {frontend_build_path}")
    app.mount("/static", StaticFiles(directory=str(frontend_build_path)), name="static")
else:
    print(f"⚠️  Frontend build not found at: {frontend_build_path}")

@app.get("/")
def root():
    """Serve frontend or fallback"""
    index_path = frontend_build_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    
    return JSONResponse({
        "message": "Virtual Try-On API is running", 
        "status": "healthy",
        "frontend": "not built"
    })

@app.get("/startup")
def startup_check():
    """Simple startup check for Render port detection"""
    return JSONResponse({"status": "starting", "message": "Application is starting up"})

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy", 
        "frontend_built": frontend_build_path.exists(),
        "port": os.environ.get("PORT", "Not set")
    })

@app.get("/api/try-on")
def try_on_endpoint():
    """Placeholder for try-on endpoint"""
    return JSONResponse({
        "message": "Try-on endpoint - MediaPipe initializing in background",
        "status": "initializing"
    })

# Catch-all route to serve frontend routes
@app.get("/{full_path:path}")
def serve_frontend(full_path: str, request: Request):
    if full_path.startswith("api/"):
        return JSONResponse({"error": "API endpoint not found"})
    
    static_file_path = frontend_build_path / full_path
    if static_file_path.exists() and static_file_path.is_file():
        return FileResponse(str(static_file_path))
    
    index_path = frontend_build_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    
    return JSONResponse({
        "error": "Frontend not available",
        "message": "Please ensure the frontend is built and available"
    })

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting minimal server on port {port}")
    print(f"📁 Frontend build exists: {frontend_build_path.exists()}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port, 
        log_level="info"
    )
