"""
FastAPI application factory for the chatbot API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import router
from ..config import API_HOST, API_PORT

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    # Create FastAPI app
    app = FastAPI(
        title="Adaptive Multi-Agent Chatbot System",
        description="A chatbot system that leverages Ollama for intelligent conversations across multiple domains",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, this should be restricted
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router)
    
    return app
