# src/embeddings/embedding_manager.py
"""Embedding generation"""
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from ..config.settings import settings


class EmbeddingManager:
    """Manages embedding generation"""
    
    def __init__(self, model_name: str = None, device: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.device = device or settings.EMBEDDING_DEVICE
        
        print(f"Loading embeddings: {self.model_name}...")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={'device': self.device}
        )
        
        print("✓ Embeddings loaded")
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        return self.embeddings.embed_documents(texts)
    
    def get_model(self):
        """Get the embeddings model"""
        return self.embeddings