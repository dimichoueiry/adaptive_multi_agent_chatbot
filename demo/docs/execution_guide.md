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

## Step 3: Clone or Download the Project

If using Git:
```bash
git clone https://github.com/your-username/adaptive-multi-agent-chatbot.git
cd adaptive-multi-agent-chatbot
```

Or simply extract the provided ZIP file to a directory of your choice.

## Step 4: Install Dependencies

Navigate to the project directory and install the required Python packages:

```bash
pip install langchain ollama fastapi uvicorn faiss-cpu chromadb pydantic python-dotenv requests wikipedia
```

## Step 5: Configure Environment (Optional)

Create a `.env` file in the project root directory with the following content:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
API_HOST=0.0.0.0
API_PORT=8000
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
python main.py
```

You should see output indicating that the server is running, typically on http://0.0.0.0:8000.

## Step 8: Interact with the Chatbot

You can interact with the chatbot using:

### cURL:
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is artificial intelligence?"}'
```

### Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "What is artificial intelligence?"}
)
print(response.json())
```

### Web Browser:
You can access the API documentation by opening http://localhost:8000/docs in your web browser.

## Step 9: Testing Different Agent Types

Try different types of queries to see how the system routes to different agents:

- General knowledge: "What is the capital of France?"
- Concordia CS admissions: "What are the requirements for Concordia's Computer Science program?"
- AI-related: "Explain how neural networks work."

## Troubleshooting

### Issue: Cannot connect to Ollama
- Ensure Ollama is running with `ollama serve`
- Check if the OLLAMA_BASE_URL in your configuration matches the actual Ollama server address

### Issue: Missing dependencies
- Run `pip install -r requirements.txt` if a requirements file is provided
- Install missing packages individually as needed

### Issue: Port already in use
- Change the API_PORT in your .env file or configuration
- Alternatively, stop the process using the conflicting port

## Additional Information

- The system maintains conversation context, so you can ask follow-up questions
- You can specify a conversation_id to continue a previous conversation
- The system automatically enhances responses with information from Wikipedia when relevant
