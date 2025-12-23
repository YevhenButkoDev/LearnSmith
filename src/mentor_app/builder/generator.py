"""Content generator for individual lessons."""

class ContentGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def generate_lesson(self, lesson_title: str, objectives: list) -> dict:
        """Generate detailed lesson content."""
        pass
