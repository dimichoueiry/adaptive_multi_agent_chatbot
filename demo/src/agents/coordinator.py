"""
Implementation of the multi-agent coordinator for routing queries to appropriate agents.
"""

from typing import Dict, List, Any, Optional
import re

from ..agents import GeneralAgent, ConcordiaCSAgent, AIAgent
from ..config import AGENTS
from ..utils.conversation import ConversationManager
from ..knowledge import KnowledgeEnhancer

class MultiAgentCoordinator:
    """
    Coordinates multiple agents and routes queries to the appropriate agent.
    """
    
    def __init__(self):
        """Initialize the multi-agent coordinator."""
        # Initialize conversation manager
        self.conversation_manager = ConversationManager()
        
        # Initialize knowledge enhancer
        self.knowledge_enhancer = KnowledgeEnhancer()
        
        # Initialize agents
        self.agents = {
            "general": GeneralAgent(
                name=AGENTS["general"]["name"],
                description=AGENTS["general"]["description"],
                model=AGENTS["general"]["model"]
            ),
            "concordia_cs": ConcordiaCSAgent(
                name=AGENTS["concordia_cs"]["name"],
                description=AGENTS["concordia_cs"]["description"],
                model=AGENTS["concordia_cs"]["model"]
            ),
            "ai": AIAgent(
                name=AGENTS["ai"]["name"],
                description=AGENTS["ai"]["description"],
                model=AGENTS["ai"]["model"]
            )
        }
    
    async def route_query(self, query: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Route a query to the appropriate agent.
        
        Args:
            query: The user's query
            conversation_id: Optional conversation ID for context
            
        Returns:
            Dictionary containing the response and metadata
        """
        # Create a new conversation if needed
        if conversation_id is None or conversation_id not in self.conversation_manager.conversations:
            conversation_id = self.conversation_manager.create_conversation(conversation_id)
        
        # Add user message to conversation history
        self.conversation_manager.add_message(conversation_id, "user", query)
        
        # Determine which agent should handle the query
        agent_type = self._determine_agent_type(query, conversation_id)
        
        # Get the appropriate agent
        agent = self.agents[agent_type]
        
        # Get conversation history
        history = self._format_history_for_agent(conversation_id)
        
        # Enhance the query with external knowledge
        knowledge = await self.knowledge_enhancer.enhance_query(query)
        
        # Format the knowledge for inclusion in the prompt
        knowledge_text = self.knowledge_enhancer.format_knowledge_for_prompt(knowledge)
        
        # Augment the query with the knowledge
        augmented_query = query
        if knowledge_text:
            augmented_query = f"{query}\n\n[EXTERNAL KNOWLEDGE: {knowledge_text}]"
        
        # Process the query with the selected agent
        response = await agent.process_query(augmented_query, history)
        
        # Add agent response to conversation history
        self.conversation_manager.add_message(conversation_id, "assistant", response)
        
        # Return the response with metadata
        return {
            "response": response,
            "agent_type": agent_type,
            "conversation_id": conversation_id
        }
    
    def _determine_agent_type(self, query: str, conversation_id: str) -> str:
        """
        Determine which agent should handle the query.
        
        Args:
            query: The user's query
            conversation_id: Conversation ID for context
            
        Returns:
            Agent type (general, concordia_cs, or ai)
        """
        # Convert query to lowercase for easier matching
        query_lower = query.lower()
        
        # Check for Concordia CS admissions related keywords
        concordia_keywords = [
            "concordia", "university", "admission", "computer science", "cs program",
            "application", "requirements", "gpa", "deadline", "tuition", "courses",
            "prerequisites", "department", "faculty", "undergraduate", "graduate"
        ]
        
        # Check for AI related keywords
        ai_keywords = [
            "artificial intelligence", "machine learning", "deep learning", "neural network",
            "nlp", "natural language processing", "computer vision", "reinforcement learning",
            "ai model", "transformer", "gpt", "llm", "large language model", "bert", "training",
            "dataset", "supervised", "unsupervised", "algorithm"
        ]
        
        # Count matches for each category
        concordia_matches = sum(1 for keyword in concordia_keywords if keyword in query_lower)
        ai_matches = sum(1 for keyword in ai_keywords if keyword in query_lower)
        
        # Determine agent type based on keyword matches
        if concordia_matches > ai_matches and concordia_matches > 0:
            return "concordia_cs"
        elif ai_matches > concordia_matches and ai_matches > 0:
            return "ai"
        else:
            # Check conversation history for context
            history = self.conversation_manager.get_history(conversation_id)
            if history:
                # Look at the last few messages to determine context
                recent_messages = history[-4:] if len(history) >= 4 else history
                recent_text = " ".join([msg["content"].lower() for msg in recent_messages])
                
                concordia_context_matches = sum(1 for keyword in concordia_keywords if keyword in recent_text)
                ai_context_matches = sum(1 for keyword in ai_keywords if keyword in recent_text)
                
                if concordia_context_matches > ai_context_matches and concordia_context_matches > 0:
                    return "concordia_cs"
                elif ai_context_matches > concordia_context_matches and ai_context_matches > 0:
                    return "ai"
            
            # Default to general agent if no clear category is detected
            return "general"
    
    def _format_history_for_agent(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Format conversation history for agent consumption.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Formatted history for agent
        """
        history = self.conversation_manager.get_history(conversation_id)
        formatted_history = []
        
        # Convert from role-based format to user/agent format
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                formatted_history.append({
                    "user": history[i]["content"],
                    "agent": history[i + 1]["content"]
                })
        
        return formatted_history
