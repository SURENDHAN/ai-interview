# SURA AI Interview Practice

An AI-powered interview practice platform with voice interaction, coding challenges, and personalized feedback.

## 🚀 Features

- **Voice-Based Interviews**: Natural conversation with AI interviewer using speech recognition and text-to-speech
- **Multiple Interview Roles**: Software Engineer, Product Manager, Sales, Retail, and General
- **Resume Analysis**: Upload your resume for personalized, role-specific questions
- **Coding Challenges**: HackerRank-style code editor with Python execution
- **Real-time Feedback**: Detailed performance analysis with scores and improvement suggestions
- **Google Authentication**: Secure login with Firebase

## � Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Setup instructions and prerequisites
- **[Configuration Guide](docs/CONFIGURATION.md)** - Environment variables and API keys
- **[MCP Tools](docs/MCP_TOOLS.md)** - Model Context Protocol tools documentation
- **[Architecture](docs/ARCHITECTURE.md)** - Project structure and code flow
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🎯 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the server**:
   ```bash
   python -m uvicorn main3:app --reload --port 8000
   ```

4. **Open browser**: http://localhost:8000/login.html

## 🔒 Security

- **NEVER commit `.env` file** - Contains sensitive API keys
- Firebase config served via backend API, not hardcoded
- All credentials loaded from environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request



## 📧 Support

For issues and questions, please open an issue on GitHub.
