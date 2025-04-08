"""
Conversation management utility for tracking multi-turn conversations.
"""

from typing import Dict, List, Any, Optional
import uuid
from ..config import MAX_HISTORY_LENGTH

class ConversationManager:
    """
    Manages conversation history across multiple sessions.
    """
    
    def __init__(self):
        """Initialize the conversation manager."""
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
    
    def create_conversation(self, conversation_id: Optional[str] = None) -> str:
        """
        Create a new conversation.
        
        Args:
            conversation_id: Optional ID for the conversation
            
        Returns:
            Conversation ID
        """
        # Generate a new ID if not provided
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        # Initialize conversation history if not exists
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: ID of the conversation
            role: Role of the message sender (user or assistant)
            content: Message content
        """
        # Create conversation if it doesn't exist
        if conversation_id not in self.conversations:
            self.create_conversation(conversation_id)
        
        # Add message to conversation
        self.conversations[conversation_id].append({
            "role": role,
            "content": content
        })
        
        # Trim history if it exceeds maximum length
        if len(self.conversations[conversation_id]) > MAX_HISTORY_LENGTH * 2:  # *2 because each turn has user and assistant messages
            self.conversations[conversation_id] = self.conversations[conversation_id][-MAX_HISTORY_LENGTH * 2:]
    
    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Get the history of a conversation.
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            List of messages in the conversation
        """
        # Return empty list if conversation doesn't exist
        if conversation_id not in self.conversations:
            return []
        
        return self.conversations[conversation_id]
    
    def clear_history(self, conversation_id: str) -> None:
        """
        Clear the history of a conversation.
        
        Args:
            conversation_id: ID of the conversation
        """
        if conversation_id in self.conversations:
            self.conversations[conversation_id] = []
    
    def delete_conversation(self, conversation_id: str) -> None:
        """
        Delete a conversation.
        
        Args:
            conversation_id: ID of the conversation
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
    
    def get_all_conversations(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Get all conversations.
        
        Returns:
            Dictionary of conversation IDs and their histories
        """
        return self.conversations
