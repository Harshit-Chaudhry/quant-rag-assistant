"""Answer generation"""
from typing import List, Dict
from langchain_core.documents import Document
from .llm_manager import LLMManager


class AnswerGenerator:
    """Generates answers from retrieved documents"""
    
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager
    
    def generate_answer(self, query: str, documents: List[Document]) -> Dict:
        """Generate answer from documents"""
        
        # Combine context
        context = "\n\n---\n\n".join([doc.page_content for doc in documents])
        
        # Create prompt
        prompt = f"""You are a financial analyst assistant for Indian stocks.

Answer using ONLY the information in the context below.

RULES:
1. Answer ONLY from the context
2. If info not available, say "Information not available"
3. Include specific numbers and metrics
4. Be concise (2-4 sentences)
5. Be factual and precise

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
        
        # Generate
        answer = self.llm_manager.generate(prompt)
        
        # Extract sources
        sources = []
        for doc in documents:
            if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                source = doc.metadata['source'].split('/')[-1]
                if source not in sources:
                    sources.append(source)
        
        return {
            'answer': answer,
            'sources': sources,
            'num_docs': len(documents)
        }