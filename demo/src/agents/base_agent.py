"""
Base agent class for the multi-agent chatbot system.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    """
    
    def __init__(self, name: str, description: str, model: str):
        """
        Initialize the base agent.
        
        Args:
            name: The name of the agent
            description: A description of the agent's capabilities
            model: The Ollama model to use for this agent
        """
        self.name = name
        self.description = description
        self.model = model
        self.conversation_history = []
    
    @abstractmethod
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process a user query and return a response.
        
        Args:
            query: The user's query text
            conversation_history: Optional conversation history for context
            
        Returns:
            The agent's response to the query
        """
        pass
    
    def add_to_history(self, user_query: str, agent_response: str) -> None:
        """
        Add a conversation turn to the history.
        
        Args:
            user_query: The user's query
            agent_response: The agent's response
        """
        self.conversation_history.append({
            "user": user_query,
            "agent": agent_response
        })
    
    def get_history(self, max_length: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Args:
            max_length: Optional maximum number of conversation turns to return
            
        Returns:
            List of conversation turns
        """
        if max_length is not None:
            return self.conversation_history[-max_length:]
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
