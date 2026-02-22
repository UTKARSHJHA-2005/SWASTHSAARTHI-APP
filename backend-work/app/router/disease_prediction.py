from fastapi import APIRouter, HTTPException
import os
import re
import json
import requests
from dotenv import load_dotenv
from google import genai

router = APIRouter()

# ----------------------------
# Symptom Master List
# ----------------------------
SYMPTOMS_LIST = {
    "itching", "skin rash", "nodal skin eruptions", "continuous sneezing", "shivering",
    "chills", "joint pain", "stomach pain", "acidity", "ulcers on tongue",
    "vomiting", "burning micturition", "spotting urination", "fatigue",
    "weight gain", "anxiety", "cold hands and feets", "mood swings",
    "weight loss", "restlessness", "lethargy", "patches in throat",
    "irregular sugar level", "cough", "high fever", "sunken eyes",
    "breathlessness", "sweating", "dehydration", "indigestion",
    "headache", "yellowish skin", "dark urine", "nausea",
    "loss of appetite", "back pain", "constipation", "abdominal pain",
    "diarrhoea", "mild fever", "yellow urine", "yellowing of eyes",
    "swelled lymph nodes", "malaise", "blurred and distorted vision",
    "phlegm", "throat irritation", "redness of eyes", "sinus pressure",
    "runny nose", "congestion", "chest pain", "weakness in limbs",
    "fast heart rate", "neck pain", "dizziness", "cramps",
    "bruising", "obesity", "swollen legs", "puffy face and eyes",
    "muscle weakness", "stiff neck", "swelling joints",
    "movement stiffness", "loss of balance", "unsteadiness",
    "weakness of one body side", "loss of smell", "depression",
    "irritability", "muscle pain", "altered sensorium",
    "red spots over body", "belly pain", "abnormal menstruation",
    "watering from eyes", "increased appetite", "polyuria",
    "coma", "stomach bleeding", "distention of abdomen",
    "palpitations", "painful walking", "pus filled pimples",
    "blackheads", "skin peeling", "blister"
}

# ----------------------------
# Load Environment
# ----------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PREDICT_API_URL = os.getenv("PREDICT_API_URL", "http://localhost:10000/predict")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Create Gemini client (NEW SDK)
client = genai.Client(api_key=GEMINI_API_KEY)


# ----------------------------
# Helper Function
# ----------------------------
def extract_json_from_text(text: str):
    """Extracts JSON list from model response."""
    match = re.search(r"\[(.*?)\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(f"[{match.group(1)}]")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Failed to parse extracted symptoms")
    return []


# ----------------------------
# Main Endpoint
# ----------------------------
@router.post("/disease-prediction")
async def process_symptoms(data: dict):
    """
    Extract symptoms using Gemini and forward to ML prediction API.
    """
    user_query = data.get("query")

    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required")

    extract_prompt = f"""
    Extract symptoms from the given text and return them as a Python list.
    If no symptoms are found, return [].
    Text: "{user_query}"
    Output format: ["symptom1", "symptom2"]
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=extract_prompt,
        )

        if not response or not response.text.strip():
            raise HTTPException(status_code=500, detail="Gemini API returned empty response")

        print("🔹 Gemini Response:", response.text)

        extracted_symptoms = extract_json_from_text(response.text.lower())

        if not isinstance(extracted_symptoms, list):
            raise HTTPException(status_code=500, detail="Unexpected Gemini format")

        matched_symptoms = [
            symptom for symptom in extracted_symptoms
            if symptom in SYMPTOMS_LIST
        ]

        # Forward to ML model API
        predict_response = requests.post(
            PREDICT_API_URL,
            json={"symptoms": matched_symptoms},
        )

        if predict_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Prediction API failed")

        return predict_response.json()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
