"""
Concordia CS Admissions agent implementation using LangChain.
"""

from typing import List, Dict, Any, Optional
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
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
            collection_name="concordia_cs",
            embedding_function=self.embeddings
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        
        # Create prompt template
        self.prompt = PromptTemplate(
            input_variables=["history", "input", "knowledge"],
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
        
        # Initialize knowledge enhancer
        self.knowledge_enhancer = KnowledgeEnhancer()
    
    async def process_query(self, query: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Process queries related to Concordia University CS admissions using LangChain.
        
        Args:
            query: The user's query text
            conversation_history: Optional conversation history for context
            
        Returns:
            The agent's response to the query
        """
        # Enhance the query with relevant knowledge
        enhanced_knowledge = await self.knowledge_enhancer.enhance_query(query, top_k=3)
        
        # Format knowledge for the prompt
        knowledge_context = ""
        if enhanced_knowledge.get("vector_store"):
            knowledge_context += "\nFrom University Admissions Database:\n"
            for item in enhanced_knowledge["vector_store"]:
                knowledge_context += f"- {item['text']}\n"
        
        if enhanced_knowledge.get("wikipedia"):
            knowledge_context += "\nFrom Wikipedia:\n"
            for item in enhanced_knowledge["wikipedia"]:
                knowledge_context += f"- {item}\n"
        
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
