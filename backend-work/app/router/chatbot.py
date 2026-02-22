from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
import os
import logging
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Create Gemini client (NEW SDK WAY)
client = genai.Client(api_key=GEMINI_API_KEY)

# Create router instance
router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str
    user_id: str


def get_gemini_response(prompt: str, response_format: str = "text"):
    """Fetches response from Gemini API using new SDK."""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        text_response = response.text

        if response_format == "json":
            cleaned = (
                text_response.replace("```json", "")
                .replace("```", "")
                .strip()
            )
            return json.loads(cleaned)

        return text_response

    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return None


def detect_language(user_input: str):
    try:
        prompt = f"""
        Identify the language of the following text and return only the language name.
        Text: "{user_input}"
        """
        response = get_gemini_response(prompt)
        return response.strip() if response else "English"
    except Exception as e:
        logging.error(f"Error detecting language: {e}")
        return "English"


def extract_symptoms(user_input: str):
    try:
        prompt = f"""
        You are a professional doctor. A patient says: '{user_input}'.
        Extract and return a JSON list of symptoms mentioned.
        If no symptoms are found, return [].
        """

        response = get_gemini_response(prompt, response_format="json")
        return response if isinstance(response, list) else []

    except Exception as e:
        logging.error(f"Error extracting symptoms: {e}")
        return []


def generate_diagnosis(symptoms: list, language: str = "English"):
    try:
        symptom_names = ", ".join(symptoms)

        prompt = f"""
        You are a professional doctor analyzing symptoms: {symptom_names}.
        Provide the response in {language} with the following JSON format:

        {{
            "disease": "Most likely disease name",
            "description": "Brief explanation in {language} (max 100 words)",
            "severity": 1-5,
            "precautions": ["List", "of", "3-5", "recommendations"],
            "urgency": "emergency | urgent | routine"
        }}
        """

        return get_gemini_response(prompt, response_format="json")

    except Exception as e:
        logging.error(f"Error generating diagnosis: {e}")
        return None


@router.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    try:
        user_input = request.user_input.strip()

        # Detect language
        detected_language = detect_language(user_input)
        logging.info(f"Detected Language: {detected_language}")

        # Extract symptoms
        symptoms = extract_symptoms(user_input)

        if not symptoms:
            return {
                "message": "I couldn't detect symptoms. Please describe them clearly."
            }

        # Generate diagnosis
        diagnosis = generate_diagnosis(symptoms, language=detected_language)

        if not diagnosis:
            return {
                "message": f"Sorry, I couldn't determine a diagnosis at this moment. (Response in {detected_language})"
            }

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
