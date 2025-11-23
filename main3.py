import asyncio
import os
import json
import logging
import io
import tempfile
import requests
import re
import random
import sys
import wikipedia
import string
import pypdf
from fastapi import UploadFile, File
from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel
from google import genai
from google.genai import types
import edge_tts
from pydub import AudioSegment
from starlette.websockets import WebSocketState

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_ID = os.getenv("MODEL_ID", "gemini-2.5-flash")
    WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base.en")
    WHISPER_COMPUTE = os.getenv("WHISPER_COMPUTE", "int8")
    VOICE_NAME = os.getenv("VOICE_NAME", "en-US-AriaNeural")
    QUESTIONS_FILE = os.getenv("QUESTIONS_FILE", "questions.json")
    PISTON_API_URL = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston/execute")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Interview prompts for different roles
INTERVIEW_PROMPTS = {
    "software_engineer": """You are SURA, a friendly senior engineer. Keep it SHORT and CRISP.

TONE: Warm but brief (15-30 words per response). Encouraging: "Nice!", "Good!", "Makes sense!"

CRITICAL: You MUST ask questions based on the candidate's RESUME and the ROLE they selected. DO NOT ask generic questions.

INTERVIEW FLOW (FAST):
1. OPENING: "Tell me about yourself and what brings you here?"
   - After they answer, ask about SPECIFIC projects/technologies mentioned in their RESUME
   - Example: "I see you worked on [PROJECT from resume]. Tell me about your role there?"

2. ASK 2-3 TECHNICAL QUESTIONS based on THEIR RESUME:
   - Look at technologies/languages in their resume
   - Ask about specific frameworks/tools they mentioned
   - Example: "You mentioned [TECH from resume]. How did you use it in [PROJECT]?"
   - Example: "Tell me about a challenge you faced with [TECH from resume]?"
   
3. CODING: "Great! Let's do a coding problem. Click 'START CODING CHALLENGE'."

4. AFTER CODING: Ask 1 follow-up: "Walk me through your approach?"

5. CLOSE: "Nice work! Any questions?" → [[END_INTERVIEW]]

RULES:
- ALWAYS reference their resume in questions
- Ask about THEIR specific experience, not generic concepts
- Total interview: 4-5 questions MAX
- Responses: 15-30 words only
- Be encouraging but move fast
- Coding is MANDATORY""",

    "product_manager": """You are SURA, a product leadership interviewer. Be CONCISE - max 2-3 sentences per response.

CRITICAL: Ask questions based on the candidate's RESUME and their product management experience.

FLOW:
1. Ask about SPECIFIC products/projects from their RESUME
   - Example: "I see you worked on [PRODUCT from resume]. What metrics did you track?"
2. Ask about their decision-making process on a SPECIFIC project from resume
3. Say: "Let's do a product case study. Click the 'START CODING CHALLENGE' button."
4. After exercise, ask 1-2 questions about their decisions
5. Say [[END_INTERVIEW]]

RULES: Keep ALL responses under 3 sentences. ALWAYS reference their resume. Focus on metrics. Case study is MANDATORY.""",

    "sales": """You are SURA, a sales director interviewer. Be CONCISE - max 2-3 sentences per response.

CRITICAL: Ask questions based on the candidate's RESUME and their sales experience.

FLOW:
1. Ask about SPECIFIC companies/products they sold (from resume)
   - Example: "I see you worked at [COMPANY]. What was your quota and achievement rate?"
2. Ask about their biggest deal mentioned in resume
3. Present 1 objection-handling scenario related to their industry
4. Say [[END_INTERVIEW]]

RULES: Keep ALL responses under 3 sentences. ALWAYS reference their resume. Focus on numbers. Be direct. NO coding.""",

    "retail": """You are SURA, a retail manager interviewer. Be CONCISE - max 2-3 sentences per response.

CRITICAL: Ask questions based on the candidate's RESUME and their retail/customer service experience.

FLOW:
1. Ask about SPECIFIC retail positions from their resume
   - Example: "I see you worked at [STORE from resume]. Tell me about your customer service approach?"
2. Ask about a challenging customer situation they mentioned or might have faced
3. Ask about availability and teamwork based on their previous roles
4. Say [[END_INTERVIEW]]

RULES: Keep ALL responses under 3 sentences. ALWAYS reference their resume. Be friendly. Focus on scenarios. NO coding.""",

    "general": """You are SURA, a professional interviewer. Be CONCISE - max 2-3 sentences per response.

CRITICAL: Ask questions based on the candidate's RESUME and their background.

FLOW:
1. Ask about SPECIFIC experiences/roles from their resume
   - Example: "I see you worked at [COMPANY from resume]. What were your main responsibilities?"
2. Ask behavioral questions related to their SPECIFIC experiences in resume
   - Use STAR method, reference their actual projects/roles
3. Ask about goals and why this role fits their background
4. Say [[END_INTERVIEW]]

RULES: Keep ALL responses under 3 sentences. ALWAYS reference their resume. Be professional. Focus on STAR method. NO coding."""
}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

