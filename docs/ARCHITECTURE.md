# Architecture Documentation

## 📁 Project Structure

```
gpt/
├── main3.py              # FastAPI backend server
├── index2.html           # Main interview interface
├── login.html            # Authentication page
├── questions.json        # Coding challenge database
├── .env                  # Environment variables (DO NOT COMMIT)
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── README.md             # Main documentation
└── docs/                 # Documentation folder
    ├── INSTALLATION.md   # Setup guide
    ├── CONFIGURATION.md  # Config guide
    ├── MCP_TOOLS.md      # MCP tools docs
    ├── ARCHITECTURE.md   # This file
    └── TROUBLESHOOTING.md # Common issues
```

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ login.html   │  │ index2.html  │  │ Ace Editor   │      │
│  │ (Firebase)   │  │ (Interview)  │  │ (Code)       │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          │ HTTP/WS          │ WebSocket        │ WebSocket
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼──────────────┐
│         ▼                  ▼                  ▼              │
│  ┌──────────────────────────────────────────────────┐       │
│  │            FastAPI Backend (main3.py)            │       │
│  ├──────────────────────────────────────────────────┤       │
│  │  • /login.html - Serve login page                │       │
│  │  • /api/config - Firebase config endpoint        │       │
│  │  • /upload_resume - Resume upload                │       │
│  │  • /ws - WebSocket for interview                 │       │
│  └──────────────┬───────────────────────────────────┘       │
│                 │                                            │
│                 ▼                                            │
│  ┌──────────────────────────────────────────────────┐       │
│  │              MCP Tools Layer                     │       │
│  ├──────────────────────────────────────────────────┤       │
│  │  • get_random_problem()                          │       │
│  │  • verify_concept()                              │       │
│  │  • submit_code()                                 │       │
│  └──────────────┬───────────────────────────────────┘       │
│                 │                                            │
└─────────────────┼────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Gemini AI    │  │ Piston API   │  │ Wikipedia    │      │
│  │ (Responses)  │  │ (Code Exec)  │  │ (Fact Check) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Request Flow

### 1. Login Flow

```
User → login.html → /api/config → Firebase Config
                  ↓
            Firebase Auth (Google)
                  ↓
            Upload Resume (optional)
                  ↓
            Redirect to index2.html
```

### 2. Interview Flow

```
User selects role → WebSocket /ws → Backend
                                   ↓
                            AI generates greeting
                                   ↓
                            TTS audio generated
                                   ↓
User speaks → Whisper STT → Text → AI processes
                                   ↓
                            AI response + Tools
                                   ↓
                            TTS audio + Text
                                   ↓
                            Sent to frontend
```

### 3. Coding Challenge Flow

```
AI decides coding needed → get_random_problem()
                                   ↓
                         Problem sent to frontend
                                   ↓
                         User writes code
                                   ↓
                         Submit button clicked
                                   ↓
                         submit_code() called
                                   ↓
                         Piston API executes
                                   ↓
                         Results returned
```

## 🧩 Component Details

### Frontend Components

#### `login.html`
- **Purpose**: User authentication
- **Features**:
  - Google Sign-In with Firebase
  - Resume upload (PDF)
  - Dynamic Firebase config loading
- **Technologies**: Vanilla JS, Firebase Auth, TailwindCSS

#### `index2.html`
- **Purpose**: Main interview interface
- **Layouts**:
  1. Role Selection Screen
  2. Chat Interface (voice/text)
  3. Coding Editor (HackerRank-style)
  4. Feedback Screen
- **Features**:
  - WebSocket communication
  - Voice Activity Detection (VAD)
  - Ace Code Editor
  - Real-time audio playback
- **Technologies**: Vanilla JS, WebSocket, Ace Editor, TailwindCSS

### Backend Components

#### `main3.py`
**Main FastAPI Application**

**Key Classes**:
- `Config`: Environment configuration loader

**Key Functions**:

1. **HTTP Endpoints**:
   - `serve_index()`: Serve main app
   - `serve_login()`: Serve login page
   - `get_config()`: Serve Firebase config
   - `upload_resume()`: Handle resume uploads

2. **WebSocket Handler**:
   - `ws_endpoint()`: Main interview WebSocket

3. **MCP Tools**:
   - `get_random_problem()`: Fetch coding problems
   - `verify_concept()`: Wikipedia fact-checking
   - `submit_code()`: Code execution & validation

