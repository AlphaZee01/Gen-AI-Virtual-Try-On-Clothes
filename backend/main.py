from fastapi import FastAPI
from routers import tryon
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Virtual Try-On API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Virtual Try-On API is running", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "mediapipe": "available"}

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tryon.router, prefix="/api")

# Server configuration for deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Virtual Try-On API on port {port}")
    print(f"Environment: PORT={os.environ.get('PORT', '8000')}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
