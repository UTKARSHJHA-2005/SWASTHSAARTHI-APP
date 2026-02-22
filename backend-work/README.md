# SwasthSarth Backend 🏥

An AI-powered doctor assistant backend for Swasth Sarthi, built with FastAPI.

## This Backend Provides:

- A **Chatbot API** (`/chat/`) for text-based medical queries.
- An **Image Prediction API** (`/predict/image/`) to detect possible diseases from images.

## Tech Stack

- **FastAPI (Python) 🚀**
- **Gemini**

## Installation & Setup 🛠

### 0. Add a `.env` File

Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

### 1. Clone the Repository

```bash
git clone https://github.com/KILLERTIAN/Swasthsarth-backend.git
cd Swasthsarth-backend
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## API Endpoint: Image Prediction 🌍

### 📩 Endpoint: `POST /predict/image/`

- **Description:** Accepts an image and predicts a possible disease based on the uploaded image.

#### Request Example:

**Headers:**

```http
Content-Type: multipart/form-data
```

**Body:**

- `file`: Upload the affected area image as a file.

#### Response Example:

```json
{
  "prediction": "The image analysis suggests symptoms similar to psoriasis, a chronic skin condition that causes red, scaly patches. It is recommended to consult a dermatologist for proper diagnosis and treatment."
}
```

## Running the Server 🚀

Run the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
```

The server will start at: [http://localhost:10000](http://localhost:10000)

### Swagger UI & Docs

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** [http://localhost:10000/docs](http://localhost:10000/docs)

## Testing the API

You can test the API using **Postman** or **cURL**.

### Using cURL

```bash
curl -X POST "http://localhost:10000/predict/image/" -F "file=@skin_rash.jpg"
```

