# src/vectorstore/vector_manager.py
"""Vector store management"""
from pathlib import Path
from typing import List, Optional, Tuple
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from ..config.settings import settings
from ..embeddings.embedding_manager import EmbeddingManager


class VectorStoreManager:
    """Manages vector store operations"""
    
    def __init__(self, embedding_manager: EmbeddingManager, store_name: str = "default"):
        self.embedding_manager = embedding_manager
        self.store_name = store_name
        self.vectorstore: Optional[FAISS] = None
        self.store_path = settings.VECTORSTORE_DIR / f"{store_name}_faiss"
        
        print(f"VectorStoreManager: {store_name}")
    
    def create_vectorstore(self, documents: List[Document]) -> FAISS:
        """Create new vector store from documents"""
        print(f"Creating vector store with {len(documents)} documents...")
        
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_manager.get_model()
        )
        
        print("✓ Vector store created")
        return self.vectorstore
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to existing vector store"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        print(f"Adding {len(documents)} documents...")
        self.vectorstore.add_documents(documents)
        print("✓ Documents added")
    
    def save(self) -> None:
        """Save vector store to disk"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.vectorstore.save_local(str(self.store_path))
        print(f"✓ Saved to: {self.store_path}")
    
    def load(self) -> FAISS:
        """Load vector store from disk"""
        print(f"Loading from: {self.store_path}")
        
        self.vectorstore = FAISS.load_local(
            str(self.store_path),
            self.embedding_manager.get_model(),
            allow_dangerous_deserialization=True
        )
        
        print("✓ Vector store loaded")
        return self.vectorstore
    
    def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """Search for similar documents"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        k = k or settings.DEFAULT_TOP_K
        return self.vectorstore.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = None) -> List[Tuple[Document, float]]:
        """Search with similarity scores"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        k = k or settings.DEFAULT_TOP_K
        return self.vectorstore.similarity_search_with_score(query, k=k)
    
    def get_count(self) -> int:
        """Get number of documents"""
        if not self.vectorstore:
            return 0
        return self.vectorstore.index.ntotal