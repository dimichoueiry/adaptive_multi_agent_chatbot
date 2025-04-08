"""
API router for the chatbot endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio

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
