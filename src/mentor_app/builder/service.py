"""Main Builder service for content generation."""

import os
import sys
from typing import Optional
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from mentor_app.models import Module, CourseContext, UserContext
from mentor_app.architect.service import ArchitectService
from mentor_app.builder.models import (
    ModuleContent, LessonContent,
    ContentGenerationError, InvalidModuleError
)


class ContentGenerator:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client or ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
        self.architect = ArchitectService()

    def generate_module_content(
        self,
        module: Module,
        course_context: CourseContext,
        user_context: Optional[UserContext] = None
    ) -> ModuleContent:
        """Generate detailed content for a module from its outline."""
        try:
            self._validate_module(module)
            
            lessons = []
            for lesson_outline in module.lessons:
                lesson_content = self._generate_lesson_content(
                    lesson_outline, course_context, user_context
                )
                lessons.append(lesson_content)
            
            return ModuleContent(
                title=module.title,
                description=module.description,
                learning_objectives=module.learning_objectives,
                estimated_duration=module.estimated_duration,
                lessons=lessons
            )
            
        except Exception as e:
            raise ContentGenerationError(f"Failed to generate module content: {str(e)}")

    def _validate_module(self, module: Module):
        """Validate module structure."""
        if not module.lessons:
            raise InvalidModuleError("Module must have lessons")

    def _generate_lesson_content(
        self,
        lesson_outline,
        course_context: CourseContext,
        user_context: Optional[UserContext]
    ) -> LessonContent:
        """Generate lesson content using AI with proper instructions."""
        
        prompt = self._build_lesson_prompt(lesson_outline, course_context, user_context)
        
        try:
            response = self.llm_client.invoke([HumanMessage(content=prompt)])
            return self._parse_ai_response(response.content, lesson_outline)
        except Exception as e:
            raise ContentGenerationError(f"Failed to generate lesson {lesson_outline.id}: {str(e)}")

    def _build_lesson_prompt(self, lesson_outline, course_context: CourseContext, user_context: Optional[UserContext]) -> str:
        """Build comprehensive prompt for AI lesson generation."""
        
        user_info = ""
        if user_context:
            user_info = f"""
User Context:
- Skill Level: {user_context.skill_level}
- Learning Style: {user_context.learning_style}
- Prior Knowledge: {', '.join(user_context.prior_knowledge)}
"""

        lesson_instructions = self._get_lesson_type_instructions(lesson_outline.type)
        
        return f"""Generate a complete lesson for an educational course.

Course Context:
- Course: {course_context.course_title}
- Domain: {course_context.topic_domain}
- Difficulty: {course_context.difficulty_level}
- Special Instructions: {course_context.user_instructions or 'None'}

{user_info}

Lesson Details:
- Title: {lesson_outline.title}
- Type: {lesson_outline.type}
- Key Concepts: {', '.join(lesson_outline.key_concepts)}
- Difficulty: {lesson_outline.difficulty}

{lesson_instructions}

Generate the complete lesson content now."""

    def _get_lesson_type_instructions(self, lesson_type: str) -> str:
        """Get specific instructions based on lesson type."""
        
        if lesson_type == "theory":
            return """Instructions for Theory Lesson:
- Create comprehensive educational content (800-1200 words)
- Use clear markdown formatting with headers and sections
- Explain concepts with real-world examples
- Include practical applications and use cases
- Add code examples ONLY if they directly illustrate key concepts
- End with a summary of key takeaways
- Make content engaging and easy to understand"""
            
        elif lesson_type == "practice":
            return """Instructions for Practice Lesson:
- Create 2-3 hands-on exercises that apply the key concepts
- Each exercise should have: clear instructions, starter code (if needed), expected outcome
- Provide step-by-step guidance
- Include hints for common challenges
- Focus on practical application rather than theory
- Exercises should build upon each other in complexity"""
            
        elif lesson_type == "assessment":
            return """Instructions for Assessment Lesson:
- Create 5-7 questions that test understanding of key concepts
- Mix question types: multiple choice, short answer, practical problems
- Each question should test a specific concept or skill
- Provide clear instructions and time estimates
- Include answer explanations
- Questions should be challenging but fair for the difficulty level"""
            
        else:
            return "Generate appropriate lesson content based on the lesson type and context."

    def _parse_ai_response(self, ai_response: str, lesson_outline) -> LessonContent:
        """Parse AI response into structured lesson content."""
        
        return LessonContent(
            id=lesson_outline.id,
            title=lesson_outline.title,
            type=lesson_outline.type,
            content_markdown=ai_response,
            key_concepts=lesson_outline.key_concepts,
            difficulty=lesson_outline.difficulty,
            code_examples=[],  # Extracted from content if present
            interactive_elements=[],  # Generated separately if needed
            practice_tasks=[],  # Extracted from content if present
            estimated_duration=self._estimate_duration(ai_response, lesson_outline.type)
        )

    def _estimate_duration(self, content: str, lesson_type: str) -> int:
        """Estimate lesson duration based on content length and type."""
        word_count = len(content.split())
        
        if lesson_type == "theory":
            return max(20, word_count // 15)  # ~15 words per minute reading
        elif lesson_type == "practice":
            return max(30, word_count // 10)  # More time for hands-on work
        elif lesson_type == "assessment":
            return max(15, word_count // 20)  # Quick assessment time
        else:
            return max(20, word_count // 15)
