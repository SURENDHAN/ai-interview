"""Test script to debug the AI response issue"""
import os
from google import genai
from google.genai import types

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD_7RhGB-H1lDwUwSquj28jqrtgDTkGdF8")
MODEL_ID = "gemini-2.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY)

# Test with a simple prompt
history = [
    {"role": "user", "parts": [{"text": "Hello, tell me about yourself"}]}
]

system_prompt = """You are SURA, a friendly senior engineer. Keep it SHORT and CRISP.

TONE: Warm but brief (15-30 words per response). Encouraging: "Nice!", "Good!", "Makes sense!"

CRITICAL: You MUST ask questions based on the candidate's RESUME and the ROLE they selected. DO NOT ask generic questions."""

print("Testing AI response...")
print(f"System prompt length: {len(system_prompt)}")

try:
    resp = client.models.generate_content(
        model=MODEL_ID,
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )
    
    print(f"\nResponse object: {resp}")
    print(f"Has text attr: {hasattr(resp, 'text')}")
    
    try:
        text = resp.text
        print(f"Response text: {text}")
    except Exception as e:
        print(f"Error accessing text: {e}")
        print(f"Response candidates: {resp.candidates if hasattr(resp, 'candidates') else 'No candidates'}")
        
except Exception as e:
    print(f"Error during API call: {e}")
