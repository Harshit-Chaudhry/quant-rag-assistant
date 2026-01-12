# src/generation/llm_manager.py
"""LLM management"""
from google import genai  # UPDATED
from google.genai import types  # UPDATED
from ..config.settings import settings


class LLMManager:
    """Manages LLM interactions"""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or settings.GOOGLE_API_KEY
        self.model_name = model_name or settings.LLM_MODEL
        
        if not self.api_key:
            raise ValueError("Google API key not set")
        
        # Configure client
        self.client = genai.Client(api_key=self.api_key)
        
        print(f"✓ LLM ready: {self.model_name}")
    
    def generate(self, prompt: str) -> str:
        """Generate response from prompt"""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text
    
    def get_model(self):
        """Get the LLM client"""
        return self.client