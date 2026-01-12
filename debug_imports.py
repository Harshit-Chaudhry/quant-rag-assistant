# debug_imports.py
import sys
print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\n" + "="*60)

try:
    from langchain_core.documents import Document
    print("✅ langchain_core.documents.Document - OK")
except Exception as e:
    print(f"❌ langchain_core.documents.Document - FAILED: {e}")

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✅ langchain_text_splitters - OK")
except Exception as e:
    print(f"❌ langchain_text_splitters - FAILED: {e}")

try:
    from langchain_community.vectorstores import FAISS
    print("✅ langchain_community.vectorstores - OK")
except Exception as e:
    print(f"❌ langchain_community.vectorstores - FAILED: {e}")

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("✅ langchain_community.embeddings - OK")
except Exception as e:
    print(f"❌ langchain_community.embeddings - FAILED: {e}")

print("\n" + "="*60)
print("Checking src imports...")

try:
    from src.config.settings import settings
    print("✅ src.config.settings - OK")
except Exception as e:
    print(f"❌ src.config.settings - FAILED: {e}")

try:
    from src.retrieval.retriever import Retriever
    print("✅ src.retrieval.retriever - OK")
except Exception as e:
    print(f"❌ src.retrieval.retriever - FAILED: {e}")