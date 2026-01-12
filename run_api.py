# run_api.py
"""
Simple script to run the API server
"""
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "="*70)
    print("🚀 STARTING QUANT RAG ASSISTANT API")
    print("="*70)
    print(f"📍 Server URL:  http://localhost:{port}")
    print(f"📚 API Docs:    http://localhost:{port}/docs")
    print(f"📖 Alt Docs:    http://localhost:{port}/redoc")
    print("="*70)
    print("\n💡 Tip: Open /docs in your browser for interactive testing!")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )