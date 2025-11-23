"""Test script to debug the AI response issue WITH TOOLS"""
import os
import json
import random
from google import genai
from google.genai import types

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD_7RhGB-H1lDwUwSquj28jqrtgDTkGdF8")
MODEL_ID = "gemini-2.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY)

# Define tools
def get_random_problem():
    """Returns a random easy coding problem with test cases."""
    return json.dumps({
        "id": "1",
        "title": "Two Sum",
        "description": "Find two numbers that add up to target",
        "starter_code": "def two_sum(nums, target):\n    pass",
        "test_cases": []
    })

def verify_concept(topic: str):
    """Verifies a technical concept."""
    return f"Fact Check: {topic} is a valid concept."

# Test with tools
history = [
    {"role": "user", "parts": [{"text": "Hello, I'm a software engineer"}]}
]

system_prompt = """You are SURA, a friendly senior engineer. Keep it SHORT and CRISP.

TONE: Warm but brief (15-30 words per response).

CRITICAL: You MUST ask questions based on the candidate's RESUME.

Coding completed: False"""

print("Testing AI response WITH TOOLS...")
print(f"System prompt length: {len(system_prompt)}")

try:
    resp = client.models.generate_content(
        model=MODEL_ID,
        contents=history,
        config=types.GenerateContentConfig(
            tools=[get_random_problem, verify_concept],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
            system_instruction=system_prompt
        )
    )
    
    print(f"\nResponse object type: {type(resp)}")
    print(f"Has text attr: {hasattr(resp, 'text')}")
    print(f"Has candidates attr: {hasattr(resp, 'candidates')}")
    
    if hasattr(resp, 'candidates'):
        print(f"Number of candidates: {len(resp.candidates)}")
        if resp.candidates:
            print(f"First candidate: {resp.candidates[0]}")
    
    try:
        text = resp.text
        print(f"\n✅ Response text: {text}")
    except ValueError as e:
        print(f"\n❌ ValueError accessing text: {e}")
        print("This is the error we're seeing!")
    except Exception as e:
        print(f"\n❌ Error accessing text: {type(e).__name__}: {e}")
        
except Exception as e:
    print(f"\n❌ Error during API call: {type(e).__name__}: {e}")
