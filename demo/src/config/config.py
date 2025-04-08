"""
Configuration settings for the Adaptive Multi-Agent Chatbot System.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Ollama settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Vector database settings
VECTOR_DB_TYPE = "faiss"  # Options: "chroma", "faiss"
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vector_db")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Agent settings
AGENTS = {
    "general": {
        "name": "General Questions Agent",
        "description": "Handles general knowledge questions on various topics",
        "model": OLLAMA_MODEL,
    },
    "concordia_cs": {
        "name": "Concordia CS Admissions Agent",
        "description": "Specializes in Concordia University Computer Science program admissions",
        "model": OLLAMA_MODEL,
    },
    "ai": {
        "name": "AI Knowledge Agent",
        "description": "Specializes in artificial intelligence related questions",
        "model": OLLAMA_MODEL,
    }
}

# External knowledge sources
KNOWLEDGE_SOURCES = {
    "wikipedia": {
        "enabled": True,
    }
}

# Context settings
MAX_HISTORY_LENGTH = 10  # Maximum number of conversation turns to keep in memory
