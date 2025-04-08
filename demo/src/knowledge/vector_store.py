"""
Vector store implementation for storing and retrieving embeddings.
"""

import os
import shutil
from typing import List, Dict, Any, Optional, Union
import numpy as np
import uuid
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import based on configured vector DB type
from config import VECTOR_DB_TYPE, VECTOR_DB_PATH

class VectorStore:
    """
    Vector database for storing and retrieving document embeddings.
    """
    
    def __init__(self, collection_name: str = "default"):
        """
        Initialize the vector store.
        
        Args:
            collection_name: Name of the collection to use
        """
        self.collection_name = collection_name
        self.db = None
        self.collection = None
        
        # Create the vector DB directory if it doesn't exist
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        
        # Initialize the appropriate vector database
        if VECTOR_DB_TYPE.lower() == "chroma":
            self._init_chroma()
        elif VECTOR_DB_TYPE.lower() == "faiss":
            self._init_faiss()
        else:
            raise ValueError(f"Unsupported vector database type: {VECTOR_DB_TYPE}")
    
    def _init_chroma(self):
        """Initialize ChromaDB."""
        try:
            import chromadb
            from chromadb.config import Settings
            
            self.db = chromadb.PersistentClient(
                path=os.path.join(VECTOR_DB_PATH, "chroma"),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            try:
                self.collection = self.db.get_collection(self.collection_name)
                print(f"Using existing collection: {self.collection_name}")
            except:
                self.collection = self.db.create_collection(self.collection_name)
                print(f"Created new collection: {self.collection_name}")
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            raise
    
    def _init_faiss(self):
        """Initialize FAISS."""
        try:
            import faiss
            import pickle
            
            self.faiss_dir = os.path.join(VECTOR_DB_PATH, "faiss")
            os.makedirs(self.faiss_dir, exist_ok=True)
            
            self.index_file = os.path.join(self.faiss_dir, f"{self.collection_name}_index.faiss")
            self.metadata_file = os.path.join(self.faiss_dir, f"{self.collection_name}_metadata.pkl")
            
            # Load existing index or create new one
            if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
                print(f"Loaded existing FAISS index: {self.collection_name}")
            else:
                # Create a new index - using L2 distance
                self.index = faiss.IndexFlatL2(1536)  # Default dimension for many embedding models
                self.metadata = {"ids": [], "texts": [], "metadatas": []}
                print(f"Created new FAISS index: {self.collection_name}")
        except Exception as e:
            print(f"Error initializing FAISS: {e}")
            raise
    
    async def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None, ids: Optional[List[str]] = None) -> List[str]:
        """
        Add texts to the vector store.
        
        Args:
            texts: List of text strings to add
            metadatas: Optional list of metadata dictionaries
            ids: Optional list of IDs for the texts
            
        Returns:
            List of IDs for the added texts
        """
        if VECTOR_DB_TYPE.lower() == "chroma":
            # Generate IDs if not provided
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in texts]
            
            # Ensure metadatas is a list of the same length as texts
            if metadatas is None:
                metadatas = [{} for _ in texts]
            
            # Add documents to ChromaDB
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Added {len(texts)} texts to ChromaDB collection: {self.collection_name}")
            return ids
            
        elif VECTOR_DB_TYPE.lower() == "faiss":
            # FAISS implementation would go here
            pass
    
    async def similarity_search(self, query: str, k: int = 4, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar texts in the vector store.
        
        Args:
            query: Query text
            k: Number of results to return
            where: Optional filter conditions for metadata
            
        Returns:
            List of dictionaries containing text and metadata
        """
        if VECTOR_DB_TYPE.lower() == "chroma":
            # Perform similarity search in ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=where
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            return formatted_results
            
        elif VECTOR_DB_TYPE.lower() == "faiss":
            # FAISS implementation would go here
            pass