4. **Helper Functions**:
   - `generate_tts()`: Text-to-speech conversion
   - `transcribe()`: Speech-to-text conversion
   - `generate_feedback()`: Interview feedback generation

## 🔌 WebSocket Protocol

### Message Types

#### Client → Server

**1. Role Selection**:
```json
{
  "type": "role_selection",
  "role": "software_engineer"
}
```

**2. Audio Data**:
```
Binary WebM audio blob
```

**3. Code Submission**:
```json
{
  "type": "code_submission",
  "problem_id": "1",
  "code": "def solve():\n    return []"
}
```

**4. Request Feedback**:
```json
{
  "type": "request_feedback"
}
```

**5. Drop Test**:
```json
{
  "type": "drop_test"
}
```

#### Server → Client

**1. Text Message**:
```json
{
  "type": "text",
  "content": "Hello! Tell me about yourself.",
  "sender": "agent"
}
```

**2. Audio Data**:
```
Binary PCM audio data
```

**3. Show Coding Button**:
```json
{
  "type": "show_button",
  "problem": {
    "id": "1",
    "title": "Two Sum",
    "description": "...",
    "starter_code": "...",
    "test_cases": [...]
  }
}
```

**4. Code Results**:
```json
{
  "type": "code_result",
  "output": "Test 1: PASSED\nTest 2: PASSED"
}
```

**5. Feedback**:
```json
{
  "type": "feedback",
  "data": {
    "overall_score": 8,
    "communication": {...},
    "technical_knowledge": {...},
    "strengths": [...],
    "improvements": [...],
    "summary": "..."
  }
}
```

## 🗄️ Data Models

### Question Format (`questions.json`)

```json
{
  "id": 1,
  "title": "Two Sum",
  "description": "Given an array of integers...",
  "difficulty": "easy",
  "signature": "def solve(nums, target):\n    pass",
  "test_cases": [
    {
      "input_code": "print(solve([2,7,11,15], 9))",
      "expected": "[0, 1]"
    }
  ]
}
```

### Interview History Format

```python
history = [
    {
        "role": "model",
        "parts": [{"text": "Hello! Tell me about yourself."}]
    },
    {
        "role": "user",
        "parts": [{"text": "I'm a software engineer..."}]
    }
]
```

## 🔐 Security Architecture

### Authentication Flow

```
User → Firebase Auth → ID Token → Backend validates → Session created
```

### API Key Protection

- All keys in `.env` file
- `.env` excluded from git
- Firebase config served via backend API
- No client-side key exposure

### Code Execution Security

- Piston API sandbox
- No local file system access
- Timeout limits
- Resource constraints

## 🎯 State Management

### Frontend State

```javascript
// Global state variables
let ws;              // WebSocket connection
let audioCtx;        // Audio context
let micStream;       // Microphone stream
let selectedRole;    // Selected interview role
let codingPhaseActive; // Coding phase flag
let pendingProblem;  // Problem data
```

### Backend State

```python
# Per-connection state
history = []         # Conversation history
coding_phase = False # Coding phase flag
selected_role = "general" # Interview role
```

## 📊 Performance Considerations

### Audio Processing

- **VAD (Voice Activity Detection)**: Reduces unnecessary transcriptions
- **Silence Timeout**: 1200ms before stopping recording
- **Minimum Speech**: 500ms to filter out noise
- **Threshold**: Volume level 30 for speech detection

### AI Response Optimization

- **Streaming**: Audio chunks streamed as generated
- **Caching**: Question bank loaded once at startup
- **Async Processing**: Non-blocking I/O operations

### Code Execution

- **External API**: Offloads execution to Piston
- **Timeout Protection**: Prevents infinite loops
- **Parallel Testing**: Could be optimized for concurrent test execution

## 🔄 Deployment Architecture

### Development

```
Local Machine
├── Python Backend (localhost:8000)
├── Frontend (served by FastAPI)
└── SQLite/JSON (local storage)
```

### Production (Recommended)

```
Cloud Platform
├── Backend (Container/VM)
├── Frontend (CDN/Static Hosting)
├── Database (Cloud SQL/MongoDB)
└── Load Balancer
```

## Next Steps

- [Installation Guide](INSTALLATION.md)
- [Configuration Guide](CONFIGURATION.md)
- [MCP Tools Documentation](MCP_TOOLS.md)
- [Troubleshooting](TROUBLESHOOTING.md)
