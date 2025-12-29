"""Mentor service that orchestrates architect and builder services with persistence."""

from typing import Optional
from mentor_app.models import CoursePlan, UserContext, Module, CourseContext
from mentor_app.builder.models import ModuleContent
from mentor_app.infrastructure.models import Module as DBModule
from mentor_app.architect.service import ArchitectService
from mentor_app.builder.service import ContentGenerator
from mentor_app.infrastructure.repositories import CourseRepository, ModuleRepository
from mentor_app.infrastructure.database import DatabaseService


class MentorService:
    def __init__(self, db_service: Optional[DatabaseService] = None):
        self.db_service = db_service or DatabaseService()
        self.architect = ArchitectService()
        self.builder = ContentGenerator()
        self.course_repo = CourseRepository(self.db_service)
        self.module_repo = ModuleRepository(self.db_service)
    
    def create_course_syllabus(self, topic: str, user_instructions: Optional[str] = None, user_context: Optional[UserContext] = None) -> tuple[CoursePlan, str]:
        """Create course syllabus using architect and persist it."""
        course_plan = self.architect.create_syllabus(topic, user_instructions, user_context)
        course_id = self.course_repo.save_course_plan(course_plan)
        return course_plan, course_id
    
    def create_module(self, course_id: str, module_id: str, user_context: Optional[UserContext] = None) -> tuple[ModuleContent, str]:
        """Create module content using builder and persist it."""
        # Get the specific module from database
        with self.db_service.get_session() as session:
            db_module = session.query(DBModule).filter(DBModule.course_id == course_id and DBModule.id == module_id).first()
            if not db_module:
                raise ValueError(f"Module {module_id} not found")
            
            # Get course for context
            course = self.course_repo.get_course(course_id)
            if not course:
                raise ValueError(f"Course {db_module.course_id} not found")
        
        # Create course context
        course_context = CourseContext(
            course_title=course.course_title,
            difficulty_level=course.difficulty_level,
            topic_domain="general"  # Default value
        )

        # 1) generate module structure with lessons if not already present
        db_module = self.architect.generate_module_structure(db_module, course_context)

        # 2) generate module content by the structure generated earlier
        module_content = self.builder.generate_module_content(db_module, course_context, user_context)
        content_id = self.module_repo.save_module_content(course_id, module_id, module_content)
        return module_content, content_id
