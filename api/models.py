# api/models.py
"""
Data models - These define what requests/responses look like
Think of it like a form: "Name must be text, Age must be number"
"""
from pydantic import BaseModel, Field
from typing import List, Optional


# ============================================================
# REQUEST MODELS (What user sends to API)
# ============================================================

class AddCompanyRequest(BaseModel):
    """When user wants to add a company"""
    ticker: str = Field(..., description="Stock ticker like TCS.NS")
    
    class Config:
        # Example that shows up in API docs
        json_schema_extra = {
            "example": {"ticker": "TCS.NS"}
        }


class AddMultipleRequest(BaseModel):
    """When user wants to add multiple companies at once"""
    tickers: List[str] = Field(..., description="List of tickers")
    
    class Config:
        json_schema_extra = {
            "example": {"tickers": ["TCS.NS", "INFY.NS", "RELIANCE.NS"]}
        }


class QuestionRequest(BaseModel):
    """When user asks a question"""
    question: str = Field(..., description="Your question")
    num_results: int = Field(3, description="How many sources to use (1-10)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is TCS's revenue?",
                "num_results": 3
            }
        }


# ============================================================
# RESPONSE MODELS (What API sends back to user)
# ============================================================

class AddCompanyResponse(BaseModel):
    """Response after adding company"""
    success: bool
    ticker: str
    message: str
    total_companies: int


class QuestionResponse(BaseModel):
    """Response with answer to question"""
    question: str
    answer: str
    sources: List[str]
    confidence: float
    response_time: float  # How long it took


class StatsResponse(BaseModel):
    """System statistics"""
    total_companies: int
    total_chunks: int
    embedding_model: str
    llm_model: str
    vectorstore_status: str


class ErrorResponse(BaseModel):
    """When something goes wrong"""
    error: str
    detail: Optional[str] = None