# MCP Tools (Model Context Protocol)

## 🛠️ Overview

The application uses **MCP tools** to extend the AI's capabilities during interviews. These tools are automatically called by the Gemini AI model when needed, following the Model Context Protocol standard.

## 📚 Available MCP Tools

### 1. `get_random_problem()`

**Purpose**: Fetches a random coding problem from the question bank for technical interviews.

**Function Signature**:
```python
def get_random_problem() -> str
```

**How it works**:
1. Loads problems from `questions.json`
2. Filters for "easy" difficulty problems
3. Randomly selects one problem
4. Returns JSON with problem details

**Returns**:
```json
{
  "id": "1",
  "title": "Two Sum",
  "description": "Given an array of integers...",
  "starter_code": "def solve(nums, target):\n    pass",
  "test_cases": [
    {
      "input_code": "print(solve([2,7,11,15], 9))",
      "expected": "[0, 1]"
    }
  ]
}
```

**When AI calls it**:
- User asks for a coding challenge
- Interview flow reaches coding phase
- AI detects need for technical assessment

**Code Location**: `main3.py` lines 200-214

---

### 2. `verify_concept(topic: str)`

**Purpose**: Fact-checks technical concepts using Wikipedia during interviews.

**Function Signature**:
```python
def verify_concept(topic: str) -> str
```

**Parameters**:
- `topic` (str): Technical concept to verify (e.g., "Binary Search Tree", "REST API")

**How it works**:
1. Searches Wikipedia for the topic
2. Retrieves the top result
3. Extracts a 3-sentence summary
4. Returns formatted fact-check

**Returns**:
```
Fact Check:
A binary search tree (BST) is a data structure in which each node has at most two children. 
The left subtree contains only nodes with keys less than the parent node. 
The right subtree contains only nodes with keys greater than the parent node.
```

**When AI calls it**:
- User makes a technical claim
- AI needs to verify accuracy
- Discussion involves complex concepts

**Code Location**: `main3.py` lines 216-223

---

### 3. `submit_code(problem_id: str, user_code: str)`

**Purpose**: Executes and validates user's code against test cases.

**Function Signature**:
```python
def submit_code(problem_id: str, user_code: str) -> str
```

**Parameters**:
- `problem_id` (str): ID of the coding problem
- `user_code` (str): User's submitted Python code

**How it works**:
1. Retrieves problem from question bank
2. Iterates through all test cases
3. Executes code using Piston API
4. Compares output with expected results
5. Returns pass/fail for each test

**Returns**:
```
Test 1: PASSED
Test 2: PASSED
Test 3: FAILED IndexError: list index out of range
```

**Security**:
- Code runs in isolated Piston API sandbox
- No access to local file system
- Timeout protection
- Resource limits enforced

**Code Location**: `main3.py` lines 239-254

---

## 🔧 MCP Tool Integration

### Registration with Gemini AI

Tools are registered using Google's Generative AI SDK:

```python
from google.genai import types

resp = client.models.generate_content(
    model=Config.MODEL_ID,
    contents=history,
    config=types.GenerateContentConfig(
        tools=[get_random_problem, verify_concept],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False
        ),
        system_instruction=system_prompt
    )
)
```

### Automatic Function Calling

**How it works**:
1. AI analyzes conversation context
2. Determines if a tool is needed
3. Calls tool with appropriate parameters
4. Receives tool response
5. Incorporates result into conversation

**Benefits**:
- ✅ No manual tool invocation needed
- ✅ AI decides optimal timing
- ✅ Seamless user experience
- ✅ Context-aware tool usage

---

## 🔄 Code Execution Flow

```
┌─────────────────┐
│  User submits   │
│      code       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Frontend      │
│ WebSocket send  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Backend      │
│  receives msg   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  submit_code()  │
│   MCP Tool      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Piston API    │
│ Execute Python  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Test Validation │
│ Compare outputs │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return results  │
│  to frontend    │
└─────────────────┘
```

---

## ➕ Adding Custom MCP Tools

### Step 1: Define the Function

Create a new function in `main3.py`:

```python
def my_custom_tool(param: str) -> str:
    """
    Brief description of what this tool does.
    
    The AI will use this docstring to understand when to call the tool.
    Be clear and specific about the tool's purpose.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of what the tool returns
    """
    # Your implementation here
    result = do_something(param)
    return result
```

### Step 2: Register with AI Model

Add your tool to the tools list:

```python
config=types.GenerateContentConfig(
    tools=[
        get_random_problem, 
        verify_concept, 
        my_custom_tool  # Add your tool here
    ],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=False
    ),
    system_instruction=system_prompt
)
```

### Step 3: Test the Tool

The AI will automatically call your tool when appropriate based on:
- The tool's docstring
- Function name
- Parameter types
- Conversation context

### Best Practices

1. **Clear Docstrings**: AI uses them to understand tool purpose
2. **Type Hints**: Use Python type hints for parameters and returns
3. **Error Handling**: Return meaningful error messages
4. **JSON Returns**: Return JSON strings for structured data
5. **Idempotent**: Tools should be safe to call multiple times

---

## 🧪 Testing MCP Tools

### Manual Testing

Test tools directly in Python:

```python
# Test get_random_problem
from main3 import get_random_problem
import json

result = get_random_problem()
problem = json.loads(result)
print(f"Problem: {problem['title']}")

# Test verify_concept
from main3 import verify_concept

info = verify_concept("Machine Learning")
print(info)

# Test submit_code
from main3 import submit_code

code = """
def solve(nums, target):
    return [0, 1]
"""
result = submit_code("1", code)
print(result)
```

### Integration Testing

Test tools through the AI conversation:

1. Start an interview
2. Trigger tool usage naturally
3. Verify tool is called
4. Check results are incorporated

---

## 📊 Tool Usage Analytics

Monitor tool usage in logs:

```
INFO - 🤖 Sending to AI with history length: 5
INFO - ✅ Got text response: Great! Let's do a coding problem...
INFO - 🔧 Tool called: get_random_problem
INFO - ✅ Tool result: {"id": "1", "title": "Two Sum"...}
```

---

## 🔍 Debugging Tools

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Tool Responses

```python
logger.debug(f"Tool response: {tool_result}")
```

### Verify Tool Registration

```python
print(f"Registered tools: {[tool.__name__ for tool in tools]}")
```

---

## Next Steps

- [Understand the architecture](ARCHITECTURE.md)
- [Configuration guide](CONFIGURATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)
