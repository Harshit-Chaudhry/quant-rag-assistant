"""Yahoo Finance data source"""
import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
from .base import BaseDataSource


class YahooFinanceSource(BaseDataSource):
    """Yahoo Finance data source"""
    
    def __init__(self):
        super().__init__("YahooFinance")
    
    def fetch_company_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Fetch company data from Yahoo Finance"""
        try:
            print(f"Fetching data for {ticker}...")
            stock = yf.Ticker(ticker)
            
            data = {
                'ticker': ticker,
                'info': stock.info,
                'financials': stock.quarterly_financials,
                'balance_sheet': stock.quarterly_balance_sheet,
                'company_name': stock.info.get('longName', ticker)
            }
            
            print(f"✓ Fetched data for {ticker}")
            return data
            
        except Exception as e:
            print(f"✗ Error fetching {ticker}: {e}")
            return None
    
    def get_financials(self, ticker: str) -> Optional[pd.DataFrame]:
        """Get quarterly financials"""
        data = self.fetch_company_data(ticker)
        return data['financials'] if data else None
    
    def create_document(self, data: Dict[str, Any]) -> str:
        """Create formatted financial document"""
        
        info = data['info']
        financials = data['financials']
        company_name = data['company_name']
        ticker = data['ticker']
        
        doc = f"""
{'='*70}
{company_name} - FINANCIAL ANALYSIS REPORT
{'='*70}
Report Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}

COMPANY OVERVIEW
{'='*70}
Company Name: {info.get('longName', company_name)}
Stock Symbol: {ticker}
Sector: {info.get('sector', 'N/A')}
Industry: {info.get('industry', 'N/A')}
Market Cap: ₹{info.get('marketCap', 0):,.0f}
Employees: {info.get('fullTimeEmployees', 'N/A'):,}

BUSINESS DESCRIPTION
{'='*70}
{info.get('longBusinessSummary', 'Not available')}

KEY FINANCIAL METRICS
{'='*70}
"""
        
        # Add metrics
        metrics = {
            'Revenue (TTM)': info.get('totalRevenue'),
            'Net Profit Margin': info.get('profitMargins'),
            'Operating Margin': info.get('operatingMargins'),
            'Return on Equity': info.get('returnOnEquity'),
            'Debt to Equity': info.get('debtToEquity'),
            'Current Ratio': info.get('currentRatio'),
            'P/E Ratio': info.get('trailingPE'),
            'EPS': info.get('trailingEps'),
        }
        
        for name, value in metrics.items():
            if value is not None:
                if isinstance(value, float) and value < 10:
                    if 'Margin' in name or 'Return' in name:
                        doc += f"{name}: {value:.2%}\n"
                    else:
                        doc += f"{name}: {value:.2f}\n"
                elif isinstance(value, (int, float)):
                    if 'Revenue' in name:
                        doc += f"{name}: ₹{value:,.0f}\n"
                    else:
                        doc += f"{name}: {value:,.2f}\n"
        
        # Quarterly data
        doc += f"\nQUARTERLY PERFORMANCE\n{'='*70}\n"
        
        if not financials.empty:
            for col in financials.columns[:4]:
                quarter = col.strftime('%b %Y')
                doc += f"\nQuarter: {quarter}\n{'-'*40}\n"
                
                if 'Total Revenue' in financials.index:
                    rev = financials.loc['Total Revenue', col]
                    doc += f"Revenue: ₹{rev/10000000:,.2f} Cr\n"
                
                if 'Net Income' in financials.index:
                    profit = financials.loc['Net Income', col]
                    doc += f"Net Profit: ₹{profit/10000000:,.2f} Cr\n"
        
        doc += f"\n{'='*70}\nEnd of Report\n{'='*70}\n"
        
        return doc