whisper_model = None
client = None
QUESTION_BANK = []
RESUME_CONTEXT = ""

# --- SERVE STATIC FILES ---
@app.get("/")
@app.get("/index.html")
@app.get("/index2.html")
async def serve_index():
    return FileResponse("index2.html")

@app.get("/login.html")
async def serve_login():
    return FileResponse("login.html")

@app.get("/api/config")
async def get_config():
    """Serve Firebase configuration from environment variables"""
    return {
        "firebase": {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
            "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
        }
    }

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    global RESUME_CONTEXT
    try:
        contents = await file.read()
        pdf_reader = pypdf.PdfReader(io.BytesIO(contents))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        RESUME_CONTEXT = text.strip()
        logger.info(f"📄 Resume uploaded. Length: {len(RESUME_CONTEXT)} chars")
        return {"status": "success", "length": len(RESUME_CONTEXT)}
    except Exception as e:
        logger.error(f"Resume upload failed: {e}")
        return {"status": "error", "message": str(e)}

# --- TOOLS ---

def load_questions(filepath: str = Config.QUESTIONS_FILE):
    global QUESTION_BANK
    if not os.path.exists(filepath):
        QUESTION_BANK = []
        return
    try:
        with open(filepath, 'r') as f:
            QUESTION_BANK = json.load(f)
    except: QUESTION_BANK = []

def get_random_problem():
    """Returns a random easy coding problem with test cases."""
    if not QUESTION_BANK: load_questions()
    if not QUESTION_BANK: return json.dumps({"error": "No questions"})
    # Filter for easy problems only
    easy_problems = [p for p in QUESTION_BANK if p.get("difficulty") == "easy"]
    if not easy_problems: easy_problems = QUESTION_BANK  # Fallback
    p = random.choice(easy_problems)
    return json.dumps({
        "id": str(p.get("id", "0")), 
        "title": p.get("title", ""), 
        "description": p.get("description", ""), 
        "starter_code": p.get("signature", ""),
        "test_cases": p.get("test_cases", [])
    })

def verify_concept(topic: str):
    """Verifies a technical concept using Wikipedia."""
    try:
        res = wikipedia.search(topic)
        if not res: return "No Wikipedia page found."
        summary = wikipedia.summary(res[0], sentences=3)
        return f"Fact Check:\n{summary}"
    except: return "Could not verify."

def execute_piston(script: str):
    try:
        resp = requests.post(Config.PISTON_API_URL, json={"language": "python", "version": "3.10.0", "files": [{"content": script}]}).json()
        return resp
    except: return None

def run_playground_code(user_code: str):
    """Runs code without test cases."""
    resp = execute_piston(user_code)
    if not resp: return "Network Error"
    out = resp.get("run", {}).get("stdout", "")
    err = resp.get("run", {}).get("stderr", "")
    return (out + "\n" + err).strip()

