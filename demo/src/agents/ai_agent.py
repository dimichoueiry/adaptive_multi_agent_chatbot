"""
AI Knowledge agent implementation using LangChain.
"""

from typing import List, Dict, Any, Optional
from .base_agent import BaseAgent
from ..knowledge.enhancer import KnowledgeEnhancer

class AIAgent(BaseAgent):
    """
    Agent that specializes in artificial intelligence related questions.
    """
    
    def __init__(self, name: str, description: str, model: str = "mistral"):
        """
        Initialize the AI Agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent's role
            model: Name of the model to use (default: mistral)
        """
        super().__init__(name, description, model)
        
        # Initialize knowledge enhancer
        self.knowledge_enhancer = KnowledgeEnhancer()
    
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process queries related to artificial intelligence using LangChain.
        
        Args:
            query: The user's query text
            conversation_history: Optional conversation history for context
            
        Returns:
            The agent's response to the query
        """
        # Enhance the query with relevant knowledge
        enhanced_knowledge = await self.knowledge_enhancer.enhance_query(query, top_k=3)
        
        # Format knowledge for the prompt
        knowledge_context = ""
        if enhanced_knowledge.get("wikipedia"):
            knowledge_context += "\nRelevant Information from Wikipedia:\n"
            for item in enhanced_knowledge["wikipedia"]:
                knowledge_context += f"- {item}\n"
        
        # Process the query using LangChain
        response = await self.conversation.arun(
            input=query,
            name=self.name,
            description=self.description,
            knowledge=knowledge_context
        )
        
        # Add to conversation history
        self.add_to_history(query, response)
        
        return response
