# run_streamlit.py
"""
Run the Streamlit app
"""
import os
import subprocess

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎨 STARTING STREAMLIT FRONTEND")
    print("="*70)
    print("Make sure your FastAPI server is running on port 8000!")
    print("If not, run: python run_api.py")
    print("="*70 + "\n")
    
    # Run streamlit
    subprocess.run([
        "streamlit",
        "run",
        "streamlit_app/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])