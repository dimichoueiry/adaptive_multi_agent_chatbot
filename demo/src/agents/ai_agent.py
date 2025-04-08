"""
AI Knowledge agent implementation.
"""

from typing import List, Dict, Any, Optional
import aiohttp
import json
from ..config import OLLAMA_BASE_URL
from .base_agent import BaseAgent

class AIAgent(BaseAgent):
    """
    Agent that specializes in artificial intelligence related questions.
    """
    
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process queries related to artificial intelligence using Ollama.
        
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
        
        # Create the prompt with context
        prompt = f"{formatted_history}User: {query}\nAssistant:"
        
        # Call Ollama API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": f"You are a specialized assistant named {self.name}. {self.description}. Provide accurate, technical, and helpful information about artificial intelligence concepts, technologies, algorithms, applications, and recent developments. Explain complex AI topics in a clear and educational manner.",
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
