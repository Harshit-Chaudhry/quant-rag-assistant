# streamlit_app/app.py
"""
Main Streamlit app - Home page
"""
import streamlit as st
from utils import check_api_health, get_companies, get_api_stats

# Page config
st.set_page_config(
    page_title="Quant RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-healthy {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🤖 Quant RAG Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Financial Analysis for Indian Stocks</div>', unsafe_allow_html=True)

# Check API status
api_status = check_api_health()

if api_status:
    st.markdown('<div class="status-box status-healthy">✅ API is running and healthy!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-box status-error">❌ API is not running. Please start the API server first.</div>', unsafe_allow_html=True)
    st.code("python run_api.py", language="bash")
    st.stop()

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Add Companies")
    st.write("Ingest stock data from Yahoo Finance into the system")
    if st.button("➡️ Go to Add Companies", use_container_width=True):
        st.switch_page("pages/1_Add_Companies.py")

with col2:
    st.markdown("### 💬 Ask Questions")
    st.write("Query the system with natural language questions")
    if st.button("➡️ Go to Ask Questions", use_container_width=True):
        st.switch_page("pages/2_Ask_Questions.py")

with col3:
    st.markdown("### 📈 Statistics")
    st.write("View system statistics and ingested companies")
    if st.button("➡️ Go to Statistics", use_container_width=True):
        st.switch_page("pages/3_Statistics.py")

# Divider
st.divider()

# Quick stats
st.markdown("### 📊 Quick Overview")

stats = get_api_stats()
companies = get_companies()

if stats:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Companies", len(companies))
    
    with col2:
        st.metric("Document Chunks", stats.get("total_chunks", 0))
    
    with col3:
        st.metric("Vectorstore", stats.get("vectorstore_status", "N/A").title())
    
    with col4:
        st.metric("LLM Model", stats.get("llm_model", "N/A"))

# Recent companies
if companies:
    st.markdown("### 🏢 Recently Added Companies")
    
    # Show as chips
    chips_html = ""
    for company in companies[:10]:  # Show max 10
        chips_html += f'<span style="display:inline-block; background-color:#e7f3ff; padding:0.3rem 0.8rem; margin:0.2rem; border-radius:1rem; font-size:0.9rem;">{company}</span>'
    
    st.markdown(chips_html, unsafe_allow_html=True)
    
    if len(companies) > 10:
        st.write(f"...and {len(companies) - 10} more")
else:
    st.info("👋 No companies added yet. Start by adding some companies!")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        Built with ❤️ using FastAPI + LangChain + Streamlit<br>
        <small>Your AI-powered financial research assistant</small>
    </div>
""", unsafe_allow_html=True)