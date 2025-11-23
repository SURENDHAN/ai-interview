# Installation Guide

## 📋 Prerequisites

- Python 3.10+
- Google Gemini API Key
- Firebase Project (for authentication)

## 🛠️ Installation Steps

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd gpt
```

### 2. Create a virtual environment
```bash
python -m venv gpt
```

### 3. Activate the virtual environment

**Windows:**
```bash
.\gpt\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source gpt/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

See [Configuration Guide](CONFIGURATION.md) for detailed setup instructions.

```bash
cp .env.example .env
# Edit .env with your API keys
```

## 🎯 Running the Application

### Start the server
```bash
python -m uvicorn main3:app --reload --port 8000
```

The application will be available at:
- **Main App**: http://localhost:8000
- **Login Page**: http://localhost:8000/login.html

## 🧪 Testing the Application

1. **Login**: Navigate to `/login.html` and sign in with Google
2. **Upload Resume**: (Optional) Upload a PDF resume for personalized questions
3. **Select Role**: Choose your interview role (e.g., Software Engineer)
4. **Start Interview**: Answer questions via voice or text
5. **Coding Challenge**: Complete the coding problem when prompted
6. **Get Feedback**: Receive detailed performance analysis

## 📦 Dependencies

The following packages will be installed:

```
edge-tts==7.2.3          # Text-to-speech
fastapi==0.121.3         # Web framework
faster-whisper==1.2.1    # Speech recognition
google-genai==1.52.0     # Gemini AI
pydub==0.25.1            # Audio processing
pypdf==6.3.0             # PDF parsing
python-dotenv==1.2.1     # Environment variables
requests==2.32.5         # HTTP client
uvicorn==0.38.0          # ASGI server
wikipedia==1.4.0         # Wikipedia API
```

## ✅ Verification

Test that everything is installed correctly:

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); print('✅ Environment loaded successfully')"
```

## Next Steps

- [Configure your API keys](CONFIGURATION.md)
- [Learn about MCP Tools](MCP_TOOLS.md)
- [Understand the architecture](ARCHITECTURE.md)
