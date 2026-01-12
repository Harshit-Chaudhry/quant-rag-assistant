"""Document loaders"""
from pathlib import Path
from typing import List
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_core.documents import Document


class DocumentLoader:
    """Document loading manager"""
    
    @staticmethod
    def load_text_file(filepath: str) -> List[Document]:
        """Load a single text file"""
        print(f"Loading: {filepath}")
        loader = TextLoader(filepath)
        docs = loader.load()
        print(f"✓ Loaded {len(docs)} documents")
        return docs
    
    @staticmethod
    def load_directory(directory: str, glob: str = "**/*.txt") -> List[Document]:
        """Load all files from directory"""
        print(f"Loading from: {directory}")
        loader = DirectoryLoader(directory, glob=glob, loader_cls=TextLoader)
        docs = loader.load()
        print(f"✓ Loaded {len(docs)} documents")
        return docs
    
    @staticmethod
    def save_text_file(text: str, filepath: str) -> None:
        """Save text to file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ Saved: {filepath}")