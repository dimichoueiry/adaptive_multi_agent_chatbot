"""
Documentation for the Adaptive Multi-Agent Chatbot System.

This file contains comprehensive documentation for the project, including:
1. Project Overview
2. System Architecture
3. Installation and Setup
4. Usage Guide
5. API Reference
6. Implementation Details
7. Future Improvements
"""

# Adaptive Multi-Agent Chatbot System using Ollama

## 1. Project Overview

The Adaptive Multi-Agent Chatbot System is an intelligent conversational system that leverages Ollama for natural language processing across multiple domains. The system features a multi-agent architecture where different specialized agents handle queries in their respective domains:

- **General Questions Agent**: Handles general knowledge questions on various topics
- **Concordia CS Admissions Agent**: Specializes in Concordia University Computer Science program admissions
- **AI Knowledge Agent**: Specializes in artificial intelligence related questions

The system dynamically routes user queries to the appropriate agent based on content analysis and conversation context. It also enhances responses with external knowledge from Wikipedia and maintains conversation history for context-aware interactions.

## 2. System Architecture

The system is built with a modular architecture consisting of the following components:

### 2.1 Multi-Agent Coordinator

The coordinator is the central component that:
- Analyzes incoming queries to determine the most appropriate agent
- Routes queries to specialized agents
- Enhances queries with external knowledge
- Maintains conversation context

### 2.2 Specialized Agents

Three specialized agents handle different types of queries:
- **General Agent**: Handles general knowledge questions
- **Concordia CS Agent**: Specializes in Concordia University CS program admissions
- **AI Agent**: Specializes in artificial intelligence topics

### 2.3 Knowledge Enhancement

The system integrates external knowledge sources:
- **Wikipedia Integration**: Retrieves relevant information from Wikipedia
- **Vector Store**: Stores and retrieves document embeddings (placeholder implementation)

### 2.4 Context Management

The system maintains conversation context through:
- **Conversation Manager**: Tracks conversation history
- **Context-Aware Responses**: Uses conversation history to provide coherent multi-turn conversations

### 2.5 API Layer

The system exposes its functionality through:
- **FastAPI Endpoints**: RESTful API for chat interactions
- **Request/Response Models**: Structured data models for API interactions

## 3. Installation and Setup

### 3.1 Prerequisites

- Python 3.10 or higher
- Ollama installed and running locally (or accessible via network)
- Internet connection for Wikipedia API access

### 3.2 Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/your-username/adaptive-multi-agent-chatbot.git
   cd adaptive-multi-agent-chatbot
   ```

2. Install required packages:
   ```
   pip install langchain ollama fastapi uvicorn faiss-cpu chromadb pydantic python-dotenv requests wikipedia
   ```

3. Configure environment variables (optional):
   Create a `.env` file in the project root with the following variables:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

### 3.3 Running Ollama

Ensure Ollama is running with the required models:
```
ollama run llama3
```

## 4. Usage Guide

### 4.1 Starting the Server

Run the following command from the project root:
```
python main.py
```

This will start the FastAPI server on the configured host and port (default: http://0.0.0.0:8000).

### 4.2 API Endpoints

#### Chat Endpoint

Send a POST request to `/api/chat` with the following JSON body:
```json
{
  "message": "Your question here",
  "conversation_id": "optional-conversation-id"
}
```

Response:
```json
{
  "response": "Agent's response",
  "agent_type": "general|concordia_cs|ai",
  "conversation_id": "conversation-id"
}
```

#### List Agents Endpoint

Send a GET request to `/api/agents` to get information about available agents.

### 4.3 Example Usage

Using curl:
```
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is artificial intelligence?"}'
```

Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "What is artificial intelligence?"}
)
print(response.json())
```

## 5. API Reference

### 5.1 Chat Endpoint

**URL**: `/api/chat`
**Method**: POST
**Request Body**:
- `message` (string, required): The user's query
- `agent_type` (string, optional): Override for agent selection
- `conversation_id` (string, optional): ID for continuing a conversation

**Response**:
- `response` (string): The agent's response
- `agent_type` (string): The type of agent that handled the query
- `conversation_id` (string): ID for the conversation

### 5.2 Agents Endpoint

**URL**: `/api/agents`
**Method**: GET
**Response**: Dictionary of agent types with their names and descriptions

## 6. Implementation Details

### 6.1 Agent Selection Logic

The system selects the appropriate agent based on:
1. Keyword matching in the current query
2. Context from previous conversation turns
3. Default to general agent when no clear category is detected

### 6.2 Knowledge Enhancement

When processing a query:
1. The system searches Wikipedia for relevant information
2. Retrieved information is formatted and added to the query
3. The enhanced query is sent to the appropriate agent

### 6.3 Conversation Management

The system maintains conversation history by:
1. Storing user and agent messages in a conversation store
2. Using conversation IDs to track separate conversations
3. Limiting history length to maintain performance

## 7. Future Improvements

Potential enhancements for the system:
- Implement full vector database functionality for better knowledge retrieval
- Add more external knowledge sources beyond Wikipedia
- Implement reinforcement learning for improving responses over time
- Add user authentication and personalization
- Develop a web-based user interface
- Implement more sophisticated agent selection logic
