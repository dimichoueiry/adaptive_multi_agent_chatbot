"""
Concordia CS Admissions agent implementation using LangChain.
"""

from typing import List, Dict, Any, Optional
from .base_agent import BaseAgent
from ..knowledge.enhancer import KnowledgeEnhancer

class ConcordiaCSAgent(BaseAgent):
    """
    Agent that specializes in Concordia University Computer Science program admissions.
    """
    
    def __init__(self, name: str, description: str, model: str = "mistral"):
        """
        Initialize the Concordia CS Agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent's role
            model: Name of the model to use (default: mistral)
        """
        super().__init__(name, description, model)
        
        # Initialize knowledge enhancer with only vector store
        self.knowledge_enhancer = KnowledgeEnhancer(use_wikipedia=False, use_vector_store=True)
    
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process queries related to Concordia University CS admissions using LangChain.
        
        Args:
            query: The user's query text
            conversation_history: Optional conversation history for context
            
        Returns:
            The agent's response to the query
        """
        # Enhance the query with relevant knowledge from vector store
        enhanced_knowledge = await self.knowledge_enhancer.enhance_query(query, top_k=3)
        
        # Format knowledge for the prompt using the enhancer's formatter
        knowledge_context = self.knowledge_enhancer.format_knowledge_for_prompt(enhanced_knowledge)
        
        # Process the query using LangChain
        response_dict = await self.invoke(
            query=query,
            name=self.name,
            description=self.description,
            knowledge=knowledge_context,
            conversation_history=conversation_history
        )
        
        response_content = response_dict["response"]
        
        # Add to conversation history using the string response
        await self.add_to_history(query, response_content)
        
        return response_content
