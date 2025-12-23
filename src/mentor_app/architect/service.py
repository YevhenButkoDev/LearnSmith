"""Main Architect service for course planning."""

from .models import CoursePlan
from .prompts import SYLLABUS_PROMPT

class ArchitectService:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def create_syllabus(self, topic: str) -> CoursePlan:
        """Generate a structured course plan for the given topic."""
        prompt = SYLLABUS_PROMPT.format(topic=topic)
        # Implementation will use LLM client
        pass
