
"""Document retrieval"""
from typing import List, Tuple
from langchain_core.documents import Document
from ..vectorstore.vector_manager import VectorStoreManager


class Retriever:
    """Handles document retrieval"""
    
    def __init__(self, vector_manager: VectorStoreManager):
        self.vector_manager = vector_manager
    
    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """Retrieve relevant documents"""
        print(f"Retrieving {k} documents for query...")
        docs = self.vector_manager.similarity_search(query, k=k)
        print(f"✓ Retrieved {len(docs)} documents")
        return docs
    
    def retrieve_with_scores(self, query: str, k: int = 3) -> List[Tuple[Document, float]]:
        """Retrieve with similarity scores"""
        print(f"Retrieving {k} documents with scores...")
        results = self.vector_manager.similarity_search_with_score(query, k=k)
        print(f"✓ Retrieved {len(results)} documents")
        return results