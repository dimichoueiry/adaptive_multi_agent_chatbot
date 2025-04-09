"""
API router for the chatbot endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Optional

from ..agents import MultiAgentCoordinator
from ..config import AGENTS

router = APIRouter(prefix="/api", tags=["chatbot"])

# Models for request and response
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    agent_type: Optional[str] = None  # Optional agent type override
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    agent_type: str
    conversation_id: str

# Initialize the multi-agent coordinator
coordinator = MultiAgentCoordinator()

@router.get("/", response_class=HTMLResponse)
async def root():
    """Serve the welcome page."""
    return """
    <html>
        <head>
            <title>Adaptive Multi-Agent Chatbot System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                .endpoint {
                    background-color: #f5f5f5;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                }
                code {
                    background-color: #f0f0f0;
                    padding: 2px 5px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Adaptive Multi-Agent Chatbot System</h1>
            <p>This is an intelligent chatbot system that uses multiple specialized agents to handle different types of queries.</p>
            
            <h2>Available Endpoints:</h2>
            
            <div class="endpoint">
                <h3>Chat Endpoint</h3>
                <p><code>POST /api/chat</code></p>
                <p>Send a message to the chatbot and get a response.</p>
                <p>Example request:</p>
                <pre>
{
    "message": "What is artificial intelligence?",
    "conversation_id": "optional-conversation-id"
}
                </pre>
            </div>
            
            <div class="endpoint">
                <h3>List Agents Endpoint</h3>
                <p><code>GET /api/agents</code></p>
                <p>Get information about available agents.</p>
            </div>
            
            <p>For more information, visit the <a href="/docs">API documentation</a>.</p>
        </body>
    </html>
    """

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return a response.
    
    Args:
        request: Chat request containing message and optional agent type
        
    Returns:
        Chat response
    """
    try:
        # If agent_type is specified, we'll use it as a hint for the coordinator
        # Otherwise, the coordinator will determine the best agent automatically
        
        # Process the query through the coordinator
        result = await coordinator.route_query(request.message, request.conversation_id)
        
        return ChatResponse(
            response=result["response"],
            agent_type=result["agent_type"],
            conversation_id=result["conversation_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.get("/agents", response_model=Dict[str, Dict[str, str]])
async def list_agents():
    """
    List available agent types.
    
    Returns:
        Dictionary of agent types and their descriptions
    """
    return {
        agent_type: {
            "name": config["name"],
            "description": config["description"]
        }
        for agent_type, config in AGENTS.items()
    }
