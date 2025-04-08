"""
Initialization file for the config module.
"""

from .config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    VECTOR_DB_TYPE,
    VECTOR_DB_PATH,
    API_HOST,
    API_PORT,
    AGENTS,
    KNOWLEDGE_SOURCES,
    MAX_HISTORY_LENGTH
)

__all__ = [
    'OLLAMA_BASE_URL',
    'OLLAMA_MODEL',
    'VECTOR_DB_TYPE',
    'VECTOR_DB_PATH',
    'API_HOST',
    'API_PORT',
    'AGENTS',
    'KNOWLEDGE_SOURCES',
    'MAX_HISTORY_LENGTH'
]
