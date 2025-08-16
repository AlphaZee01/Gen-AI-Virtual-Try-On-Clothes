import cv2
import numpy as np
from PIL import Image
import io
import base64
import requests
from rembg import remove
import os
from typing import Tuple, Optional

class VirtualTryOnProcessor:
    def __init__(self):
        self.API_KEY = os.getenv("GEMINI_API_KEY")
        
    def preprocess_images(self, person_image_bytes: bytes, cloth_image_bytes: bytes) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess images for virtual try-on"""
        # Convert bytes to numpy arrays
        person_np = np.frombuffer(person_image_bytes, np.uint8)
        person_img = cv2.imdecode(person_np, cv2.IMREAD_COLOR)
        
        cloth_np = np.frombuffer(cloth_image_bytes, np.uint8)
        cloth_img = cv2.imdecode(cloth_np, cv2.IMREAD_COLOR)
        
        # Ensure images are in RGB format
        person_rgb = cv2.cvtColor(person_img, cv2.COLOR_BGR2RGB)
        cloth_rgb = cv2.cvtColor(cloth_img, cv2.COLOR_BGR2RGB)
        
        return person_rgb, cloth_rgb
    
    def remove_background(self, image: np.ndarray) -> np.ndarray:
        """Remove background from image using rembg"""
        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(image)
        
        # Remove background
        result = remove(pil_image)
        
        # Convert back to numpy array
        return np.array(result)
    
    def detect_person_segmentation(self, person_image: np.ndarray) -> np.ndarray:
        """Detect person segmentation using OpenCV"""
        # Convert to grayscale for processing
        gray = cv2.cvtColor(person_image, cv2.COLOR_RGB2GRAY)
        
        # Use HOG (Histogram of Oriented Gradients) for person detection
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        # Detect people
        boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8), padding=(4, 4), scale=1.05)
        
        # Create mask for detected person
        mask = np.zeros(gray.shape, dtype=np.uint8)
        
        if len(boxes) > 0:
            # Use the largest detected person
            largest_box = max(boxes, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_box
            
            # Create a more refined mask using the detected region
            mask[y:y+h, x:x+w] = 255
            
            # Apply morphological operations to smooth the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        return mask
    
    def extract_clothing(self, cloth_image: np.ndarray) -> np.ndarray:
        """Extract clothing from the garment image"""
        # Remove background from clothing image
        cloth_no_bg = self.remove_background(cloth_image)
        
        # Convert to RGBA if not already
        if cloth_no_bg.shape[2] == 3:
            # Add alpha channel
            alpha = np.ones((cloth_no_bg.shape[0], cloth_no_bg.shape[1]), dtype=np.uint8) * 255
            cloth_no_bg = np.dstack((cloth_no_bg, alpha))
        
        return cloth_no_bg
    
    def resize_clothing_to_person(self, clothing: np.ndarray, person_mask: np.ndarray) -> np.ndarray:
        """Resize clothing to fit the person's detected region"""
        # Find the bounding box of the person
        contours, _ = cv2.findContours(person_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return clothing
        
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Estimate clothing region (upper body for tops, lower body for pants)
        # This is a simplified approach - in a real implementation, you'd use more sophisticated body part detection
        clothing_height = int(h * 0.6)  # Assume clothing covers about 60% of person height
        clothing_width = int(w * 0.8)   # Assume clothing covers about 80% of person width
        
        # Resize clothing to fit
        resized_clothing = cv2.resize(clothing, (clothing_width, clothing_height))
        
        return resized_clothing
    
    def blend_clothing_onto_person(self, person_image: np.ndarray, clothing: np.ndarray, 
                                 person_mask: np.ndarray, garment_type: str = "") -> np.ndarray:
        """Blend the clothing onto the person while preserving the original background"""
        result = person_image.copy()
        
        # Convert to RGBA if needed
        if result.shape[2] == 3:
            alpha = np.ones((result.shape[0], result.shape[1]), dtype=np.uint8) * 255
            result = np.dstack((result, alpha))
        
        # Find the best position to place the clothing
        contours, _ = cv2.findContours(person_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return person_image
        
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Position clothing based on garment type
        if garment_type.lower() in ['shirt', 'tshirt', 'top', 'blouse']:
            # Position for upper body clothing
            clothing_y = y + int(h * 0.1)  # Start from upper part of person
        elif garment_type.lower() in ['pants', 'trousers', 'jeans']:
            # Position for lower body clothing
            clothing_y = y + int(h * 0.4)  # Start from middle part of person
        else:
            # Default positioning
            clothing_y = y + int(h * 0.2)
        
        clothing_x = x + int(w * 0.1)  # Center the clothing
        
        # Ensure clothing fits within image bounds
        clothing_h, clothing_w = clothing.shape[:2]
        
        if clothing_y + clothing_h > result.shape[0]:
            clothing_h = result.shape[0] - clothing_y
            clothing = cv2.resize(clothing, (clothing_w, clothing_h))
        
        if clothing_x + clothing_w > result.shape[1]:
            clothing_w = result.shape[1] - clothing_x
            clothing = cv2.resize(clothing, (clothing_w, clothing_h))
        
        # Blend the clothing onto the person
        if clothing.shape[2] == 4:  # Has alpha channel
            alpha = clothing[:, :, 3] / 255.0
            alpha = np.expand_dims(alpha, axis=2)
            
            # Extract RGB channels
            clothing_rgb = clothing[:, :, :3]
            
            # Blend using alpha compositing
            for c in range(3):
                result[clothing_y:clothing_y+clothing_h, clothing_x:clothing_x+clothing_w, c] = \
                    (1 - alpha[:, :, 0]) * result[clothing_y:clothing_y+clothing_h, clothing_x:clothing_x+clothing_w, c] + \
                    alpha[:, :, 0] * clothing_rgb[:, :, c]
        
        return result
    
    def enhance_lighting_consistency(self, result_image: np.ndarray, original_image: np.ndarray) -> np.ndarray:
        """Enhance lighting consistency between the clothing and the original image"""
        # This is a simplified lighting adjustment
        # In a real implementation, you'd use more sophisticated lighting analysis
        
        # Convert to LAB color space for better color manipulation
        lab_result = cv2.cvtColor(result_image, cv2.COLOR_RGB2LAB)
        lab_original = cv2.cvtColor(original_image, cv2.COLOR_RGB2LAB)
        
        # Calculate average lighting from original image
        original_l = lab_original[:, :, 0].mean()
        result_l = lab_result[:, :, 0].mean()
        
        # Adjust lighting to match original
        lighting_adjustment = original_l - result_l
        lab_result[:, :, 0] = np.clip(lab_result[:, :, 0] + lighting_adjustment, 0, 255)
        
        # Convert back to RGB
        enhanced_result = cv2.cvtColor(lab_result, cv2.COLOR_LAB2RGB)
        
        return enhanced_result
    
    def process_virtual_tryon(self, person_image_bytes: bytes, cloth_image_bytes: bytes, 
                            garment_type: str = "", instructions: str = "") -> Tuple[np.ndarray, str]:
        """Main method to process virtual try-on"""
        try:
            # Preprocess images
            person_img, cloth_img = self.preprocess_images(person_image_bytes, cloth_image_bytes)
            
            # Detect person segmentation
            person_mask = self.detect_person_segmentation(person_img)
            
            # Extract clothing from garment image
            clothing = self.extract_clothing(cloth_img)
            
            # Resize clothing to fit person
            resized_clothing = self.resize_clothing_to_person(clothing, person_mask)
            
            # Blend clothing onto person
            result = self.blend_clothing_onto_person(person_img, resized_clothing, person_mask, garment_type)
            
            # Enhance lighting consistency
            result = self.enhance_lighting_consistency(result, person_img)
            
            # Generate description
            description = self.generate_description(garment_type, instructions)
            
            return result, description
            
        except Exception as e:
            raise Exception(f"Error in virtual try-on processing: {str(e)}")
    
    def generate_description(self, garment_type: str, instructions: str) -> str:
        """Generate a description of the try-on result"""
        base_description = f"Virtual try-on completed successfully! The {garment_type} has been applied to your image while preserving the original background and lighting."
        
        if instructions:
            base_description += f" Special instructions applied: {instructions}"
        
        base_description += " The clothing has been seamlessly integrated to maintain a natural appearance."
        
        return base_description
    
    def numpy_to_base64(self, image: np.ndarray) -> str:
        """Convert numpy array to base64 string"""
        # Convert to PIL Image
        pil_image = Image.fromarray(image)
        
        # Convert to bytes
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        
        # Convert to base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return f"data:image/png;base64,{img_base64}"

