"""Repository services for data persistence."""

import uuid
from typing import List, Optional
from mentor_app.models import CoursePlan, Module as PydanticModule
from mentor_app.builder.models import ModuleContent, LessonContent
from .models import Course, Module, Lesson
from .models import Module as DBModule
from .database import DatabaseService


class CourseRepository:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    def save_course_plan(self, course_plan: CoursePlan) -> str:
        """Save course plan to database."""
        with self.db_service.get_session() as session:
            # Create course
            course = Course(
                id=str(uuid.uuid4()),
                course_title=course_plan.course_title,
                estimated_duration=course_plan.estimated_duration,
                difficulty_level=course_plan.difficulty_level,
                prerequisites=course_plan.prerequisites
            )
            session.add(course)
            
            # Create modules
            for module_data in course_plan.modules:
                module = Module(
                    id=module_data.id,
                    course_id=course.id,
                    title=module_data.title,
                    description=module_data.description,
                    learning_objectives=module_data.learning_objectives,
                    estimated_duration=module_data.estimated_duration,
                    dependencies=module_data.dependencies
                )
                session.add(module)
            
            session.commit()
            return course.id
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID."""
        with self.db_service.get_session() as session:
            return session.query(Course).filter(Course.id == course_id).first()


class ModuleRepository:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    def save_module_content(self, course_id: str, module_id: str, module_content: ModuleContent) -> str:
        """Save detailed module content to database."""
        with self.db_service.get_session() as session:

            # Create lessons with generated content
            for lesson_content in module_content.lessons:
                lesson = Lesson(
                    id=lesson_content.id,
                    module_id=module_id,
                    course_id=course_id,
                    title=lesson_content.title,
                    type=lesson_content.type,
                    key_concepts=lesson_content.key_concepts,
                    difficulty=lesson_content.difficulty,
                    content_markdown=lesson_content.content_markdown,
                    estimated_duration=lesson_content.estimated_duration,
                    code_examples=[ex.dict() for ex in lesson_content.code_examples] if lesson_content.code_examples else [],
                    interactive_elements=[ie.dict() for ie in lesson_content.interactive_elements] if lesson_content.interactive_elements else [],
                    practice_tasks=[pt.dict() for pt in lesson_content.practice_tasks] if lesson_content.practice_tasks else []
                )
                session.add(lesson)
            
            session.commit()
            return module_id
    
    def get_modules_by_course(self, course_id: str) -> List[Module]:
        """Get all modules for a course."""
        with self.db_service.get_session() as session:
            return session.query(Module).filter(Module.course_id == course_id).all()
    
    def get_module(self, module_id: str) -> Optional[Module]:
        """Get module by ID."""
        with self.db_service.get_session() as session:
            return session.query(Module).filter(Module.id == module_id).first()


class LessonRepository:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
    
    def get_lesson(self, lesson_id: str) -> Optional[Lesson]:
        """Get lesson by ID."""
        with self.db_service.get_session() as session:
            return session.query(Lesson).filter(Lesson.id == lesson_id).first()
    
    def get_lessons_by_module(self, module_id: str) -> List[Lesson]:
        """Get all lessons for a module."""
        with self.db_service.get_session() as session:
            return session.query(Lesson).filter(Lesson.module_id == module_id).all()
