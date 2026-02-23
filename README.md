# SWASTHSAARTHI
Swasthsaarthi is a **multilingual AI-powered health chatbot** that helps users access reliable healthcare guidance in their preferred language.  
It is designed to make health support **accessible, inclusive, and available 24/7**.  <br/>
<br/>
 ✨ <strong>Features</strong>  <br/>
🌍 Multilingual support (speak to users in their own language)  <br/>
🤝 Conversational AI for health & wellness queries  <br/>
⏰ 24/7 availability  <br/>
🔒 Privacy-focused and secure<br/> 
📱 Easy integration with apps, websites, or platforms   <br/>
<br/>
🛠 <strong>Tech Stack</strong> <br/>
Frontend: React.js (with Vite), Tailwind CSS.<br/>
Backend Setup: Firebase,FastAPI.<br/>
Machine Learning: NLLB-200-Distilled,Random Forest.<br/>
<br/>
🔧 <strong>Prerequisites</strong> <br/>
1)Vite With TailwindCSS <br/>
2)Node.js (v16+ recommended) <br/>
3)Firebase <br/>
4)Python <br/>
5)Gemini <br/>
<br/>
<strong>Installation And Setup</strong><br/>
1) Clone the Repository<br/>
   ```
   git clone https://github.com/UTKARSHJHA-2005/SWASTHSAARTHI.git
   cd SWASTHSAARTHI
   ```
   <br/>
2) Create a Virtual Enviroment (for backend)
   ```
   cd backend-work
   python -m venv venv
   ```
   source venv/bin/activate  # On macOS/Linux <br/>
   venv\Scripts\activate      # On Windows <br/>
   <br/>
4) env for backend<br/>
   ```
    GEMINI_API_KEY=your_api_key_here
   ```
   <br/>
5) Install Dependencies <br/>
   (for backend) <br/>
   ```
   cd backend-work
   pip install -r requirements.txt
   ```
   (for frontend)
   ```
   npm install
   ```
   <br/>
6) Run the server <br/>
   (for frontend) <br/>
   ```
   npx react-native run-android
   ```
   (for backend-work) <br/>
   ```
   cd backend-work
   uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
   ```
   The server will start at: http://localhost:10000
