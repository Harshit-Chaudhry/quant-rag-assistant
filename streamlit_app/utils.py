# streamlit_app/utils.py
"""
Helper functions for Streamlit app
Handles all API communication
"""
import requests
import streamlit as st
from typing import Dict, List, Optional

# API Base URL
API_URL = "http://localhost:8000"


def check_api_health() -> bool:
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_api_stats() -> Optional[Dict]:
    """Get API statistics"""
    try:
        response = requests.get(f"{API_URL}/stats")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def get_companies() -> List[str]:
    """Get list of companies in system"""
    try:
        response = requests.get(f"{API_URL}/companies")
        if response.status_code == 200:
            data = response.json()
            return data.get("companies", [])
        return []
    except:
        return []


def add_company(ticker: str) -> Dict:
    """Add a single company"""
    try:
        response = requests.post(
            f"{API_URL}/ingest/single",
            json={"ticker": ticker}
        )
        return response.json()
    except Exception as e:
        return {"success": False, "message": str(e)}


def add_multiple_companies(tickers: List[str]) -> Dict:
    """Add multiple companies"""
    try:
        response = requests.post(
            f"{API_URL}/ingest/multiple",
            json={"tickers": tickers}
        )
        return response.json()
    except Exception as e:
        return {"success": False, "message": str(e)}


def ask_question(question: str, num_results: int = 3) -> Dict:
    """Ask a question to the RAG system"""
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question,
                "num_results": num_results
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            error_data = response.json()
            return {
                "error": True,
                "message": error_data.get("detail", "Unknown error")
            }
    except Exception as e:
        return {"error": True, "message": str(e)}