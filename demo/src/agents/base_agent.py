"""
Base agent class for the multi-agent chatbot system using LangChain.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from ..config import OLLAMA_BASE_URL

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    """
    
    def __init__(self, name: str, description: str, model: str):
        """
        Initialize the base agent.
        
        Args:
            name: The name of the agent
            description: A description of the agent's capabilities
            model: The Ollama model to use for this agent
        """
        self.name = name
        self.description = description
        self.model = model
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            base_url=OLLAMA_BASE_URL,
            model=model,
            temperature=0.7,
            num_thread=4
        )
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(
            base_url=OLLAMA_BASE_URL,
            model=model
        )
        
        # Initialize vector store
        self.vector_store = Chroma(
            collection_name=f"{name.lower().replace(' ', '_')}",
            embedding_function=self.embeddings
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        
        # Create base prompt template
        self.prompt = PromptTemplate(
            input_variables=["history", "input", "knowledge", "name", "description"],
            template="""You are a specialized assistant named {name}. {description}

Previous conversation:
{history}

Relevant Information:
{knowledge}

User: {input}
Assistant:"""
        )
        
        # Initialize conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )
    
    @abstractmethod
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process a user query and return a response.
        
        Args:
            query: The user's query text
            conversation_history: Optional conversation history for context
            
        Returns:
            The agent's response to the query
        """
        pass
    
    def add_to_history(self, user_query: str, agent_response: str) -> None:
        """
        Add a conversation turn to the history.
        
        Args:
            user_query: The user's query
            agent_response: The agent's response
        """
        self.memory.save_context(
            {"input": user_query},
            {"output": agent_response}
        )
    
    def get_history(self, max_length: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Args:
            max_length: Optional maximum number of conversation turns to return
            
        Returns:
            List of conversation turns
        """
        history = self.memory.load_memory_variables({})
        messages = history.get("history", [])
        
        if max_length is not None:
            messages = messages[-max_length:]
            
        return [
            {"user": msg.content if msg.type == "human" else "", 
             "agent": msg.content if msg.type == "ai" else ""}
            for msg in messages
        ]
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.memory.clear()
