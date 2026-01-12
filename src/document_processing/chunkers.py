"""Text chunking"""
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from ..config.settings import settings


class TextChunker:
    """Text chunking manager"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        print(f"TextChunker ready (size={self.chunk_size}, overlap={self.chunk_overlap})")
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunk documents into smaller pieces"""
        print(f"Chunking {len(documents)} documents...")
        chunks = self.splitter.split_documents(documents)
        print(f"✓ Created {len(chunks)} chunks")
        return chunks
    
    def chunk_text(self, text: str, metadata: dict = None) -> List[Document]:
        """Chunk raw text"""
        doc = Document(page_content=text, metadata=metadata or {})
        chunks = self.splitter.split_documents([doc])
        print(f"✓ Created {len(chunks)} chunks")
        return chunks