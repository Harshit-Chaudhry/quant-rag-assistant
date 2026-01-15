# streamlit_app/pages/2_💬_Ask_Questions.py
"""
Page to ask questions to the RAG system
"""
import streamlit as st
import time
from utils import check_api_health, ask_question, get_companies

st.set_page_config(page_title="Ask Questions", page_icon="💬", layout="wide")

# Header
st.title("💬 Ask Questions")
st.write("Query your financial data using natural language")

# Check API
if not check_api_health():
    st.error("❌ API is not running. Please start it first.")
    st.stop()

# Check if we have companies
companies = get_companies()
if not companies:
    st.warning("⚠️ No companies in the system yet. Please add companies first.")
    if st.button("➕ Go to Add Companies"):
        st.switch_page("pages/1_📊_Add_Companies.py")
    st.stop()

# Show available companies
with st.expander("🏢 Available Companies"):
    st.write(", ".join(companies))

# Question input
st.markdown("### 🤔 What would you like to know?")

question = st.text_input(
    "Your Question",
    placeholder="e.g., What is TCS's revenue? Compare TCS and Infosys profit margins.",
    label_visibility="collapsed"
)

# Sample questions
st.markdown("**💡 Sample Questions:**")
sample_questions = [
    "What is TCS's revenue?",
    "What is the profit margin of Infosys?",
    "Compare TCS and Infosys market cap",
    "What sector does Reliance operate in?",
    "How many employees does TCS have?"
]

cols = st.columns(len(sample_questions))
for idx, sample in enumerate(sample_questions):
    with cols[idx]:
        if st.button(sample, key=f"sample_{idx}", use_container_width=True):
            question = sample

# Advanced settings
with st.expander("⚙️ Advanced Settings"):
    num_results = st.slider(
        "Number of sources to retrieve",
        min_value=1,
        max_value=10,
        value=3,
        help="More sources = more context but slower"
    )

# Ask button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    ask_btn = st.button("🚀 Ask Question", type="primary", use_container_width=True)

# Process question
if ask_btn and question:
    
    with st.spinner("🤔 Thinking..."):
        start_time = time.time()
        result = ask_question(question, num_results)
        elapsed_time = time.time() - start_time
    
    if result.get("error"):
        st.error(f"❌ Error: {result.get('message')}")
    else:
        # Success - show answer
        st.markdown("---")
        st.markdown("### 💡 Answer")
        
        # Answer box
        st.markdown(f"""
            <div style="padding:1.5rem; background-color:#f0f8ff; border-left:4px solid #1f77b4; border-radius:0.5rem; margin:1rem 0;">
                <p style="font-size:1.1rem; margin:0;">{result['answer']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Metadata
        col1, col2, col3 = st.columns(3)
        
        with col1:
            confidence_pct = result['confidence'] * 100
            st.metric("Confidence", f"{confidence_pct:.0f}%")
        
        with col2:
            st.metric("Response Time", f"{result['response_time']:.2f}s")
        
        with col3:
            st.metric("Sources Used", result['num_docs'])
        
        # Sources
        st.markdown("### 📚 Sources")
        for source in result['sources']:
            st.markdown(f"- 📄 {source}")
        
        # Feedback
        st.markdown("---")
        st.markdown("**Was this answer helpful?**")
        col1, col2 = st.columns([1, 5])
        with col1:
            st.button("👍 Yes")
        with col2:
            st.button("👎 No")

# Chat history (stored in session state)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Add to history
if ask_btn and question and not result.get("error"):
    st.session_state.chat_history.append({
        "question": question,
        "answer": result['answer'],
        "confidence": result['confidence']
    })

# Show history
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📜 Recent Questions")
    
    for idx, item in enumerate(reversed(st.session_state.chat_history[-5:])):
        with st.expander(f"Q: {item['question']}", expanded=False):
            st.write(item['answer'])
            st.caption(f"Confidence: {item['confidence']*100:.0f}%")

# Back button
st.divider()
if st.button("⬅️ Back to Home"):
    st.switch_page("app.py")