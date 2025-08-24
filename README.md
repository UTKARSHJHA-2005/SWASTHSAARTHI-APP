# 🩺 SWASTHSAARTHI
Swasth Saarthi is a multilingual AI-powered health assistant that allows users to:<br/>
1) Describe their symptoms in natural language (text / voice input support).<br/>
2) Upload medical-related images for AI-driven image analysis.<br/>
3) Get preliminary disease predictions, severity, precautions, and urgency.<br/>
4) Interact in multiple languages, ensuring accessibility for diverse users.<br/>

🛠️ <b>Tech Stack</b><br/>
Frontend (Mobile App):<br/>
1) React Native (CLI) – Cross-platform mobile app<br/>
2) Axios – API communication<br/>
3) React Native Image Picker – Upload medical images<br/>
4) react-native-vector-icons – UI icons<br/>
Backend:<br/>
1) FastAPI – RESTful API framework<br/>
2) Uvicorn – ASGI server<br/>
3) Google Gemini API – Natural language understanding & multilingual support<br/>
4) TensorFlow / PyTorch ( image classification) – Disease image analysis<br/>
5) NLLB-200-Distilled - Multilingual handling<br/>
⚡ <b>Features</b><br/>
✅ Symptom-based disease prediction using AI (via Gemini API)<br/>
✅ Image upload & disease classification (via ML model)<br/>
✅ Multilingual support – users can interact in multiple languages<br/>
✅ Severity, precautions, and urgency detection for better guidance<br/>
✅ Smooth chat-like UI with typing indicators and file/image previews<br/>
⚙️<b> Setup & Installation</b><br/>
1. Clone Repository<br/>
<pre>
git clone https://github.com/UTKARSHJHA-2005/SWASTHSAARTHI-APP.git
cd SWASTHSAARTH-APP
</pre>
<br/>
2. Backend Setup<br/>
i) Create a Virtual Enviroment<br/>
<pre>
python -m venv venv
source venv/bin/activate  # On macOS/Linux
       venv\Scripts\activate      # On Windows
</pre>
<br/>
ii) Install Dependencies<br/>
<pre>
pip install -r requirements.txt
</pre>
<br/>
iii) Running the server <br/>
<pre>
uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
</pre>
It will run on localhost:10000 but if it doesn't then go to Command Prompt and find your PC’s IP address:<br/>
Windows: <pre>
ipconfig </pre><br/>
macOS/Linux: <pre>ifconfig or ip a </pre> <br/>
then it will give the ip address in the form 192.168... then go to Chat.jsx and change the line from http://192.168.1.5:10000 -> http://<your-ip-address>:10000<br/>
3. Frontend Setup <br/>
<pre>
cd SWASTHSAARTH-APP
npm install
npx react-native run-android   # for Android
npx react-native run-ios       # for iOS
</pre>
<br/>
4. Enviroment Values<br/>
Create a .env file in backend/: <br/>
<pre>
GEMINI_API_KEY=your_api_key_here
</pre>
<br/>
🔄 <b>Technical Workflow</b><br/>
flowchart TD <br/>
    User[User: Symptom / Image] -->|Text/Img| App[React Native App] <br/>
    App -->|API Request| FastAPI[FastAPI Backend] <br/>
    FastAPI -->|Symptom Text| Gemini[Gemini AI API] <br/>
    FastAPI -->|Image| MLModel[Image Classification Model] <br/>
    Gemini -->|Response| FastAPI <br/>
    MLModel -->|Prediction| FastAPI <br/>
    FastAPI -->|Diagnosis, Severity, Precautions| App <br/>
    App --> User <br/>
