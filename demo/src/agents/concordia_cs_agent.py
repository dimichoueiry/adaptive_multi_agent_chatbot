"""
Concordia CS Admissions agent implementation.
"""

from typing import List, Dict, Any, Optional
import aiohttp
import json
from ..config import OLLAMA_BASE_URL
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
        self.knowledge_enhancer = KnowledgeEnhancer()
    
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process queries related to Concordia University CS admissions using Ollama.
        
        Args:
            query: The user's query text
            conversation_history: Optional conversation history for context
            
        Returns:
            The agent's response to the query
        """
        # Use conversation history if provided, otherwise use the agent's history
        history = conversation_history if conversation_history is not None else self.get_history()
        
        # Format conversation history for the prompt
        formatted_history = ""
        if history:
            for turn in history:
                formatted_history += f"User: {turn['user']}\nAssistant: {turn['agent']}\n\n"
        
        # Enhance the query with relevant knowledge
        enhanced_knowledge = await self.knowledge_enhancer.enhance_query(query, top_k=3)
        
        # Create the prompt with context and enhanced knowledge
        knowledge_context = "\nRelevant Information:\n"
        if enhanced_knowledge.get("vector_store"):
            knowledge_context += "\nFrom University Admissions Database:\n"
            for item in enhanced_knowledge["vector_store"]:
                knowledge_context += f"- {item['text']}\n"
        
        if enhanced_knowledge.get("wikipedia"):
            knowledge_context += "\nFrom Wikipedia:\n"
            for item in enhanced_knowledge["wikipedia"]:
                knowledge_context += f"- {item}\n"
        
        prompt = f"{formatted_history}{knowledge_context}\nUser: {query}\nAssistant:"
        
        # Call Ollama API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": f"You are a specialized assistant named {self.name}. {self.description}. Provide accurate and helpful information about Concordia University's Computer Science program admissions, requirements, application process, deadlines, and related topics. Base your responses on the provided relevant information. If you don't know the answer, suggest contacting the university directly.",
                    "stream": False,
                    "options": {
                        "num_gpu": 0,  # Force CPU usage
                        "num_thread": 4  # Use 4 CPU threads
                    }
                }
            ) as response:
                if response.status == 200:
                    # Read the response as text first
                    response_text = await response.text()
                    # Parse the last line as JSON (Ollama sends the final response in the last line)
                    try:
                        last_line = [line for line in response_text.strip().split('\n') if line.strip()][-1]
                        result = json.loads(last_line)
                        response_text = result.get("response", "")
                    except (json.JSONDecodeError, IndexError, KeyError) as e:
                        return f"Error parsing response: {str(e)}"
                    
                    # Add to conversation history
                    self.add_to_history(query, response_text)
                    
                    return response_text
                else:
                    error_text = await response.text()
                    return f"Error processing query: {error_text}"
