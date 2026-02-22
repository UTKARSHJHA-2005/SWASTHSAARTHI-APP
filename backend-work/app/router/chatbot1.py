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
from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import google.generativeai as genai
import csv
import os
import json
import re
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Create router instance
router = APIRouter()

# Load datasets
TRAINING_CSV_PATH = "app/Data/Training.csv"
testing = pd.read_csv(TRAINING_CSV_PATH)
cols = testing.columns[:-1]
y = testing['prognosis']
le = LabelEncoder()
y = le.fit_transform(y)
clf = DecisionTreeClassifier()
x_train, x_test, y_train, y_test = train_test_split(testing[cols], y, test_size=0.3, random_state=42)
clf.fit(x_train, y_train)

# Load Master Data
description_dict = {}
severity_dict = {}
precaution_dict = {}

def load_data():
    global description_dict, severity_dict, precaution_dict
    desc_path = "app/MasterData/symptom_Description.csv"
    severity_path = "app/MasterData/symptom_severity.csv"
    precaution_path = "app/MasterData/symptom_precaution.csv"
    
    if os.path.exists(desc_path):
        with open(desc_path) as file:
            reader = csv.reader(file)
            description_dict = {row[0]: row[1] for row in reader if len(row) >= 2}
    
    if os.path.exists(severity_path):
        with open(severity_path) as file:
            reader = csv.reader(file)
            severity_dict = {row[0]: int(row[1]) for row in reader if len(row) >= 2 and row[1].isdigit()}
    
    if os.path.exists(precaution_path):
        with open(precaution_path) as file:
            reader = csv.reader(file)
            precaution_dict = {row[0]: row[1:] for row in reader if len(row) >= 2}

load_data()

class ChatRequest(BaseModel):
    user_input: str
    user_id: str  # Unique identifier for conversation tracking

# In-memory session storage
user_sessions = {}
FOLLOW_UP_QUESTIONS = {
    "fever": "Do you also have chills or sweating?",
    "cough": "Is it a dry cough or productive with mucus?",
    "headache": "Is your headache mild or severe?",
}

def detect_language_with_gemini(text):
    prompt = f"Detect the language of the following text and return only the language name (e.g., English, Hindi, Spanish):\n\n{text}"
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

def translate_with_gemini(text, target_language):
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

def extract_symptoms(user_input: str):
    prompt = f"""
    Extract symptoms from the following patient complaint: "{user_input}"
    - Only return symptoms present in this list: {list(cols)}
    - Output should be a valid JSON list (e.g., ["fever", "cough"])
    - If no symptoms match, return []
    """
    
    response = gemini_model.generate_content(prompt)
    
    try:
        match = re.search(r"\[(.*?)\]", response.text, re.DOTALL)
        if match:
            symptoms = json.loads(f"[{match.group(1)}]")  
            return [s.strip().lower() for s in symptoms if s.strip().lower() in cols]
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse Gemini response: {e}")
    
    return []

def predict_disease(symptoms):
    input_vector = np.zeros(len(cols))
    for symptom in symptoms:
        if symptom in cols:
            input_vector[list(cols).index(symptom)] = 1
    prediction = clf.predict(input_vector.reshape(1, -1))
    disease = le.inverse_transform(prediction)[0]
    
    return {
        "disease": disease,
        "description": description_dict.get(disease, "No description available"),
        "precautions": precaution_dict.get(disease, []),
        "symptom_severity": {symptom: severity_dict.get(symptom, "Unknown") for symptom in symptoms},
    }

@router.post("/chat/")
def chat_with_bot(request: ChatRequest):
    user_id = request.user_id
    user_input = request.user_input
    
    # Detect user's language
    user_lang = detect_language_with_gemini(user_input)
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {"symptoms": [], "asked_followup": False, "confirmation_stage": False}

    session = user_sessions[user_id]
    symptoms = extract_symptoms(user_input)

    # **Step 1: If no symptoms are detected, ask user to describe further**
    if not symptoms and not session["symptoms"]:
        message = "I couldn't detect any symptoms. Can you describe your health problem in more detail?"
        return {"message": translate_with_gemini(message, user_lang)}

    session["symptoms"].extend(symptoms)
    session["symptoms"] = list(set(session["symptoms"]))  # Remove duplicates

    # **Step 2: If detected symptoms are less than 2, ask a follow-up question**
    if len(session["symptoms"]) < 2 and not session["asked_followup"]:
        symptom_to_ask = session["symptoms"][0] if session["symptoms"] else np.random.choice(list(FOLLOW_UP_QUESTIONS.keys()))
        session["asked_followup"] = True
        return {"message": translate_with_gemini(FOLLOW_UP_QUESTIONS.get(symptom_to_ask, "Can you describe your symptoms in more detail?"), user_lang)}

    # **Step 3: Ask for confirmation before final diagnosis**
    if not session["confirmation_stage"]:
        session["confirmation_stage"] = True
        confirmation_text = f"I detected these symptoms: {', '.join(session['symptoms'])}. Can you confirm? Reply with 'yes' to proceed or add more symptoms."
        return {"message": translate_with_gemini(confirmation_text, user_lang)}

    # **Step 4: If user confirms, proceed with disease prediction**
    if "yes" in user_input.lower():
        result = predict_disease(session["symptoms"])
        del user_sessions[user_id]  # Clear session after diagnosis
        
        diagnosis_text = f"""
        Disease: {result['disease']}
        Description: {result['description']}
        Precautions: {', '.join(result['precautions'])}
        Symptom Severity: {result['symptom_severity']}
        """
        return {
            "disease": result["disease"],
            "description": result["description"],
            "precautions": result["precautions"],
            "symptom_severity": result["symptom_severity"],
            "message": translate_with_gemini(diagnosis_text, user_lang)
        }

    # **Step 5: If user adds more symptoms instead of confirming**
    return {"message": translate_with_gemini("Please list any additional symptoms, or reply with 'yes' to proceed with diagnosis.", user_lang)}
