# Execution Guide for Adaptive Multi-Agent Chatbot System

This guide provides step-by-step instructions for setting up and running the Adaptive Multi-Agent Chatbot System.

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.10 or higher
- Ollama (for local LLM inference)
- Git (optional, for cloning the repository)

## Step 1: Install Ollama

If you haven't already installed Ollama, follow these steps:

### For Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### For macOS:
Download and install from: https://ollama.com/download

### For Windows:
Download and install from: https://ollama.com/download

## Step 2: Pull the Required Model

After installing Ollama, pull the required model:

```bash
ollama pull llama3
```

## Step 3: Set Up the Project

### Clone or Download the Project
If using Git:
```bash
git clone <repository-url>
cd adaptive-multi-agent-chatbot
```

Or extract the provided ZIP file to a directory of your choice.

### Create and Activate Virtual Environment
It's recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

## Step 4: Install Dependencies

With the virtual environment activated, install all required dependencies:

```bash
pip install -r requirements.txt
```

## Step 5: Configure Environment

Create a `.env` file in the project root directory with the following content:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
API_HOST=localhost
API_PORT=8080
```

You can modify these values according to your setup if needed.

## Step 6: Start Ollama

Ensure Ollama is running in a separate terminal:

```bash
ollama serve
```

## Step 7: Run the Chatbot API

From the project root directory, run:

```bash
python demo/main.py
```

You should see output indicating that the server is running on http://localhost:8080.

## Step 8: Access the API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Step 9: Test Different Agent Types

The system includes three specialized agents:
- **Concordia CS Agent**: Handles questions about Concordia's Computer Science program
- **AI Agent**: Handles artificial intelligence related queries
- **General Questions Agent**: Handles general knowledge questions

Example queries for each agent:

### Using cURL:
```bash
curl -X POST "http://localhost:8080/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What are the admission requirements for Concordia CS program?"}'
```

### Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8080/api/chat",
    json={"message": "What are the admission requirements for Concordia CS program?"}
)
print(response.json())
```

## Troubleshooting

### Common Issues and Solutions

#### Cannot connect to Ollama
- Verify Ollama is running with `ollama serve`
- Check if the OLLAMA_BASE_URL in your .env file matches the Ollama server address
- Ensure the llama3 model is downloaded using `ollama list`

#### API Connection Issues
- Confirm the API_HOST and API_PORT in .env match your setup
- Check if another process is using port 8080
- Verify you're using the correct URL in your requests

#### Dependencies Issues
- Ensure you're in the virtual environment (you should see (.venv) in your terminal)
- Try removing and recreating the virtual environment if dependencies are corrupted
- Make sure you have the latest pip: `python -m pip install --upgrade pip`

#### Virtual Environment Issues
- If venv creation fails, ensure you have Python 3.10+ installed
- On Windows, you might need to run PowerShell as administrator
- On Linux/macOS, you might need to install python3-venv package

## Project Structure

For reference, the project is organized as follows:
```
demo/
├── docs/          # Documentation files
├── src/           # Source code
│   ├── agents/    # Agent implementations
│   ├── api/       # FastAPI endpoints
│   ├── config/    # Configuration
│   ├── data/      # Data management
│   ├── knowledge/ # Knowledge base
│   └── utils/     # Utilities
├── main.py        # Entry point
└── todo.md        # Development tasks
```

## Additional Information

- The system maintains conversation context, so you can ask follow-up questions
- You can specify a conversation_id to continue a previous conversation
- The system automatically enhances responses with information from Wikipedia when relevant

** NB: A LOT OF THIS CODE WAS WRITTEN AND RESEARCHED WITH THE HELP OF AI **
