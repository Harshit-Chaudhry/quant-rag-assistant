# streamlit_app/pages/1_📊_Add_Companies.py
"""
Page to add companies to the system
"""
import streamlit as st
import time
from utils import check_api_health, add_company, add_multiple_companies, get_companies

st.set_page_config(page_title="Add Companies", page_icon="📊", layout="wide")

# Header
st.title("📊 Add Companies")
st.write("Ingest stock data from Yahoo Finance into the RAG system")

# Check API
if not check_api_health():
    st.error("❌ API is not running. Please start it first.")
    st.code("python run_api.py", language="bash")
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["➕ Add Single", "📋 Add Multiple", "🏢 Current Companies"])

# TAB 1: Add Single Company
with tab1:
    st.markdown("### Add Single Company")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker_input = st.text_input(
            "Stock Ticker",
            placeholder="e.g., TCS.NS, INFY.NS, RELIANCE.NS",
            help="Enter the Yahoo Finance ticker symbol"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        add_button = st.button("➕ Add Company", type="primary", use_container_width=True)
    
    # Popular tickers
    st.markdown("**Popular Indian Stocks:**")
    popular_tickers = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "WIPRO.NS"]
    
    cols = st.columns(6)
    for idx, ticker in enumerate(popular_tickers):
        with cols[idx]:
            if st.button(ticker, key=f"pop_{ticker}"):
                ticker_input = ticker
                add_button = True
    
    # Process addition
    if add_button and ticker_input:
        with st.spinner(f"🔄 Fetching and processing {ticker_input}... This may take 30-60 seconds..."):
            result = add_company(ticker_input)
        
        if result.get("success"):
            st.success(f"✅ Successfully added {ticker_input}!")
            st.balloons()
            
            # Show details
            st.info(f"📊 Total companies in system: {result.get('total_companies', 'N/A')}")
        else:
            st.error(f"❌ Failed to add {ticker_input}")
            st.error(f"Reason: {result.get('message', 'Unknown error')}")

# TAB 2: Add Multiple Companies
with tab2:
    st.markdown("### Add Multiple Companies")
    st.info("💡 Add multiple companies at once. Enter one ticker per line.")
    
    tickers_text = st.text_area(
        "Stock Tickers (one per line)",
        placeholder="TCS.NS\nINFY.NS\nRELIANCE.NS",
        height=150
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        add_multiple_btn = st.button("➕ Add All", type="primary", use_container_width=True)
    
    if add_multiple_btn and tickers_text:
        # Parse tickers
        tickers = [t.strip() for t in tickers_text.split('\n') if t.strip()]
        
        if tickers:
            st.write(f"📋 Adding {len(tickers)} companies...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner(f"Processing {len(tickers)} companies..."):
                result = add_multiple_companies(tickers)
            
            progress_bar.progress(100)
            
            # Show results
            st.success(f"✅ Completed!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("✅ Successful", result.get("success_count", 0))
                if result.get("successful"):
                    for ticker in result["successful"]:
                        st.write(f"  ✓ {ticker}")
            
            with col2:
                st.metric("❌ Failed", result.get("failed_count", 0))
                if result.get("failed"):
                    for ticker in result["failed"]:
                        st.write(f"  ✗ {ticker}")

# TAB 3: Current Companies
with tab3:
    st.markdown("### 🏢 Companies in System")
    
    companies = get_companies()
    
    if companies:
        st.success(f"Found {len(companies)} companies")
        
        # Display as grid
        cols_per_row = 4
        for i in range(0, len(companies), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, company in enumerate(companies[i:i+cols_per_row]):
                with cols[j]:
                    st.markdown(f"""
                        <div style="padding:1rem; background-color:#f0f2f6; border-radius:0.5rem; text-align:center; margin:0.5rem 0;">
                            <strong>{company}</strong>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No companies added yet. Add some using the tabs above!")
    
    # Refresh button
    if st.button("🔄 Refresh List"):
        st.rerun()

# Back button
st.divider()
if st.button("⬅️ Back to Home"):
    st.switch_page("app.py")