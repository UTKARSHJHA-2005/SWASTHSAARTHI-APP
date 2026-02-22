# main.py (FastAPI Entry Point)
from fastapi import FastAPI
from app.router import chatbot
from app.router import ai_integration
from fastapi import FastAPI
from pydantic import BaseModel
from app.router import disease_prediction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Health Chatbot", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend origin for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from other files
app.include_router(chatbot.router)
app.include_router(ai_integration.router)
app.include_router(disease_prediction.router)

class ChatRequest(BaseModel):
    user_input: str  # Must match the frontend key

@app.post("/chat")
async def chat(request: ChatRequest):
    response_text = f"Bot Response: {request.user_input}"  # Replace with your logic
    return {"response": response_text}

@app.get("/")
def home():
    return {"message": "Welcome to AI Health Chatbot"}
