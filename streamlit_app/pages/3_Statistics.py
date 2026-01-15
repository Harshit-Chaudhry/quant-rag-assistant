# streamlit_app/pages/3_📈_Statistics.py
"""
Statistics and system information page
"""
import streamlit as st
import plotly.graph_objects as go
from utils import check_api_health, get_api_stats, get_companies

st.set_page_config(page_title="Statistics", page_icon="📈", layout="wide")

# Header
st.title("📈 System Statistics")
st.write("Overview of your RAG system")

# Check API
if not check_api_health():
    st.error("❌ API is not running")
    st.stop()

# Get data
stats = get_api_stats()
companies = get_companies()

if not stats:
    st.error("Failed to fetch statistics")
    st.stop()

# Metrics row
st.markdown("### 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Companies",
        len(companies),
        delta=None,
        help="Number of companies ingested in the system"
    )

with col2:
    st.metric(
        "Document Chunks",
        stats.get("total_chunks", 0),
        delta=None,
        help="Number of text chunks in vector store"
    )

with col3:
    st.metric(
        "Vectorstore Status",
        stats.get("vectorstore_status", "N/A").title(),
        delta=None,
        help="Status of the vector database"
    )

with col4:
    avg_chunks = stats.get("total_chunks", 0) / len(companies) if companies else 0
    st.metric(
        "Avg Chunks/Company",
        f"{avg_chunks:.1f}",
        delta=None,
        help="Average chunks per company"
    )

st.divider()

# System info
st.markdown("### ⚙️ System Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Embedding Model**")
    st.code(stats.get("embedding_model", "N/A"), language="text")
    
    st.markdown("**Vector Store Name**")
    st.code(stats.get("store_name", "N/A"), language="text")

with col2:
    st.markdown("**LLM Model**")
    st.code(stats.get("llm_model", "N/A"), language="text")
    
    st.markdown("**API Status**")
    st.success("✅ Healthy")

st.divider()

# Companies list
st.markdown("### 🏢 Ingested Companies")

if companies:
    # Simple chart
    fig = go.Figure(data=[
        go.Bar(
            x=companies,
            y=[1] * len(companies),
            text=companies,
            textposition='auto',
            marker_color='lightblue'
        )
    ])
    
    fig.update_layout(
        title="Companies in System",
        xaxis_title="Company",
        yaxis_title="",
        showlegend=False,
        height=400,
        yaxis=dict(showticklabels=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Table view
    st.markdown("**Detailed View:**")
    for idx, company in enumerate(companies, 1):
        st.markdown(f"{idx}. **{company}**")
else:
    st.info("No companies in system yet")

# Refresh button
st.divider()
col1, col2 = st.columns([1, 5])

with col1:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

with col2:
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.switch_page("app.py")