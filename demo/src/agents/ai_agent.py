"""
AI and machine learning questions agent implementation using LangChain.
"""

from typing import List, Dict, Any, Optional
from .base_agent import BaseAgent
from ..knowledge.enhancer import KnowledgeEnhancer

class AIAgent(BaseAgent):
    """
    Agent that handles questions about AI, machine learning, and related topics.
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
        
        # Initialize knowledge enhancer with both Wikipedia and vector store
        self.knowledge_enhancer = KnowledgeEnhancer(use_wikipedia=True, use_vector_store=True)
    
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process an AI/ML query using LangChain.
        
        Args:
            query: The user's query text
            conversation_history: Optional conversation history for context
            
        Returns:
            The agent's response to the query
        """
        # Enhance the query with relevant knowledge
        enhanced_knowledge = await self.knowledge_enhancer.enhance_query(query, top_k=3)
        
        # Format knowledge for the prompt using the enhancer's formatter
        knowledge_context = self.knowledge_enhancer.format_knowledge_for_prompt(enhanced_knowledge)
        
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
