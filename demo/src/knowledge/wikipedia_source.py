"""
Wikipedia knowledge source implementation.
"""

import wikipedia
from typing import List, Dict, Any, Optional

class WikipediaSource:
    """
    Knowledge source that retrieves information from Wikipedia.
    """
    
    def __init__(self):
        """Initialize the Wikipedia knowledge source."""
        pass
    
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
            return wikipedia.search(query, results=results_limit)
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
            return wikipedia.summary(title, sentences=sentences)
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation pages by returning the first option
            if e.options:
                try:
                    return wikipedia.summary(e.options[0], sentences=sentences)
                except:
                    return f"Multiple Wikipedia pages found for '{title}'. Options include: {', '.join(e.options[:5])}."
            return f"Disambiguation error for '{title}'."
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{title}'."
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
            page = wikipedia.page(title)
            return page.content
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation pages by returning the first option
            if e.options:
                try:
                    page = wikipedia.page(e.options[0])
                    return page.content
                except:
                    return f"Multiple Wikipedia pages found for '{title}'. Options include: {', '.join(e.options[:5])}."
            return f"Disambiguation error for '{title}'."
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{title}'."
        except Exception as e:
            return f"Error retrieving Wikipedia content: {e}"
