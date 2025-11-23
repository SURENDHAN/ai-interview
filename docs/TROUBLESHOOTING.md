# Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Installation Issues

#### Issue: `ModuleNotFoundError: No module named 'dotenv'`

**Cause**: `python-dotenv` package not installed

**Solution**:
```bash
pip install python-dotenv
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

---

#### Issue: `No module named 'faster_whisper'`

**Cause**: Whisper package installation failed

**Solution**:
```bash
pip install faster-whisper --upgrade
```

If still failing, try:
```bash
pip install faster-whisper==1.2.1
```

---

### Configuration Issues

#### Issue: Firebase authentication fails

**Symptoms**:
- "Failed to load authentication" error
- Sign-in button not working
- Console shows Firebase errors

**Solution**:

1. **Check `.env` file**:
   ```bash
   # Verify all Firebase variables are set
   cat .env | grep FIREBASE
   ```

2. **Verify Firebase config**:
   - Go to Firebase Console
   - Check that web app is configured
   - Ensure authorized domains include `localhost`

3. **Test config endpoint**:
   ```bash
   curl http://localhost:8000/api/config
   ```

4. **Check browser console** for specific error messages

---

#### Issue: Gemini API errors

**Symptoms**:
- "API key not valid" error
- 429 rate limit errors
- Empty AI responses

**Solution**:

1. **Verify API key**:
   ```bash
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Key:', os.getenv('GEMINI_API_KEY')[:20] + '...')"
   ```

2. **Check API quota**:
   - Go to [Google AI Studio](https://makersuite.google.com/)
   - Check usage and limits

3. **Test API directly**:
   ```python
   from google import genai
   client = genai.Client(api_key="your_key")
   resp = client.models.generate_content(
       model="gemini-2.5-flash",
       contents="Hello"
   )
   print(resp.text)
   ```

---

### Audio Issues

#### Issue: Microphone not working

**Symptoms**:
- "Error accessing microphone" message
- No audio bars moving
- VAD status stuck on "Idle"

**Solution**:

1. **Grant browser permissions**:
   - Click lock icon in address bar
   - Allow microphone access
   - Refresh page

2. **Check microphone device**:
   - Test mic in other apps
   - Ensure mic is not muted
   - Check system audio settings

3. **Try different browser**:
   - Chrome/Edge recommended
   - Firefox may have different permissions

---

#### Issue: Audio playback not working

**Symptoms**:
- AI text appears but no voice
- Console shows TTS errors
- Audio queue errors

**Solution**:

1. **Check edge-tts**:
   ```bash
   pip install edge-tts --upgrade
   ```

2. **Test TTS directly**:
   ```python
   import asyncio
   import edge_tts
   
   async def test():
       tts = edge_tts.Communicate("Hello", "en-US-AriaNeural")
       await tts.save("test.mp3")
   
   asyncio.run(test())
   ```

3. **Check browser audio**:
   - Unmute browser tab
   - Check system volume
   - Test with other audio

---

### WebSocket Issues

#### Issue: WebSocket connection fails

**Symptoms**:
- "Reconnecting..." status
- No AI responses
- Console shows WebSocket errors

**Solution**:

1. **Check server is running**:
   ```bash
   curl http://localhost:8000
   ```

2. **Verify WebSocket endpoint**:
   ```javascript
   // In browser console
   ws = new WebSocket('ws://localhost:8000/ws');
   ws.onopen = () => console.log('Connected');
   ws.onerror = (e) => console.error('Error:', e);
   ```

3. **Check firewall**:
   - Allow port 8000
   - Disable VPN temporarily
   - Check antivirus settings

4. **Restart server**:
   ```bash
   # Stop server (Ctrl+C)
   # Restart
   python -m uvicorn main3:app --reload --port 8000
   ```

---

### Coding Challenge Issues

#### Issue: Code execution fails

**Symptoms**:
- "Network Error" in output
- Tests always fail
- Timeout errors

**Solution**:

1. **Check Piston API**:
   ```bash
   curl https://emkc.org/api/v2/piston/execute \
     -H "Content-Type: application/json" \
     -d '{"language":"python","version":"3.10.0","files":[{"content":"print(\"Hello\")"}]}'
   ```

2. **Verify internet connection**:
   - Piston API requires internet
   - Check proxy settings
   - Test with other APIs

3. **Check code syntax**:
   - Ensure valid Python
   - Check indentation
   - Test locally first

---

#### Issue: Tests pass locally but fail in app

**Cause**: Different Python versions or environments

**Solution**:

1. **Check Python version**:
   ```bash
   python --version  # Should be 3.10+
   ```

2. **Test with same version**:
   - Piston uses Python 3.10.0
   - Match your local version

3. **Check test cases**:
   - Verify expected output format
   - Check for whitespace differences
   - Test edge cases

---

### Resume Upload Issues

#### Issue: Resume upload fails

**Symptoms**:
- "Resume upload failed" error
- PDF not parsing
- Empty resume context

**Solution**:

1. **Check file format**:
   - Must be PDF
   - Not password-protected
   - Not scanned image (needs text)

2. **Check file size**:
   - Keep under 10MB
   - Compress if needed

3. **Test PDF parsing**:
   ```python
   import pypdf
   import io
   
   with open('resume.pdf', 'rb') as f:
       reader = pypdf.PdfReader(f)
       text = reader.pages[0].extract_text()
       print(text)
   ```

---

### Performance Issues

#### Issue: Slow AI responses

**Cause**: Large conversation history or slow API

**Solution**:

1. **Clear conversation**:
   - Refresh page to start new session
   - History accumulates over time

2. **Check API latency**:
   - Test Gemini API directly
   - Check network speed

3. **Optimize model settings**:
   ```env
   # In .env, use faster model
   MODEL_ID=gemini-2.5-flash
   ```

---

#### Issue: High memory usage

**Cause**: Whisper model loaded in memory

**Solution**:

1. **Use smaller model**:
   ```env
   WHISPER_MODEL_SIZE=tiny.en  # Smaller, faster
   ```

2. **Restart server periodically**:
   ```bash
   # Stop and restart to clear memory
   ```

---

### Environment Issues

#### Issue: `.env` file not loading

**Symptoms**:
- Environment variables not set
- Using default values
- API keys not found

**Solution**:

1. **Check file location**:
   ```bash
   ls -la .env  # Should be in project root
   ```

2. **Check file format**:
   ```bash
   # No spaces around =
   GEMINI_API_KEY=your_key_here
   
   # Not this:
   GEMINI_API_KEY = your_key_here
   ```

3. **Test loading**:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   print(os.getenv('GEMINI_API_KEY'))
   ```

