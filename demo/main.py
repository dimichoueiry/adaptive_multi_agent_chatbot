"""
Main application entry point for the Adaptive Multi-Agent Chatbot System.
"""

import uvicorn
import asyncio
import os
from src.api import create_app
from src.config import API_HOST, API_PORT

def main():
    """Run the FastAPI application."""
    # Create the FastAPI app
    app = create_app()
    
    # Run the app with uvicorn
    print(f"Starting Adaptive Multi-Agent Chatbot System on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)

if __name__ == "__main__":
    main()
