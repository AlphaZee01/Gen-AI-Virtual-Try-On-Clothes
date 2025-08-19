from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from utils.base64_helpers import array_buffer_to_base64
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import traceback
import base64

load_dotenv()

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

client = genai.Client(api_key=GEMINI_API_KEY)

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

        user_bytes = await person_image.read()

        size_in_mb_for_person_image = len(user_bytes) / (1024 * 1024)
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


        user_b64 = array_buffer_to_base64(user_bytes)
        cloth_b64 = array_buffer_to_base64(cloth_bytes)

        prompt = f"""
        You are a virtual fashion stylist. Your task is to modify the MAIN IMAGE (person) by ONLY changing their clothing to match the REFERENCE IMAGE (garment), while keeping everything else exactly the same.

        IMAGE STRUCTURE:
        - MAIN IMAGE (PERSON): This is the base image to modify - keep everything except clothing
        - REFERENCE IMAGE (GARMENT): This is the clothing reference - extract ONLY the garment

        CRITICAL INSTRUCTIONS:
        1. START with the MAIN IMAGE (person) as your base - this is the image to modify
        2. KEEP the person's face, hair, skin tone, and pose EXACTLY as they are in the MAIN IMAGE
        3. KEEP the original background EXACTLY as it is in the MAIN IMAGE
        4. KEEP the lighting, shadows, and environment EXACTLY as they are in the MAIN IMAGE
        5. ONLY change the clothing/garment to match the REFERENCE IMAGE (garment)
        6. Make the garment from the REFERENCE IMAGE fit naturally on the person's body shape and pose
        7. Preserve the exact color, pattern, and texture of the garment from the REFERENCE IMAGE

        GARMENT TRANSFER SPECIFICATIONS:
        - Extract ONLY the clothing item from the REFERENCE IMAGE
        - Ignore any person, model, mannequin, or background in the REFERENCE IMAGE
        - Transfer ONLY the fabric, color, pattern, and design of the garment
        - Scale the garment to fit the person's body proportions in the MAIN IMAGE
        - Maintain the garment's original appearance but adapt it to the person's pose
        - Keep the garment's texture, material properties, and visual details intact

        STRICT PRESERVATION RULES:
        - Person's face: NO changes whatsoever
        - Person's hair: NO changes whatsoever  
        - Person's skin tone: NO changes whatsoever
        - Person's pose: NO changes whatsoever
        - Person's body shape: NO changes whatsoever
        - Background: NO changes whatsoever
        - Lighting: NO changes whatsoever
        - Shadows: NO changes whatsoever
        - Environment: NO changes whatsoever
        - Accessories (glasses, jewelry, etc.): NO changes unless covered by new garment
        - Image framing: NO changes whatsoever - keep exact same crop and composition
        - Image zoom level: NO changes whatsoever - maintain exact same scale
        - Image dimensions: NO changes whatsoever - output same size as input

        DO NOT:
        - Change the person's face, hair, or skin tone from the MAIN IMAGE
        - Change the background or environment from the MAIN IMAGE
        - Change the lighting or shadows from the MAIN IMAGE
        - Generate a new scene or setting
        - Alter the person's pose or body shape from the MAIN IMAGE
        - Use the REFERENCE IMAGE as the main person (it's just for the clothing reference)
        - Copy any person, model, or mannequin from the REFERENCE IMAGE
        - Transfer any background elements from the REFERENCE IMAGE
        - Change the composition or framing of the MAIN IMAGE
        - Zoom in or out on the image
        - Crop or resize the image
        - Change the image dimensions or aspect ratio
        - Adjust the camera angle or perspective

        Context:
            - Model Type: {model_type}
            - Gender: {gender}
            - Garment Type: {garment_type}
            - Style: {style}
            - Special Instructions: {instructions}

        Return the MAIN IMAGE with ONLY the garment changed to match the REFERENCE IMAGE, keeping everything else identical to the original MAIN IMAGE.
        """
               
        print(model_type)
        print(gender)
        print(garment_type)
        print(style)
        print(instructions)
        
        print(prompt)

        contents=[
            prompt,
            types.Part(text="MAIN IMAGE (PERSON) - This is the base image to modify:"),
            types.Part.from_bytes(
                data=user_bytes,
                mime_type= person_image.content_type,
            ),
            types.Part(text="REFERENCE IMAGE (GARMENT) - Extract ONLY the clothing from this image:"),
            types.Part.from_bytes(
                data=cloth_bytes,
                mime_type= cloth_image.content_type,
            ),
        ]        
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=contents,
            config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
            )
        )


        print(response)
        
        image_data = None
        text_response = "No Description available."
        if response.candidates and len(response.candidates) > 0:
            parts = response.candidates[0].content.parts

            if parts:
                print("Number of parts in response:", len(parts))

                for part in parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        image_data = part.inline_data.data
                        image_mime_type = getattr(part.inline_data, "mime_type", "image/png")
                        print("Image data received, length:", len(image_data))
                        print("MIME type:", image_mime_type)

                    elif hasattr(part, "text") and part.text:
                        text_response = part.text
                        preview = (text_response[:100] + "...") if len(text_response) > 100 else text_response
                        print("Text response received:", preview)
            else:
                print("No parts found in the response candidate.")
        else:
            print("No candidates found in the API response.")

        image_url = None
        if image_data:
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            image_url = f"data:{image_mime_type};base64,{image_base64}"
        else:
            image_url = None
    
        return JSONResponse(
        content={
            "image": image_url,
            "text": text_response,
        }
        )

    except Exception as e:
        print(f"Error in /api/try-on endpoint: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
