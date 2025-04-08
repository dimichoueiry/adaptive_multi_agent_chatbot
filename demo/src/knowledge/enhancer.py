"""
Integration of external knowledge sources with agents.
"""

from typing import List, Dict, Any, Optional
import asyncio

from ..knowledge import WikipediaSource, VectorStore
from ..config import KNOWLEDGE_SOURCES

class KnowledgeEnhancer:
    """
    Enhances agent responses with external knowledge.
    """
    
    def __init__(self, use_wikipedia: bool = False, use_vector_store: bool = True):
        """
        Initialize the knowledge enhancer.
        
        Args:
            use_wikipedia: Whether to use Wikipedia as a knowledge source
            use_vector_store: Whether to use vector store as a knowledge source
        """
        # Initialize knowledge sources
        self.sources = {}
        
        if use_wikipedia and KNOWLEDGE_SOURCES.get("wikipedia", {}).get("enabled", False):
            self.sources["wikipedia"] = WikipediaSource()
        
        # Initialize vector store if needed
        if use_vector_store:
            self.vector_store = VectorStore(collection_name="external_knowledge")
        else:
            self.vector_store = None
    
    async def enhance_query(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Enhance a query with external knowledge.
        
        Args:
            query: The user's query
            top_k: Number of most similar results to return
            
        Returns:
            Dictionary containing retrieved knowledge
        """
        results = {}
        
        # Search vector store if enabled
        if self.vector_store:
            vector_results = await self.vector_store.similarity_search(query, k=top_k)
            if vector_results:
                results["vector_store"] = vector_results
        
        # Search Wikipedia if enabled
        if "wikipedia" in self.sources:
            wiki_source = self.sources["wikipedia"]
            
            # Search for relevant Wikipedia pages
            wiki_titles = await wiki_source.search(query)
            
            if wiki_titles:
                # Get summaries for the top results
                summaries = []
                for title in wiki_titles[:2]:  # Limit to top 2 results
                    summary = await wiki_source.get_summary(title)
                    if not summary.startswith("Error") and not summary.startswith("No Wikipedia"):
                        summaries.append({
                            "title": title,
                            "summary": summary
                        })
                
                if summaries:
                    results["wikipedia"] = summaries
        
        return results
    
    def format_knowledge_for_prompt(self, knowledge: Dict[str, Any]) -> str:
        """
        Format retrieved knowledge for inclusion in a prompt.
        
        Args:
            knowledge: Dictionary of retrieved knowledge
            
        Returns:
            Formatted knowledge string
        """
        formatted = ""
        
        # Format vector store knowledge
        if "vector_store" in knowledge and knowledge["vector_store"]:
            formatted += "\n\nRelevant information from knowledge base:\n"
            for item in knowledge["vector_store"]:
                formatted += f"\n{item['text']}\n"
                if item.get('metadata'):
                    formatted += f"Additional context: {item['metadata']}\n"
        
        # Format Wikipedia knowledge
        if "wikipedia" in knowledge and knowledge["wikipedia"]:
            formatted += "\n\nRelevant information from Wikipedia:\n"
            for item in knowledge["wikipedia"]:
                formatted += f"\n{item['title']}:\n{item['summary']}\n"
        
        return formatted
