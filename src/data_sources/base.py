"""Abstract base class for data sources"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd


class BaseDataSource(ABC):
    """Base class for financial data sources"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def fetch_company_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Fetch company data"""
        pass
    
    @abstractmethod
    def create_document(self, data: Dict[str, Any]) -> str:
        """Create formatted document from data"""
        pass
    
    @abstractmethod
    def get_financials(self, ticker: str) -> Optional[pd.DataFrame]:
        """Get financial statements"""
        pass