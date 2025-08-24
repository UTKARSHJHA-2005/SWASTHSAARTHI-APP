from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import logging
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Create router instance
router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str
    user_id: str  # Unique identifier for conversation tracking

def get_gemini_response(prompt: str, response_format: str = "text"):
    """Fetches response from Gemini API."""
    try:
        response = gemini_model.generate_content(prompt)
        if response_format == "json":
            cleaned = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return None

def detect_language(user_input: str):
    """Detects the language of the user input."""
    try:
        prompt = f"""Identify the language of the following text and return only the language name (e.g., English, Spanish, Hindi):
        Text: "{user_input}"."""
        return get_gemini_response(prompt).strip()
    except Exception as e:
        logging.error(f"Error detecting language: {e}")
        return "English"  # Default to English

def extract_symptoms(user_input: str):
    """Extracts symptoms from the user input."""
    try:
        prompt = f"""You are a professional doctor. A patient says: '{user_input}'.
        Extract and return a JSON list of symptoms mentioned.
        If no symptoms are found, return []."""
        response = get_gemini_response(prompt, response_format="json")
        return response if isinstance(response, list) else []
    except Exception as e:
        logging.error(f"Error extracting symptoms: {e}")
        return []

def generate_diagnosis(symptoms: list, language: str = "English"):
    """Generates a diagnosis based on symptoms in the detected language."""
    try:
        symptom_names = ", ".join(symptoms)
        prompt = f"""You are a professional doctor analyzing symptoms: {symptom_names}.
        Provide the response in {language} with the following JSON format:
        {{
            "disease": "Most likely disease name",
            "description": "Brief explanation in {language} (max 100 words)",
            "severity": Severity level (1-5, where 1 is minor and 5 is critical),
            "precautions": ["List", "of", "3-5", "recommendations"],
            "urgency": "emergency | urgent | routine"
        }}"""
        return get_gemini_response(prompt, response_format="json")
    except Exception as e:
        logging.error(f"Error generating diagnosis: {e}")
        return None

@router.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    try:
        user_input = request.user_input.strip()

        # Detect language of user input
        detected_language = detect_language(user_input)
        logging.info(f"Detected Language: {detected_language}")

        # Extract symptoms
        symptoms = extract_symptoms(user_input)
        if not symptoms:
            return {"message": "I couldn't detect symptoms. Please describe them clearly."}

        # Generate diagnosis in the detected language
        diagnosis = generate_diagnosis(symptoms, language=detected_language)
        if not diagnosis:
            return {"message": f"Sorry, I couldn't determine a diagnosis at this moment. (Response in {detected_language})"}

        return {
            "disease": diagnosis.get("disease", "Unknown"),
            "description": diagnosis.get("description", ""),
            "severity": diagnosis.get("severity", 2),
            "precautions": diagnosis.get("precautions", []),
            "urgency": diagnosis.get("urgency", "routine"),
            "language": detected_language,
        }

    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred")
