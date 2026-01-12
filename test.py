import os
from dotenv import load_dotenv
from src.pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Set API key if not in .env
os.environ['GOOGLE_API_KEY'] = 'Your_API_KEY'  # Replace if needed

print("\n" + "="*60)
print("TESTING RAG PIPELINE")
print("="*60)

# Initialize pipeline
pipeline = RAGPipeline(store_name="indian_stocks")

# Ingest TCS data
pipeline.ingest_stock('TCS.NS')

# Save vector store
pipeline.save_vectorstore()

# Query
result = pipeline.query("What is TCS's revenue?")

print(f"\n{'='*60}")
print("RESULT")
print('='*60)
print(f"Question: {result['question']}")
print(f"\nAnswer: {result['answer']}")
print(f"\nSources: {', '.join(result['sources'])}")
print(f"Confidence: {result['confidence']:.0%}")

# Get stats
stats = pipeline.get_stats()
print(f"\n{'='*60}")
print("PIPELINE STATS")
print('='*60)
for key, value in stats.items():
    print(f"{key}: {value}")

print("\n✅ Test complete!")