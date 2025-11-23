# Configuration Guide

## 📝 Environment Variables

All configuration is managed through the `.env` file. Never commit this file to version control.

## 🔑 Required API Keys

### Gemini API Key

**Purpose**: Powers the AI interviewer and conversation

**How to get**:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste into `.env`

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Firebase Configuration

**Purpose**: Handles Google authentication

**How to get**:
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing
3. Go to Project Settings > General
4. Scroll to "Your apps" and click the web icon (</>)
5. Copy all configuration values

```env
FIREBASE_API_KEY=your_firebase_api_key_here
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id
```

## ⚙️ Optional Configuration

### Model Settings

```env
# Gemini model version
MODEL_ID=gemini-2.5-flash

# Whisper speech recognition model size
# Options: tiny.en, base.en, small.en, medium.en, large
WHISPER_MODEL_SIZE=base.en

# Whisper compute type
# Options: int8, float16, float32
WHISPER_COMPUTE=int8

# Text-to-speech voice
# Options: en-US-AriaNeural, en-US-GuyNeural, etc.
VOICE_NAME=en-US-AriaNeural
```

### Server Configuration

```env
# Server host (0.0.0.0 allows external connections)
HOST=0.0.0.0

# Server port
PORT=8000
```

### File Paths

```env
# Path to coding questions database
QUESTIONS_FILE=questions.json

# Piston API for code execution
PISTON_API_URL=https://emkc.org/api/v2/piston/execute
```

## 📋 Configuration Table

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | None | Google Gemini API key |
| `FIREBASE_API_KEY` | ✅ Yes | None | Firebase API key |
| `FIREBASE_AUTH_DOMAIN` | ✅ Yes | None | Firebase auth domain |
| `FIREBASE_PROJECT_ID` | ✅ Yes | None | Firebase project ID |
| `FIREBASE_STORAGE_BUCKET` | ✅ Yes | None | Firebase storage bucket |
| `FIREBASE_MESSAGING_SENDER_ID` | ✅ Yes | None | Firebase messaging sender ID |
| `FIREBASE_APP_ID` | ✅ Yes | None | Firebase app ID |
| `FIREBASE_MEASUREMENT_ID` | ✅ Yes | None | Firebase measurement ID |
| `MODEL_ID` | ❌ No | `gemini-2.5-flash` | Gemini model version |
| `WHISPER_MODEL_SIZE` | ❌ No | `base.en` | Speech recognition model |
| `WHISPER_COMPUTE` | ❌ No | `int8` | Whisper compute type |
| `VOICE_NAME` | ❌ No | `en-US-AriaNeural` | TTS voice |
| `HOST` | ❌ No | `0.0.0.0` | Server host |
| `PORT` | ❌ No | `8000` | Server port |
| `QUESTIONS_FILE` | ❌ No | `questions.json` | Questions database path |
| `PISTON_API_URL` | ❌ No | `https://emkc.org/api/v2/piston/execute` | Code execution API |

## 🔒 Security Best Practices

1. **Never commit `.env`**: The `.gitignore` file excludes it automatically
2. **Use `.env.example`**: Share template with team, not actual keys
3. **Rotate keys regularly**: Update API keys periodically
4. **Limit API key permissions**: Use least privilege principle
5. **Monitor usage**: Check API quotas and usage patterns

## 🌍 Environment-Specific Configs

### Development
```env
HOST=127.0.0.1
PORT=8000
MODEL_ID=gemini-2.5-flash
```

### Production
```env
HOST=0.0.0.0
PORT=80
MODEL_ID=gemini-2.5-flash
# Use production Firebase project
```

## 🔄 Loading Configuration

The application uses `python-dotenv` to load environment variables:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file

# Access variables
api_key = os.getenv("GEMINI_API_KEY")
```

## ✅ Verification

Check if your configuration is loaded correctly:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Gemini API Key:', 'SET' if os.getenv('GEMINI_API_KEY') else 'MISSING')"
```

## Next Steps

- [Learn about MCP Tools](MCP_TOOLS.md)
- [Understand the architecture](ARCHITECTURE.md)
- [Troubleshooting guide](TROUBLESHOOTING.md)
