"""Main RAG Pipeline"""
from typing import Dict, List, Optional
from pathlib import Path

from .config.settings import settings
from .data_sources.yahoo_finance import YahooFinanceSource
from .document_processing.loaders import DocumentLoader
from .document_processing.chunkers import TextChunker
from .embeddings.embedding_manager import EmbeddingManager
from .vectorstore.vector_manager import VectorStoreManager
from .retrieval.retriever import Retriever
from .generation.llm_manager import LLMManager
from .generation.answer_generator import AnswerGenerator


class RAGPipeline:
    """Complete RAG Pipeline"""
    
    def __init__(self, store_name: str = "default", api_key: str = None):
        print("\n" + "="*60)
        print("Initializing RAG Pipeline")
        print("="*60)
        
        self.store_name = store_name
        self.api_key = api_key
        
        # Initialize components
        self.data_source = YahooFinanceSource()
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.embedding_manager = EmbeddingManager()
        self.vector_manager = VectorStoreManager(self.embedding_manager, store_name)
        self.retriever = Retriever(self.vector_manager)
        self.llm_manager = LLMManager(api_key=self.api_key)
        self.answer_generator = AnswerGenerator(self.llm_manager)
        
        print("\n✓ RAG Pipeline ready!")
    
    def ingest_stock(self, ticker: str, save_doc: bool = True) -> bool:
        """Ingest stock data"""
        print(f"\n{'='*60}")
        print(f"Ingesting {ticker}")
        print('='*60)
        
        # Fetch data
        data = self.data_source.fetch_company_data(ticker)
        if not data:
            print("✗ Failed to fetch data")
            return False
        
        # Create document
        doc_text = self.data_source.create_document(data)
        
        # Save to file
        if save_doc:
            filepath = settings.DOCUMENTS_DIR / f"{ticker.replace('.', '_')}_report.txt"
            self.loader.save_text_file(doc_text, str(filepath))
        
        # Chunk
        chunks = self.chunker.chunk_text(doc_text, metadata={'source': f"{ticker}_report.txt"})
        
        # Add to vector store
        if self.vector_manager.vectorstore is None:
            self.vector_manager.create_vectorstore(chunks)
        else:
            self.vector_manager.add_documents(chunks)
        
        print(f"✓ {ticker} ingested successfully!")
        return True
    
    def ingest_multiple_stocks(self, tickers: List[str]) -> Dict:
        """Ingest multiple stocks"""
        print(f"\n{'='*60}")
        print(f"Ingesting {len(tickers)} stocks")
        print('='*60)
        
        results = {'success': [], 'failed': []}
        
        for ticker in tickers:
            if self.ingest_stock(ticker):
                results['success'].append(ticker)
            else:
                results['failed'].append(ticker)
        
        print(f"\n✓ Success: {len(results['success'])}, Failed: {len(results['failed'])}")
        return results
    
    def save_vectorstore(self) -> None:
        """Save vector store to disk"""
        self.vector_manager.save()
    
    def load_vectorstore(self) -> bool:
        """Load vector store from disk"""
        try:
            self.vector_manager.load()
            return True
        except Exception as e:
            print(f"✗ Failed to load: {e}")
            return False
    
    def query(self, question: str, k: int = 3) -> Dict:
        """Query the RAG system"""
        print(f"\n{'='*60}")
        print(f"Query: {question}")
        print('='*60)
        
        # Retrieve
        docs = self.retriever.retrieve(question, k=k)
        
        if not docs:
            return {
                'question': question,
                'answer': 'No relevant information found',
                'sources': [],
                'confidence': 0.0
            }
        
        # Generate answer
        result = self.answer_generator.generate_answer(question, docs)
        
        # Get scores
        docs_with_scores = self.retriever.retrieve_with_scores(question, k=k)
        scores = [1 - score for _, score in docs_with_scores]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'question': question,
            'answer': result['answer'],
            'sources': result['sources'],
            'confidence': avg_score,
            'num_docs': result['num_docs']
        }
    
    def get_stats(self) -> Dict:
        """Get pipeline statistics"""
        return {
            'store_name': self.store_name,
            'num_documents': self.vector_manager.get_count(),
            'embedding_model': self.embedding_manager.model_name,
            'llm_model': self.llm_manager.model_name
        }