# Quant RAG Assistant

A Retrieval-Augmented Generation (RAG) application that combines Large Language Models with quantitative financial data to provide intelligent analysis and insights. Built with LangChain, FastAPI, and Streamlit.

## 📋 Overview

Quant RAG Assistant is a sophisticated AI-powered tool designed to help users analyze quantitative financial information by leveraging:
- **RAG (Retrieval-Augmented Generation)**: Combines external financial data with LLM capabilities
- **Financial Data Integration**: Real-time financial data through yfinance
- **Document Processing**: PDF analysis for financial documents
- **Semantic Search**: Using embeddings and vector databases for intelligent retrieval

## 🚀 Features

- **Dual Interface**: 
  - FastAPI REST API for programmatic access
  - Streamlit web application for interactive exploration
- **Real-time Financial Data**: Integration with yfinance for current market data
- **Document Analysis**: Process and query PDF documents
- **Advanced RAG Pipeline**: LangChain-based retrieval and generation
- **Vector Search**: FAISS vector database for efficient semantic search
- **Multi-format Support**: Pandas dataframe processing and visualization

## 🛠️ Tech Stack

### Core Dependencies
- **LLMs & RAG**: 
  - `langchain` - Framework for building applications with LLMs
  - `langchain-community` - Community integrations
  - `langgraph` - Graph-based LLM workflows
  - `google-generativeai` - Google's Generative AI API
  - `langchain-huggingface` - Hugging Face integration

- **Embeddings & Vector Store**:
  - `sentence-transformers` - State-of-the-art sentence embeddings
  - `faiss-cpu` - Efficient similarity search and clustering

- **Data Sources**:
  - `yfinance` - Yahoo Finance data
  - `pandas` - Data manipulation and analysis
  - `pypdf` - PDF processing

- **Backend**:
  - `fastapi` - Modern async web framework
  - `uvicorn` - ASGI server
  - `python-multipart` - Form data parsing

- **Frontend**:
  - `streamlit` - Rapid web app development
  - `plotly` - Interactive visualizations
  - `requests` - HTTP client library

- **Utilities**:
  - `python-dotenv` - Environment variable management
  - `pydantic` - Data validation

## 📁 Project Structure

```
quant-rag-assistant/
├── api/                    # FastAPI application modules
├── src/                    # Source code for core logic
├── streamlit_app/          # Streamlit application files
├── data/                   # Data directory for processed files
├── APItesting.py           # API testing utilities
├── run_api.py              # FastAPI server entry point
├── run_streamlit.py        # Streamlit app entry point
├── test.py                 # Test suite
├── check_allfiles.py       # File verification utility
├── debug_imports.py        # Import debugging utility
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
└── .dockerignore           # Docker ignore rules
```

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Harshit-Chaudhry/quant-rag-assistant.git
cd quant-rag-assistant
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env  # Create from template if available
# Edit .env with your API keys and configuration
```

## 🚀 Usage

### Running the Streamlit App
Interactive web interface for exploring financial data and RAG queries:

```bash
python run_streamlit.py
```
The app will be available at http://localhost:8501

### Running the FastAPI Server
REST API for programmatic access:

```bash
python run_api.py
```
- The API will be available at http://localhost:8000
- API documentation available at http://localhost:8000/docs

### Testing
Run the test suite:

```bash
python test.py
```

### Docker Deployment
Build and run with Docker:

```bash
docker build -t quant-rag-assistant .
docker run -p 8000:8000 -p 8501:8501 quant-rag-assistant
```

## 📊 API Endpoints

The FastAPI server provides endpoints for:

- Financial data queries
- Document upload and processing
- RAG-based question answering
- Quantitative analysis

Full API documentation available at `/docs` when running the API server.

## 🔍 Key Capabilities

- **Financial Data Retrieval**: Fetch real-time market data using yfinance
- **Document Intelligence**: Upload and analyze financial documents (PDFs)
- **Semantic Search**: Find relevant financial information using embeddings
- **Intelligent Responses**: Generate context-aware answers using LLMs
- **Data Visualization**: Interactive charts and plots with Plotly

## 🧪 Testing

Utility scripts for development and debugging:

- `test.py` - Main test suite
- `APItesting.py` - API endpoint testing
- `debug_imports.py` - Dependency verification
- `check_allfiles.py` - Project structure validation

## 📝 Environment Configuration

Create a `.env` file in the root directory with:

```env
GOOGLE_API_KEY=your_google_api_key_here
# Add other configuration as needed
```

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- Report bugs
- Suggest enhancements
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Harshit Chaudhry**

## 🔗 Links

- Repository: [GitHub](https://github.com/Harshit-Chaudhry/quant-rag-assistant)
- Issue Tracker: [GitHub Issues](https://github.com/Harshit-Chaudhry/quant-rag-assistant/issues)

## 📞 Support

For issues, questions, or feedback, please open an issue on the GitHub repository.

---

**Last Updated**: February 2026
