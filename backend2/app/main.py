# main.py (FastAPI Entry Point)
from fastapi import FastAPI
from app.router import chatbot
from app.router import ai_integration
from app.router import disease_prediction

app = FastAPI(title="AI Health Chatbot", version="1.0")

app.include_router(chatbot.router)
app.include_router(ai_integration.router)
app.include_router(disease_prediction.router)

@app.get("/")
def home():
    return {"message": "Welcome to AI Health Chatbot"}
