# check_files.py
import os

files_to_check = {
    'src/config/settings.py': 'Settings',
    'src/data_sources/base.py': 'BaseDataSource',
    'src/data_sources/yahoo_finance.py': 'YahooFinanceSource',
    'src/document_processing/loaders.py': 'DocumentLoader',
    'src/document_processing/chunkers.py': 'TextChunker',
    'src/embeddings/embedding_manager.py': 'EmbeddingManager',
    'src/vectorstore/vector_manager.py': 'VectorStoreManager',
    'src/retrieval/retriever.py': 'Retriever',
    'src/generation/llm_manager.py': 'LLMManager',
    'src/generation/answer_generator.py': 'AnswerGenerator',
    'src/pipeline.py': 'RAGPipeline',
}

print("Checking files...\n")

for filepath, class_name in files_to_check.items():
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            if class_name in content:
                print(f"✅ {filepath} - {class_name} found")
            else:
                print(f"⚠️  {filepath} - {class_name} NOT found")
    else:
        print(f"❌ {filepath} - FILE MISSING")