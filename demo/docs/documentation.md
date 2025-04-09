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

The Adaptive Multi-Agent Chatbot System is an intelligent conversational system that leverages Ollama for natural language processing across multiple domains. The system features a multi-agent architecture where different specialized agents handle queries in their respective domains.

The project is organized with a clean, modular structure:
```
demo/
├── docs/          # Project documentation
├── src/           # Source code
│   ├── agents/    # Agent implementations
│   ├── api/       # FastAPI endpoints
│   ├── config/    # Configuration management
│   ├── data/      # Data storage and management
│   ├── knowledge/ # Knowledge base integration
│   └── utils/     # Utility functions
├── main.py        # Application entry point
└── todo.md        # Development tasks
```

## 2. System Architecture

The system is built with a modular architecture consisting of the following components:

### 2.1 Multi-Agent System

The system is organized into specialized modules:
- **Agents Module**: Contains implementations of different specialized agents (Concordia CS Agent, AI Agent, General Questions Agent)
- **API Module**: FastAPI-based REST endpoints
- **Config Module**: Environment and system configuration management
- **Knowledge Module**: Integration with external knowledge sources
- **Utils Module**: Shared utility functions and helpers

The multi-agent system features:
- **Efficient Routing**: Keyword-based agent selection through MultiAgentCoordinator
- **Context Awareness**: Maintains conversation context for better agent selection
- **Specialized Processing**: Each agent type has specific knowledge source configurations:
  - General Agent: Wikipedia integration
  - AI Agent: Combined Wikipedia and vector store
  - Concordia CS Agent: Vector store only
- **Conversation Management**: Custom implementation using MessageStore and ConversationManager

### 2.2 Knowledge Enhancement

The system integrates with external knowledge sources through the knowledge module, with implementations for:
- **Wikipedia Integration**: Retrieves relevant information using Langchain's Wikipedia tools
- **Vector Store**: Document embeddings and retrieval (using FAISS)
- **Conversation Management**: Custom implementation for handling multi-turn conversations:
  - MessageStore: Maintains conversation state using Langchain's BaseMessage objects
  - ConversationManager: Handles multiple conversation sessions
  - History Management: Configurable history length with automatic trimming
  - Knowledge Integration: Seamless combination of conversation context and external knowledge

The conversation system maintains context while keeping memory usage efficient through:
- Configurable MAX_HISTORY_LENGTH setting
- Session-based conversation tracking
- Integration with the knowledge enhancement pipeline
- Clean separation between conversation state and knowledge retrieval

### 2.3 API Layer

The system exposes its functionality through FastAPI:
- **REST Endpoints**: API for chat interactions
- **Async Support**: Built with async/await for better performance
- **OpenAPI Documentation**: Auto-generated API documentation

## 3. Installation and Setup

### 3.1 Prerequisites

- Python 3.10 or higher
- Ollama installed and running locally
- Virtual environment (recommended)

### 3.2 Installation Steps

1. Clone the repository and set up environment:
   ```bash
   git clone <repository-url>
   cd adaptive-multi-agent-chatbot
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   Create a `.env` file with:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   API_HOST=localhost
   API_PORT=8080
   ```

### 3.3 Running the System

Start the server:
```bash
python demo/main.py
```

The API will be available at `http://localhost:8080`

## 4. Usage Guide

### 4.1 Starting the Server

The system uses uvicorn as the ASGI server:
```bash
python demo/main.py
```

### 4.2 API Endpoints

The API endpoints are implemented in the `src/api` module. Documentation is available at:
- OpenAPI UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## 5. API Reference

Detailed API documentation is available through the OpenAPI interface when the server is running.

## 6. Implementation Details

### 6.1 Project Structure

The project follows a modular architecture:
- `src/agents/`: Agent implementations
- `src/api/`: FastAPI endpoint definitions
- `src/config/`: Configuration management
- `src/data/`: Data storage and management
- `src/knowledge/`: Knowledge base integration
- `src/utils/`: Utility functions

### 6.2 Dependencies

Key dependencies include:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `ollama`: LLM integration
- `langchain`: LLM framework and Wikipedia integration
- `faiss-cpu`: Vector storage
- `python-dotenv`: Environment management

### 6.3 Implementation Challenges

The development of this system presented several key challenges:

1. **Local LLM Integration**
   - Basic Ollama integration through environment variables
   - CPU-only execution with standard settings
   - Performance dependent on local hardware capabilities

2. **Agent System Implementation**
   - Keyword-based routing through MultiAgentCoordinator
   - Domain-specific knowledge configurations per agent
   - Basic conversation state management
   - Current limitations in NLP capabilities

3. **Knowledge Integration**
   - Wikipedia integration via Langchain
   - FAISS vector store implementation
   - Basic knowledge enhancement without caching
   - Limited knowledge source types

4. **System Architecture**
   - Basic async implementation with FastAPI
   - In-memory conversation storage
   - Simple configuration management
   - Limited error handling and logging

5. **Development Gaps**
   - No testing infrastructure
   - Basic error handling
   - Limited documentation
   - No monitoring systems

These challenges represent our current implementation state and areas for future improvement.

## 7. Future Improvements

Planned enhancements:
- Implement more specialized agents
- Add authentication and rate limiting
- Enhance knowledge base integration
- Add monitoring and logging
- Implement caching for improved performance
- Add unit and integration tests

** NB: THIS CODEBASE HAS AI WRITTEN CODE **
