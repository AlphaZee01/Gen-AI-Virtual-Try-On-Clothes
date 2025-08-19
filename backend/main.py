import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

# Add error handling for router import
try:
    from routers import tryon
    print("✅ Successfully imported tryon router")
except Exception as e:
    print(f"❌ Error importing tryon router: {e}")
    sys.exit(1)

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

print(f"🚀 Starting Gen-AI Virtual Try-On API")
print(f"📊 Environment: {ENVIRONMENT}")
print(f"🔧 Debug mode: {DEBUG}")
print(f"📁 Working directory: {os.getcwd()}")
print(f"📁 Frontend dist path: {os.path.abspath('./frontend/dist')}")

app = FastAPI(
    title="Gen-AI Virtual Try-On API",
    description="AI-powered virtual try-on platform for clothes",
    version="1.0.0",
    debug=DEBUG
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": ENVIRONMENT}

# Serve static files (frontend build)
if ENVIRONMENT == "production":
    # Check if frontend build exists
    frontend_dist_path = "./frontend/dist"
    print(f"🔍 Checking for frontend build at: {frontend_dist_path}")
    print(f"📁 Frontend dist exists: {os.path.exists(frontend_dist_path)}")
    
    if os.path.exists(frontend_dist_path):
        print("✅ Frontend build found, mounting static files")
        
        # Mount static assets (JS, CSS, images)
        app.mount("/assets", StaticFiles(directory=f"{frontend_dist_path}/assets"), name="assets")
        
        @app.get("/")
        async def serve_frontend():
            return FileResponse(f"{frontend_dist_path}/index.html")
        
        @app.get("/{full_path:path}")
        async def serve_static_files(full_path: str):
            # Skip API routes
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="Not found")
            
            # Try to serve static files first
            static_file_path = f"{frontend_dist_path}/{full_path}"
            if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
                return FileResponse(static_file_path)
            
            # If not found, serve index.html for SPA routing
            return FileResponse(f"{frontend_dist_path}/index.html")
    else:
        print("⚠️ Frontend build not found, static file serving disabled")

app.include_router(tryon.router, prefix="/api")
