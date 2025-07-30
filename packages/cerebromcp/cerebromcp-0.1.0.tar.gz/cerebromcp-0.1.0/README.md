# 🧠 CerebroMCP: Your AI Command Center

> **Intelligent AI Orchestration at Your Fingertips**  
> A powerful system that combines the best of multiple AI technologies to deliver smart, context-aware responses.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## ✨ Why CerebroMCP?

Imagine having a team of AI experts at your disposal, each specialized in different tasks. CerebroMCP is exactly that - an intelligent system that:

- 🤖 **Smartly Routes** your queries to the most appropriate AI system
- 🧠 **Learns & Remembers** your conversation history
- 📚 **Retrieves Information** from your documents when needed
- 👥 **Collaborates** using multiple AI agents for complex tasks
- ⚡ **Responds Instantly** with the most relevant information

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/CerebroMCP.git
cd CerebroMCP

# Set up your environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application

### Method 1: Using VS Code (Recommended)

1. Open the project in VS Code
2. Go to the Run and Debug view (Ctrl+Shift+D or Cmd+Shift+D)
3. Select "Run Full Application" from the dropdown
4. Click the play button or press F5

This will start both the persistent server and main application in debug mode.

### Method 2: Manual Terminal

1. Start the persistent server in one terminal:
```bash
# Activate virtual environment if not already activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the persistent server
python app/servers/persistent_server.py
```

2. In another terminal, start the main application:
```bash
# Activate virtual environment if not already activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the main application
python app/main.py
```

### Method 3: Using Scripts

You can also use the provided scripts to start the application:

```bash
# Start both server and main application
./scripts/start.sh  # On Windows: scripts\start.bat
```

## 🎯 How It Works

CerebroMCP uses intelligent routing to direct your queries to the most appropriate AI system:

| Query Type | AI System | Best For |
|------------|-----------|----------|
| Short questions (< 5 words) | Internal LLM | Quick, simple responses |
| "Explain..." questions | OpenAI | Detailed explanations |
| Document/Design queries | RAG system | Information retrieval |
| Analysis/Research | CrewAI | Complex problem-solving |
| Everything else | LLaMA | General queries |

## 📁 Project Structure

```
├── app/
│   ├── main.py              # 🎮 Main application
│   ├── clients/             # 🤝 AI client implementations
│   ├── servers/            # 🖥️  MCP server implementations
│   ├── host_managed/       # 🏠 Internal LLM implementations
│   └── memory/            # 💾 Conversation memory
├── .env                   # 🔑 Environment variables
├── requirements.txt       # 📦 Dependencies
└── memory.db             # 💿 SQLite database
```

## 🔧 Configuration

1. Create a `.env` file in the root directory
2. Add your API keys and configurations:
```env
OPENAI_API_KEY=your_key_here
LLAMA_API_KEY=your_key_here
# Add other configurations as needed
```

## 🛠️ Dependencies

- `mcp` - Core MCP functionality
- `openai` - OpenAI API integration
- `langgraph` - Graph-based workflow management
- `crewai` - Multi-agent collaboration
- `chromadb` - Vector database for RAG
- And more... (see requirements.txt)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star Us!

If you find CerebroMCP useful, please consider giving us a star on GitHub! It helps others discover the project.

---

Made with ❤️ by Prahlad
