SYMPTOMS_LIST = {
    "itching", "skin rash", "nodal skin eruptions", "continuous sneezing", "shivering",
    "chills", "joint pain", "stomach pain", "acidity", "ulcers on tongue", "muscle wasting",
    "vomiting", "burning micturition", "spotting urination", "fatigue", "weight gain",
    "anxiety", "cold hands and feets", "mood swings", "weight loss", "restlessness",
    "lethargy", "patches in throat", "irregular sugar level", "cough", "high fever",
    "sunken eyes", "breathlessness", "sweating", "dehydration", "indigestion", "headache",
    "yellowish skin", "dark urine", "nausea", "loss of appetite", "pain behind the eyes",
    "back pain", "constipation", "abdominal pain", "diarrhoea", "mild fever", "yellow urine",
    "yellowing of eyes", "acute liver failure", "fluid overload", "swelling of stomach",
    "swelled lymph nodes", "malaise", "blurred and distorted vision", "phlegm",
    "throat irritation", "redness of eyes", "sinus pressure", "runny nose", "congestion",
    "chest pain", "weakness in limbs", "fast heart rate", "pain during bowel movements",
    "pain in anal region", "bloody stool", "irritation in anus", "neck pain", "dizziness",
    "cramps", "bruising", "obesity", "swollen legs", "swollen blood vessels",
    "puffy face and eyes", "enlarged thyroid", "brittle nails", "swollen extremities",
    "excessive hunger", "extra marital contacts", "drying and tingling lips", "slurred speech",
    "knee pain", "hip joint pain", "muscle weakness", "stiff neck", "swelling joints",
    "movement stiffness", "spinning movements", "loss of balance", "unsteadiness",
    "weakness of one body side", "loss of smell", "bladder discomfort", "foul smell of urine",
    "continuous feel of urine", "passage of gases", "internal itching", "toxic look (typhos)",
    "depression", "irritability", "muscle pain", "altered sensorium", "red spots over body",
    "belly pain", "abnormal menstruation", "dischromic patches", "watering from eyes",
    "increased appetite", "polyuria", "family history", "mucoid sputum", "rusty sputum",
    "lack of concentration", "visual disturbances", "receiving blood transfusion",
    "receiving unsterile injections", "coma", "stomach bleeding", "distention of abdomen",
    "history of alcohol consumption", "fluid overload", "blood in sputum",
    "prominent veins on calf", "palpitations", "painful walking", "pus filled pimples",
    "blackheads", "scurring", "skin peeling", "silver like dusting", "small dents in nails",
    "inflammatory nails", "blister", "red sore around nose", "yellow crust ooze"
}
from fastapi import APIRouter, HTTPException
import os
import re
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai

router = APIRouter()

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PREDICT_API_URL = os.getenv("PREDICT_API_URL", "http://localhost:10000/predict")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_json_from_text(text: str):
    """Extracts a valid JSON list from Gemini API response using regex."""
    match = re.search(r'\[(.*?)\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(f"[{match.group(1)}]")  # Convert string to JSON
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Failed to parse extracted symptoms")
    return []

@router.post("/disease-prediction")
async def process_symptoms(data: dict):
    """
    Extracts symptoms from user input and forwards them to the disease prediction API.
    """
    user_query = data.get("query")
    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required")

    extract_prompt = f"""
    Extract symptoms from the given text and return them as a Python list.
    If no symptoms are found, return an empty list.
    Text: "{user_query}"
    Output format: ["symptom1", "symptom2", ...]
    """

    try:
        response = model.generate_content(extract_prompt)

        if not response or not response.text.strip():
            raise HTTPException(status_code=500, detail="Gemini API returned an empty response")

        print("🔹 Gemini API Response:", response.text)  # Debugging

        extracted_symptoms = extract_json_from_text(response.text.lower())

        if not isinstance(extracted_symptoms, list):
            raise HTTPException(status_code=500, detail="Unexpected response format from Gemini")

        matched_symptoms = [symptom for symptom in extracted_symptoms if symptom in SYMPTOMS_LIST]

        # ✅ Forward symptoms to disease prediction API
        predict_response = requests.post(PREDICT_API_URL, json={"symptoms": matched_symptoms})

        if predict_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Prediction API failed")

        return predict_response.json()

    except HTTPException:
        raise  # Forward FastAPI exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))