---

## 🐛 Debugging Tips

### Enable Debug Logging

```python
# In main3.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

### Check Browser Console

1. Open Developer Tools (F12)
2. Go to Console tab
3. Look for errors (red text)
4. Check Network tab for failed requests

### Check Server Logs

```bash
# Server logs show:
# - WebSocket connections
# - Tool calls
# - Errors and warnings
# - API responses
```

### Test Components Individually

```python
# Test Whisper
from faster_whisper import WhisperModel
model = WhisperModel("base.en")

# Test Gemini
from google import genai
client = genai.Client(api_key="...")

# Test TTS
import edge_tts
```

---

## 📞 Getting Help

### Before Asking for Help

1. **Check this guide** for your specific issue
2. **Review logs** for error messages
3. **Test components** individually
4. **Verify configuration** in `.env`

### When Reporting Issues

Include:
- **Error message** (full text)
- **Steps to reproduce**
- **Environment** (OS, Python version)
- **Configuration** (without API keys!)
- **Logs** (relevant portions)

### Useful Commands

```bash
# System info
python --version
pip list

# Test configuration
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Config loaded')"

# Check ports
netstat -an | grep 8000

# Test API
curl http://localhost:8000/api/config
```

---

## 🔍 Advanced Debugging

### WebSocket Debugging

```javascript
// In browser console
ws.addEventListener('message', (event) => {
    console.log('Received:', event.data);
});

ws.addEventListener('error', (event) => {
    console.error('WebSocket error:', event);
});
```

### Audio Debugging

```javascript
// Check audio context
console.log('Audio context state:', audioCtx.state);

// Check microphone stream
console.log('Mic tracks:', micStream.getTracks());

// Check analyser
const data = new Uint8Array(analyser.frequencyBinCount);
analyser.getByteFrequencyData(data);
console.log('Audio level:', data.reduce((a,b) => a+b) / data.length);
```

### Backend Debugging

```python
# Add breakpoints
import pdb; pdb.set_trace()

# Log everything
logger.debug(f"Variable value: {variable}")

# Check WebSocket state
logger.info(f"WebSocket state: {websocket.client_state}")
```

---

## Next Steps

- [Installation Guide](INSTALLATION.md)
- [Configuration Guide](CONFIGURATION.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [MCP Tools](MCP_TOOLS.md)
