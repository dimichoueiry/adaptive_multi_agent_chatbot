"""
Wikipedia knowledge source implementation using LangChain.
"""

from typing import List, Dict, Any, Optional
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

class WikipediaSource:
    """
    Knowledge source that retrieves information from Wikipedia using LangChain.
    """
    
    def __init__(self):
        """Initialize the Wikipedia knowledge source."""
        self.wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    
    async def search(self, query: str, results_limit: int = 5) -> List[str]:
        """
        Search Wikipedia for relevant pages.
        
        Args:
            query: The search query
            results_limit: Maximum number of search results to return
            
        Returns:
            List of page titles
        """
        try:
            # Use LangChain's Wikipedia tool to search
            results = self.wikipedia.run(query)
            # Extract titles from the results
            titles = []
            for line in results.split('\n'):
                if line.strip().startswith('Title:'):
                    titles.append(line.replace('Title:', '').strip())
                if len(titles) >= results_limit:
                    break
            return titles
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []
    
    async def get_summary(self, title: str, sentences: int = 3) -> str:
        """
        Get a summary of a Wikipedia page.
        
        Args:
            title: The title of the Wikipedia page
            sentences: Number of sentences to include in the summary
            
        Returns:
            Summary text
        """
        try:
            # Use LangChain's Wikipedia tool to get summary
            query = f"Give me a {sentences} sentence summary of the Wikipedia article '{title}'"
            return self.wikipedia.run(query)
        except Exception as e:
            return f"Error retrieving Wikipedia summary: {e}"
    
    async def get_content(self, title: str) -> str:
        """
        Get the full content of a Wikipedia page.
        
        Args:
            title: The title of the Wikipedia page
            
        Returns:
            Full page content
        """
        try:
            # Use LangChain's Wikipedia tool to get full content
            query = f"Give me the full content of the Wikipedia article '{title}'"
            return self.wikipedia.run(query)
        except Exception as e:
            return f"Error retrieving Wikipedia content: {e}"
