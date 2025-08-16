from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from utils.base64_helpers import array_buffer_to_base64
from utils.enhanced_tryon import EnhancedVirtualTryOnProcessor
from dotenv import load_dotenv
import os
import traceback

try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

router = APIRouter()

# Initialize the enhanced virtual try-on processor
try_on_processor = EnhancedVirtualTryOnProcessor()

@router.post("/try-on")
async def try_on(
    person_image: UploadFile = File(...),
    cloth_image: UploadFile = File(...),
    instructions: str = Form(""),
    model_type: str = Form(""),
    gender: str = Form(""),
    garment_type: str = Form(""),
    style: str = Form(""),
):
    try:
        # Validate file types and sizes
        MAX_IMAGE_SIZE_MB = 10
        ALLOWED_MIME_TYPES = {
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/heic",
            "image/heif",
        }

        if person_image.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file type for person_image: {person_image.content_type}"
            )

        person_bytes = await person_image.read()
        size_in_mb_for_person_image = len(person_bytes) / (1024 * 1024)
        if size_in_mb_for_person_image > MAX_IMAGE_SIZE_MB:
            raise HTTPException(status_code=400, detail="Image exceeds 10MB size limit for person_image")
        
        if cloth_image.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file type for cloth_image: {cloth_image.content_type}"
            )

        cloth_bytes = await cloth_image.read()
        size_in_mb_for_cloth_image = len(cloth_bytes) / (1024 * 1024)
        if size_in_mb_for_cloth_image > MAX_IMAGE_SIZE_MB:
            raise HTTPException(status_code=400, detail="Image exceeds 10MB size limit for cloth_image")

        # Process virtual try-on using the enhanced processor
        result_image, description = try_on_processor.process_virtual_tryon(
            person_bytes, 
            cloth_bytes, 
            garment_type, 
            instructions
        )
        
        # Convert result to base64
        image_url = try_on_processor.numpy_to_base64(result_image)
        
        return JSONResponse(
            content={
                "image": image_url,
                "text": description,
            }
        )

    except Exception as e:
        print(f"Error in /api/try-on endpoint: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
