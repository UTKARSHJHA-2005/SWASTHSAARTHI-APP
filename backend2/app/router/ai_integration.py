import os
from dotenv import load_dotenv
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from google.generativeai import GenerativeModel, configure

# Initialize FastAPI Router
router = APIRouter()
load_dotenv()
# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

configure(api_key=GEMINI_API_KEY)
gemini_model = GenerativeModel("gemini-1.5-flash")

# Pydantic model for symptom-based prediction request
class SymptomRequest(BaseModel):
    symptoms: str

@router.post("/predict/symptoms")
async def predict_disease_from_symptoms(request: SymptomRequest):
    """
    Predicts disease based on symptoms using Gemini AI.
    """
    prompt = f"Given the symptoms: {request.symptoms}, what are the possible diseases?"
    
    try:
        response = gemini_model.generate_content(prompt)
        return {"predicted_disease": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.post("/predict/image")
async def predict_disease_from_image(file: UploadFile = File(...)):
    """
    Predicts disease or injury based on an uploaded image using Gemini AI.
    """
    try:
        image_data = await file.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        response = gemini_model.generate_content(
            ["Identify any medical condition, disease, or injury in this image:", {"mime_type": "image/jpeg", "data": image_base64}]
        )

        return {"predicted_disease": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
