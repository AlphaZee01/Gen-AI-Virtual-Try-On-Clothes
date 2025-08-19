import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import tryon
from fastapi.middleware.cors import CORSMiddleware

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

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
    frontend_dist_path = "../frontend/dist"
    if os.path.exists(frontend_dist_path):
        app.mount("/static", StaticFiles(directory=frontend_dist_path), name="static")
        
        @app.get("/")
        async def serve_frontend():
            return FileResponse(f"{frontend_dist_path}/index.html")
        
        @app.get("/{full_path:path}")
        async def serve_static_files(full_path: str):
            # Try to serve static files first
            static_file_path = f"{frontend_dist_path}/{full_path}"
            if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
                return FileResponse(static_file_path)
            
            # If not found, serve index.html for SPA routing
            return FileResponse(f"{frontend_dist_path}/index.html")

app.include_router(tryon.router, prefix="/api")
