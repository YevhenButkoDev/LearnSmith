"""LLM client wrapper for OpenAI/Claude/Gemini."""

import openai
import os

class LLMClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_response(self, prompt: str, model: str = "gpt-4") -> str:
        """Generate response from LLM."""
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def generate_json_response(self, prompt: str, model: str = "gpt-4") -> dict:
        """Generate structured JSON response."""
        pass