def submit_code(problem_id: str, user_code: str):
    """Runs user code against test cases."""
    if not QUESTION_BANK: load_questions()
    problem = next((p for p in QUESTION_BANK if str(p["id"]) == str(problem_id)), None)
    if not problem: return "Invalid Problem ID."
    
    results = []
    for i, test in enumerate(problem.get("test_cases", []), 1):
        script = f"{user_code}\n\n{test['input_code']}"
        resp = execute_piston(script)
        if resp and "run" in resp and resp["run"]["stdout"].strip() == test["expected"].strip():
            results.append(f"Test {i}: PASSED")
        else:
            err = resp.get("run", {}).get("stderr", "") if resp else "Network Error"
            results.append(f"Test {i}: FAILED {err}")
    return "\n".join(results)

# --- FEEDBACK GENERATION ---
def generate_feedback(history: list, role: str) -> dict:
    """Generate interview feedback based on conversation history and role."""
    try:
        # Create a prompt for feedback generation
        feedback_prompt = f"""Analyze this {role.replace('_', ' ')} interview and provide detailed, comprehensive feedback.

Interview Transcript:
{json.dumps(history, indent=2)}

Provide feedback in the following JSON format:
{{
    "overall_score": <1-10>,
    "communication": {{"score": <1-10>, "feedback": "..."}},
    "technical_knowledge": {{"score": <1-10>, "feedback": "..."}},
    "problem_solving": {{"score": <1-10>, "feedback": "..."}},
    "strengths": ["strength1", "strength2", "strength3"],
    "improvements": ["area1", "area2", "area3"],
    "summary": "Overall assessment..."
}}

Be specific, constructive, and actionable. Provide detailed feedback."""

        resp = client.models.generate_content(
            model=Config.MODEL_ID,
            contents=feedback_prompt
        )
        
        # Parse JSON from response
        feedback_text = resp.text
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', feedback_text, re.DOTALL)
        if json_match:
            feedback_data = json.loads(json_match.group())
        else:
            feedback_data = {
                "overall_score": 7,
                "communication": {"score": 7, "feedback": "Good communication throughout"},
                "technical_knowledge": {"score": 7, "feedback": "Demonstrated knowledge"},
                "problem_solving": {"score": 7, "feedback": "Approached problems logically"},
                "strengths": ["Clear communication", "Good attitude"],
                "improvements": ["More specific examples", "Deeper technical details"],
                "summary": "Overall solid performance in the interview."
            }
        
        # Save feedback to file
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"interview_feedback_{role}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"INTERVIEW FEEDBACK - {role.replace('_', ' ').upper()}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"OVERALL SCORE: {feedback_data['overall_score']}/10\n\n")
            
            f.write("DETAILED SCORES:\n")
            f.write(f"  • Communication: {feedback_data['communication']['score']}/10\n")
            f.write(f"    {feedback_data['communication']['feedback']}\n\n")
            f.write(f"  • Technical Knowledge: {feedback_data['technical_knowledge']['score']}/10\n")
            f.write(f"    {feedback_data['technical_knowledge']['feedback']}\n\n")
            f.write(f"  • Problem Solving: {feedback_data['problem_solving']['score']}/10\n")
            f.write(f"    {feedback_data['problem_solving']['feedback']}\n\n")
            
            f.write("STRENGTHS:\n")
            for i, strength in enumerate(feedback_data['strengths'], 1):
                f.write(f"  {i}. {strength}\n")
            f.write("\n")
            
            f.write("AREAS FOR IMPROVEMENT:\n")
            for i, improvement in enumerate(feedback_data['improvements'], 1):
                f.write(f"  {i}. {improvement}\n")
            f.write("\n")
            
            f.write("SUMMARY:\n")
            f.write(f"{feedback_data['summary']}\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("Full Interview Transcript:\n")
            f.write("=" * 60 + "\n")
            f.write(json.dumps(history, indent=2))
        
        logger.info(f"📄 Feedback saved to: {filename}")
        feedback_data['filename'] = filename  # Add filename to response
        return feedback_data
        
    except Exception as e:
        logger.error(f"Feedback generation error: {e}")
        return {"error": "Could not generate feedback"}

# --- STARTUP ---
@app.on_event("startup")
def startup():
    global whisper_model, client
    load_questions()
    logger.info(f"🚀 Loading Whisper ({Config.WHISPER_MODEL_SIZE})...")
    whisper_model = WhisperModel(Config.WHISPER_MODEL_SIZE, device="cpu", compute_type=Config.WHISPER_COMPUTE)
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    logger.info("✅ Ready")

# --- HELPERS ---
async def generate_tts(text: str):
    clean = text.replace("*", "").strip()
    if not clean: return None
    try:
        logger.info(f"🔊 Generating TTS for: {clean[:50]}...")
        comm = edge_tts.Communicate(clean, Config.VOICE_NAME)
        out = b""
        async for chunk in comm.stream():
            if chunk["type"] == "audio": out += chunk["data"]
        logger.info(f"✅ TTS Generated: {len(out)} bytes")
        return out
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        return None

def transcribe(data: bytes):
    try:
        audio = AudioSegment.from_file(io.BytesIO(data)).set_frame_rate(16000).set_channels(1)
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(wav_io.read())
            tpath = tmp.name
        
        # Enhanced transcription settings to reduce hallucinations
        segs, info = whisper_model.transcribe(
            tpath, 
            beam_size=1,
            temperature=0.0,
            vad_filter=True,  # Voice Activity Detection to filter silence
            condition_on_previous_text=False,  # Prevent repetitive hallucinations
            log_prob_threshold=-1.0,  # Filter low-confidence segments
            no_speech_threshold=0.6,  # Higher threshold for detecting silence
            compression_ratio_threshold=2.4  # Detect repetitive text
        )
        
        # Filter segments by log probability and no_speech_prob
        filtered_segments = []
        for seg in segs:
            # Skip segments with low confidence or high no_speech probability
            if hasattr(seg, 'avg_logprob') and seg.avg_logprob < -1.0:
                logger.info(f"🔇 Skipped low-confidence segment: {seg.text}")
                continue
            if hasattr(seg, 'no_speech_prob') and seg.no_speech_prob > 0.6:
                logger.info(f"🔇 Skipped likely silence: {seg.text}")
                continue
            filtered_segments.append(seg.text)
        
        text = " ".join(filtered_segments).strip()
        os.remove(tpath)
        
        cleaned = text.lower().translate(str.maketrans('', '', string.punctuation)).strip()
        
        # Advanced hallucination detection
        
        # 1. Check for repetitive patterns (e.g., "a little bit of" repeated)
        words = cleaned.split()
        if len(words) > 10:
            # Check for repeated sequences
            # Look for 3-word, 4-word, and 5-word patterns
            for pattern_length in [3, 4, 5]:
                if len(words) >= pattern_length * 3:  # At least 3 repetitions
                    pattern = ' '.join(words[:pattern_length])
                    # Count how many times this pattern appears
                    pattern_count = cleaned.count(pattern)
                    if pattern_count >= 3:
                        logger.info(f"🔇 Filtered repetitive pattern: '{pattern}' repeated {pattern_count} times")
                        return ""
        
        # 2. Check for excessive word repetition
        if len(words) > 5:
            unique_words = set(words)
            repetition_ratio = len(words) / len(unique_words)
            if repetition_ratio > 4:  # Same words repeated too many times
                logger.info(f"🔇 Filtered excessive repetition: ratio {repetition_ratio:.1f}")
                return ""
        
        # 3. Common Whisper hallucinations
        hallucinations = [
            "thanks for watching", "thank you for watching", "please subscribe",
            "like and subscribe", "don't forget to subscribe",
            "thank you", "you", "bye", "okay", "ok", "be", "to", "the", "it", "i", "me",
            "a little bit of", "um", "uh", "hmm"
        ]
        
        # Check if the text is just a repetition of hallucination phrases
        if not words: 
            return ""
        
        # Check if entire text matches common hallucinations
        is_hallucination = all(w in hallucinations for w in words)
        
        # Check if text is too short or matches hallucination patterns
        if is_hallucination or len(cleaned) < 2:
            logger.info(f"🔇 Filtered hallucination: '{text}'")
            return ""
        
        # 4. Check if text is mostly filler words
        filler_words = {"a", "the", "of", "to", "and", "in", "is", "it", "that", "for", "on", "with", "as", "at", "by"}
        if len(words) > 3:
            filler_count = sum(1 for w in words if w in filler_words)
            if filler_count / len(words) > 0.8:  # More than 80% filler words
                logger.info(f"🔇 Filtered filler-heavy text: '{text}'")
                return ""
            
        logger.info(f"🎤 User: {text}")
        return text
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""

# --- WEBSOCKET ---
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("🔌 Connected")
    
    # Connection state
    history = []
    coding_phase = False
    coding_completed = False
    selected_role = "general"  # Default role

    async def send_txt(t):
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json({"type": "text", "content": t, "sender": "agent"})
        except: pass

    async def send_aud(b):
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_bytes(b)
        except: pass

    async def send_json_raw(j):
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(j)
        except: pass

    # Wait for role selection
    try:
        msg = await websocket.receive()
        data = json.loads(msg["text"])
        if data.get("type") == "role_selection":
            selected_role = data.get("role", "general")
            logger.info(f"📋 Role selected: {selected_role}")
    except:
        selected_role = "general"

    # Initial Greeting based on role
    if RESUME_CONTEXT:
        greeting = f"Hello! I am SURA, your interview practice partner. I've reviewed your resume and I'll be conducting a {selected_role.replace('_', ' ')} interview today. Let's begin - tell me about yourself?"
    else:
        greeting = f"Hello! I am SURA, your interview practice partner. I'll be conducting a {selected_role.replace('_', ' ')} interview today. Let's begin - tell me about yourself?"
    history.append({"role": "model", "parts": [{"text": greeting}]})
    await send_txt(greeting)
    aud = await generate_tts(greeting)
    if aud: await send_aud(aud)

    try:
        while True:
            try:
                msg = await websocket.receive()
            except (WebSocketDisconnect, RuntimeError):
                logger.info("👋 Client Disconnected")
                break
            
            if msg["type"] == "websocket.disconnect": break
            
            user_text = ""
            if "bytes" in msg:
                if coding_phase:
                    continue
                user_text = await asyncio.to_thread(transcribe, msg['bytes'])
                if not user_text: continue
                await send_txt(user_text)

            elif "text" in msg:
                try:
                    data = json.loads(msg["text"])
                    if data.get("type") == "code_submission":
                        if data.get("problem_id"):
                            res = submit_code(data["problem_id"], data["code"])
                            if "FAILED" not in res:
                                coding_phase = False
                                coding_completed = True
                        else:
                            res = run_playground_code(data["code"])
                        await send_json_raw({"type": "code_result", "output": res})
                        user_text = f"Code Submitted. Result:\n{res}"
                    elif data.get("type") == "request_feedback":
                        # Generate and send feedback
                        feedback = generate_feedback(history, selected_role)
                        await send_json_raw({"type": "feedback", "data": feedback})
                        continue
                    elif data.get("type") == "drop_test":
                        logger.info("❌ User dropped the coding test")
                        coding_completed = True
                        user_text = "[SYSTEM: User dropped the coding test. They get 0 marks for this section. Please acknowledge this briefly and continue with the next part of the interview.]"
                    else: 
                        user_text = data.get("text", "")
                        if coding_phase and user_text:
                            continue
                except: user_text = msg["text"]

            if not user_text: continue

            history.append({"role": "user", "parts": [{"text": user_text}]})
            
            # Get role-specific system prompt
            system_prompt = INTERVIEW_PROMPTS.get(selected_role, INTERVIEW_PROMPTS["general"])
            if RESUME_CONTEXT:
                # Limit resume context to prevent token overflow (max 800 chars for safety)
                resume_snippet = RESUME_CONTEXT[:800] if len(RESUME_CONTEXT) > 800 else RESUME_CONTEXT
                system_prompt += f"\n\nCANDIDATE RESUME:\n{resume_snippet}\n\nAsk specific questions about their resume."
                logger.info(f"📄 Using resume context ({len(resume_snippet)} chars)")
            system_prompt += f"\n\nCoding completed: {coding_completed}"
            logger.info(f"🤖 Sending to AI with history length: {len(history)}")
            
            try:
                resp = client.models.generate_content(
                    model=Config.MODEL_ID, contents=history,
                    config=types.GenerateContentConfig(
                        tools=[get_random_problem, verify_concept],
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
                        system_instruction=system_prompt
                    )
                )
                
                # Better handling of empty responses and function calls
                reply = None
                try:
                    # When automatic_function_calling is enabled, the response might have:
                    # 1. Just text
                    # 2. Function calls that were executed automatically
                    # 3. Both
                    # 4. Neither (error case)
                    
                    if resp and hasattr(resp, 'candidates') and resp.candidates:
                        # Check if there's actual content
                        candidate = resp.candidates[0]
                        if hasattr(candidate, 'content') and candidate.content:
                            # Try to get text
                            if hasattr(resp, 'text'):
                                try:
                                    reply = resp.text
                                    if reply:
                                        logger.info(f"✅ Got text response: {reply[:50]}...")
                                except ValueError:
                                    # This happens when response only has function calls
                                    logger.info("ℹ️ Response contains only function calls, no text")
                    
                    # If still no reply, check if it was a function-only response
                    if not reply and resp and hasattr(resp, 'candidates'):
                        logger.warning("⚠️ No text in response after function calling")
                        
                except (ValueError, AttributeError) as e:
                    logger.warning(f"⚠️ Could not extract text from response: {e}")
                
                if not reply or len(reply.strip()) == 0:
                    logger.warning("⚠️ Model returned empty response, using fallback")
                    reply = "I see. Could you tell me more about that?"
                
                # Check for interview end
                if "[[END_INTERVIEW]]" in reply:
                    reply = reply.replace("[[END_INTERVIEW]]", "").strip()
                    history.append({"role": "model", "parts": [{"text": reply}]})
                    await send_txt(reply)
                    aud = await generate_tts(reply)
                    if aud: await send_aud(aud)
                    
                    # Generate and send feedback
                    feedback = generate_feedback(history, selected_role)
                    await send_json_raw({"type": "feedback", "data": feedback})
                    continue
                
                # Check if AI wants to give coding problem (ONLY for technical roles)
                if ('"starter_code"' in reply or "START CODING CHALLENGE" in reply) and not coding_completed and selected_role in ["software_engineer", "product_manager"]:
                    problem_json = get_random_problem()
                    try:
                        problem_data = json.loads(problem_json)
                        await send_json_raw({"type": "show_button", "problem": problem_data})
                        if '"starter_code"' in reply:
                            m = re.search(r'\{[^{}]*"starter_code"[^{}]*\}', reply, re.DOTALL)
                            if m:
                                reply = reply.replace(m.group(0), "")
                    except Exception as e:
                        logger.error(f"Problem data error: {e}")

                history.append({"role": "model", "parts": [{"text": reply}]})
                await send_txt(reply)
                
                # Skip TTS during coding phase
                if not coding_phase:
                    aud = await generate_tts(reply)
                    if aud: await send_aud(aud)
                else:
                    logger.info("🔇 Skipping TTS during coding phase")

            except Exception as e:
                logger.error(f"AI Error: {e}")
                # Provide fallback response on error
                error_reply = "I apologize, I had a technical issue. Could you please repeat that?"
                history.append({"role": "model", "parts": [{"text": error_reply}]})
                await send_txt(error_reply)
                aud = await generate_tts(error_reply)
                if aud: await send_aud(aud)

    except Exception as e:
        logger.error(f"Socket Loop Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
