"""
Base agent class for the multi-agent chatbot system using LangChain.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.runnables import RunnableWithMessageHistory
from ..config import OLLAMA_BASE_URL

class MessageStore:
    """A simple message store for conversation history."""
    
    def __init__(self):
        """Initialize the message store."""
        self.messages: Dict[str, List[BaseMessage]] = {}
    
    def get_messages(self, session_id: str) -> List[BaseMessage]:
        """Get messages for a session synchronously."""
        if session_id not in self.messages:
            self.messages[session_id] = []
        # Make sure we return a list of BaseMessage objects
        return self.messages[session_id]
    
    def save_messages(self, session_id: str, messages: List[BaseMessage]) -> None:
        """Save messages for a session synchronously."""
        # Make sure we're storing a list of BaseMessage objects
        self.messages[session_id] = list(messages)

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
        self.llm = OllamaLLM(
            base_url=OLLAMA_BASE_URL,
            model=model,
            temperature=0.7,
            num_thread=8,  # Increased for better CPU performance
            stop=["</s>"],  # Add explicit stop token
            timeout=120,  # Increase timeout
            retry_on_failure=True,  # Enable retries
            context_window=4096,  # Explicit context window
            num_gpu=0  # Force CPU mode to avoid CUDA errors
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
        
        # Create chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a specialized assistant named {name}. {description}"),
            MessagesPlaceholder(variable_name="history"),
            ("system", "Relevant Information:\n{knowledge}"),
            ("human", "{input}")
        ])
        
        # Create the chain
        self.chain = self.prompt | self.llm
        
        # Initialize message store
        self.message_store = MessageStore()
    
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
    
    async def invoke(self, query: str, name: str, description: str, knowledge: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Invoke the conversation chain with the given inputs.
        
        Args:
            query: The user's query
            name: The agent's name
            description: The agent's description
            knowledge: The knowledge context
            conversation_history: Optional conversation history for context
            
        Returns:
            Dictionary containing the response and metadata
        """
        # Convert conversation history to LangChain messages if provided
        history = []
        if conversation_history:
            for turn in conversation_history:
                if "user" in turn:
                    history.append(HumanMessage(content=turn["user"]))
                if "agent" in turn:
                    history.append(AIMessage(content=turn["agent"]))
        
        # Invoke the chain with all parameters including history
        response = await self.chain.ainvoke({
            "input": query,
            "name": name,
            "description": description,
            "knowledge": knowledge,
            "history": history
        })
        
        # Extract the content from the response
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "response": response_content,
            "agent_type": self.name,
            "conversation_id": "default"
        }
    
    async def add_to_history(self, user_query: str, agent_response: str) -> None:
        """
        Add a conversation turn to the history.
        
        Args:
            user_query: The user's query
            agent_response: The agent's response
        """
        # Get existing messages
        existing_messages = self.message_store.get_messages("default")
        
        # Add new messages
        new_messages = existing_messages + [
            HumanMessage(content=user_query),
            AIMessage(content=agent_response)
        ]
        
        # Save updated messages
        self.message_store.save_messages("default", new_messages)
    
    def get_history(self, max_length: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Args:
            max_length: Optional maximum number of conversation turns to return
            
        Returns:
            List of conversation turns
        """
        messages = self.message_store.get_messages("default")
        if max_length is not None:
            messages = messages[-max_length * 2:]  # *2 because each turn has user and agent messages
            
        return [
            {"user": msg.content if isinstance(msg, HumanMessage) else "", 
             "agent": msg.content if isinstance(msg, AIMessage) else ""}
            for msg in messages
        ]
