# api/main.py
"""
Main FastAPI application with production features:
- Error handling
- Request validation
- Rate limiting awareness
- Logging
- Auto documentation
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import time
from datetime import datetime
from dotenv import load_dotenv

from .models import (
    AddCompanyRequest, AddCompanyResponse,
    AddMultipleRequest, QuestionRequest, QuestionResponse,
    StatsResponse, ErrorResponse
)
from src.pipeline import RAGPipeline

# Load environment
load_dotenv()

# Global variables
pipeline = None
request_count = 0  # Track API usage


# ============================================================
# STARTUP & SHUTDOWN (Lifecycle Management)
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    What happens when API starts and stops
    
    Startup: Initialize pipeline, load data
    Shutdown: Clean up resources
    """
    global pipeline
    
    # STARTUP
    print("\n" + "="*70)
    print("🚀 STARTING QUANT RAG ASSISTANT API")
    print("="*70)
    
    try:
        # Initialize pipeline
        print("Initializing RAG pipeline...")
        pipeline = RAGPipeline(store_name="indian_stocks")
        
        # Try to load existing vector store
        try:
            pipeline.load_vectorstore()
            print(f"✓ Loaded existing vector store ({pipeline.vector_manager.get_count()} chunks)")
        except Exception as e:
            print("⚠ No existing vector store (will create on first ingest)")
        
        print("✓ API Ready!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ FAILED TO START: {e}")
        raise
    
    yield  # API runs here
    
    # SHUTDOWN
    print("\n" + "="*70)
    print("Shutting down API...")
    print(f"Total requests served: {request_count}")
    print("="*70)


# ============================================================
# CREATE APP
# ============================================================

app = FastAPI(
    title="Quant RAG Assistant",
    description="""
    🤖 AI-powered financial analysis system for Indian stocks
    
    Features:
    - Fetch real-time stock data from Yahoo Finance
    - Semantic search through financial documents
    - LLM-powered Q&A with citations
    - Multi-company support
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# ============================================================
# MIDDLEWARE (Runs before/after each request)
# ============================================================

# Enable CORS (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    """
    Log every API request
    Shows: timestamp, method, path, response time
    """
    global request_count
    
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate time taken
    process_time = time.time() - start_time
    request_count += 1
    
    # Log it
    print(f"[{datetime.now()}] {request.method} {request.url.path} - {process_time:.2f}s")
    
    return response


# ============================================================
# HEALTH & INFO ENDPOINTS
# ============================================================

@app.get("/", tags=["Health"])
def root():
    """
    Root endpoint - API welcome message
    """
    return {
        "message": "🤖 Quant RAG Assistant API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check - Is API alive?
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "pipeline_loaded": pipeline is not None,
        "vectorstore_loaded": pipeline.vector_manager.vectorstore is not None if pipeline else False
    }


@app.get("/stats", response_model=StatsResponse, tags=["Info"])
def get_statistics():
    """
    Get system statistics
    Shows: number of companies, chunks, models used
    """
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline not initialized"
        )
    
    stats = pipeline.get_stats()
    
    # Check if vectorstore is loaded
    vs_status = "loaded" if pipeline.vector_manager.vectorstore else "empty"
    
    return StatsResponse(
        total_companies=len(list_company_files()),
        total_chunks=stats['num_documents'],
        embedding_model=stats['embedding_model'],
        llm_model=stats['llm_model'],
        vectorstore_status=vs_status
    )


@app.get("/companies", tags=["Info"])
def list_companies():
    """
    List all ingested companies
    Shows which companies are in the system
    """
    companies = list_company_files()
    
    return {
        "count": len(companies),
        "companies": companies,
        "message": f"Found {len(companies)} companies in system"
    }


# ============================================================
# INGESTION ENDPOINTS (Add Data)
# ============================================================

@app.post("/ingest/single", response_model=AddCompanyResponse, tags=["Ingestion"])
def add_single_company(request: AddCompanyRequest):
    """
    Add a single company to the system
    
    Process:
    1. Fetch data from Yahoo Finance
    2. Create financial document
    3. Chunk the document
    4. Generate embeddings
    5. Store in vector database
    
    Takes ~30 seconds per company
    """
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline not initialized"
        )
    
    try:
        print(f"\n📊 Adding {request.ticker}...")
        
        # Ingest the stock
        success = pipeline.ingest_stock(request.ticker, save_doc=True)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch data for {request.ticker}"
            )
        
        # Save vector store
        pipeline.save_vectorstore()
        
        return AddCompanyResponse(
            success=True,
            ticker=request.ticker,
            message=f"Successfully added {request.ticker}",
            total_companies=len(list_company_files())
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@app.post("/ingest/multiple", tags=["Ingestion"])
def add_multiple_companies(request: AddMultipleRequest):
    """
    Add multiple companies at once
    
    More efficient than adding one-by-one
    Returns success/failure for each ticker
    """
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline not initialized"
        )
    
    try:
        print(f"\n📊 Adding {len(request.tickers)} companies...")
        
        results = pipeline.ingest_multiple_stocks(request.tickers)
        
        # Save after all ingestions
        pipeline.save_vectorstore()
        
        return {
            "success_count": len(results['success']),
            "failed_count": len(results['failed']),
            "successful": results['success'],
            "failed": results['failed'],
            "total_companies": len(list_company_files())
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


# ============================================================
# QUERY ENDPOINT (Ask Questions)
# ============================================================

@app.post("/ask", response_model=QuestionResponse, tags=["Query"])
def ask_question(request: QuestionRequest):
    """
    Ask a question about your companies
    
    Process:
    1. Semantic search to find relevant chunks
    2. Send chunks + question to LLM
    3. Generate answer with citations
    4. Return answer + confidence score
    
    Takes ~3-5 seconds
    """
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline not initialized"
        )
    
    # Check if we have data
    if pipeline.vector_manager.vectorstore is None:
        try:
            pipeline.load_vectorstore()
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No companies in system. Please add companies first using /ingest/single"
            )
    
    try:
        print(f"\n❓ Question: {request.question}")
        
        start_time = time.time()
        
        # Query the pipeline
        result = pipeline.query(
            question=request.question,
            k=request.num_results
        )
        
        response_time = time.time() - start_time
        
        return QuestionResponse(
            question=result['question'],
            answer=result['answer'],
            sources=result['sources'],
            confidence=round(result['confidence'], 2),
            response_time=round(response_time, 2)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def list_company_files():
    """Helper: List all company files"""
    from pathlib import Path
    from src.config.settings import settings
    
    companies = []
    doc_dir = settings.DOCUMENTS_DIR
    
    if doc_dir.exists():
        for file in doc_dir.glob("*_report.txt"):
            ticker = file.stem.replace("_report", "").replace("_", ".")
            companies.append(ticker)
    
    return sorted(companies)


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Catch all unhandled errors
    Returns clean error message instead of crash
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )