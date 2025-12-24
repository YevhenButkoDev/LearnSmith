"""Main Architect service for course planning."""

import json
import os
import sys
from typing import Optional
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from mentor_app.models import CoursePlan, UserContext
from mentor_app.architect.prompts import SYLLABUS_PROMPT

class ArchitectService:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client or ChatOpenAI(
            model="gpt-5.2",  # Using GPT-4o as GPT-5.2 is not available
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    
    def create_syllabus(
        self, 
        topic: str, 
        user_instructions: Optional[str] = None,
        user_context: Optional[UserContext] = None
    ) -> CoursePlan:
        """Generate a structured course plan for the given topic."""
        prompt = SYLLABUS_PROMPT.format(
            topic=topic,
            skill_level=user_context.skill_level if user_context else "beginner",
            learning_style=user_context.learning_style if user_context else "hands-on",
            time_commitment=user_context.time_commitment if user_context else 5,
            prior_knowledge=", ".join(user_context.prior_knowledge) if user_context and user_context.prior_knowledge else "None",
            user_instructions=user_instructions or "No special instructions"
        )
        
        response = self.llm_client.invoke([HumanMessage(content=prompt)])
        
        try:
            # Extract JSON from markdown code blocks if present
            content = response.content.strip()
            if content.startswith('```json'):
                content = content[7:]  # Remove ```json
            if content.startswith('```'):
                content = content[3:]   # Remove ```
            if content.endswith('```'):
                content = content[:-3]  # Remove closing ```
            
            course_data = json.loads(content.strip())
            return CoursePlan(**course_data)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Raw response: {response.content}")
            raise ValueError(f"Failed to parse LLM response: {e}")

def main():
    """Test function for the Architect service."""
    from dotenv import load_dotenv
    load_dotenv()
    
    architect = ArchitectService()
    
    # Test with basic topic
    user_context = UserContext(
        skill_level="intermediate",
        learning_style="hands-on",
        time_commitment=8,
        prior_knowledge=["basic SQL", "database design"]
    )
    
    course_plan = architect.create_syllabus(
        topic="Advanced SQL",
        user_instructions="Focus heavily on complex joins, window functions, and query optimization. Include performance tuning exercises.",
        user_context=user_context
    )
    
    print(f"Generated course: {course_plan.course_title}")
    print(f"Duration: {course_plan.estimated_duration} hours")
    print(f"Modules: {len(course_plan.modules)}")
    for module in course_plan.modules:
        print(f"  - {module.title} ({len(module.lessons)} lessons)")

if __name__ == "__main__":
    main()
