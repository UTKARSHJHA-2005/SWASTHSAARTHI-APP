import os
import base64
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from google import genai

# Initialize FastAPI Router
router = APIRouter()

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Create Gemini client (NEW SDK)
client = genai.Client(api_key=GEMINI_API_KEY)


# ----------------------------
# Pydantic Model
# ----------------------------
class SymptomRequest(BaseModel):
    symptoms: str


# ----------------------------
# Symptom-Based Prediction
# ----------------------------
@router.post("/predict/symptoms")
async def predict_disease_from_symptoms(request: SymptomRequest):

    prompt = f"""
    You are a medical assistant.

    Based on these symptoms: {request.symptoms}

    Return ONLY valid JSON in this exact format:

    {{
        "disease": "Most likely disease name",
        "description": "Short explanation (max 80 words)",
        "severity": 1-5,
        "precautions": ["3-5 precautions"],
        "urgency": "emergency | urgent | routine"
    }}

    DO NOT return text.
    DO NOT explain.
    ONLY return JSON.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw_text = response.text.strip()

        # Clean markdown if Gemini adds it
        cleaned = (
            raw_text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        import json
        parsed = json.loads(cleaned)

        return parsed

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ----------------------------
# Image-Based Prediction
# ----------------------------
@router.post("/predict/image")
async def predict_disease_from_image(file: UploadFile = File(...)):
    """
    Predicts disease or injury based on an uploaded image using Gemini AI.
    """
    try:
        image_data = await file.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Identify any medical condition, disease, or injury in this image.",
                {
                    "mime_type": file.content_type,
                    "data": image_data,
                },
            ],
        )

        return {"predicted_disease": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
