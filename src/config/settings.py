
"""Configuration settings"""
import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings"""
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    DOCUMENTS_DIR: Path = DATA_DIR / "documents"
    VECTORSTORE_DIR: Path = DATA_DIR / "vectorstore"
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    #OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Embedding settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"
    
    # Chunking settings
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    
    # Retrieval settings
    DEFAULT_TOP_K: int = 3
    
    # LLM settings
    LLM_MODEL: str = "gemini-2.5-flash"  # gemini-2.5-flash
    LLM_TEMPERATURE: float = 0.1
    
    def __post_init__(self):
        """Create directories"""
        self.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
        self.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)


# Global settings
settings = Settings()