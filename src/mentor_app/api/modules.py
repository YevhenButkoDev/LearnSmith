"""Module API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from mentor_app.models import UserContext
from mentor_app.mentor.mentor_service import MentorService
from mentor_app.infrastructure.database import DatabaseService
from mentor_app.infrastructure.repositories import LessonRepository

router = APIRouter(prefix="/api/v1", tags=["modules"])

# Response models  
class ModuleResponse(BaseModel):
    module_id: str
    title: str
    description: str
    learning_objectives: list[str]
    estimated_duration: int
    lessons: list[dict]
    module_assessment: Optional[dict] = None

# Initialize services
db_service = DatabaseService()
mentor_service = MentorService(db_service)
lesson_repo = LessonRepository(db_service)

@router.post("/courses/{course_id}/modules/{module_id}", response_model=ModuleResponse, status_code=201)
async def create_module(course_id: str, module_id: str):
    """Generate detailed content for a module from its outline."""
    try:
        # Create dummy user context (will be loaded from DB in future)
        user_context = UserContext(
            skill_level="intermediate",
            learning_style="hands-on",
            time_commitment=8,
            prior_knowledge=["basic programming", "databases"]
        )
        
        # Create module content using mentor service
        module_content, content_id = mentor_service.create_module(
            course_id=course_id,
            module_id=module_id,
            user_context=user_context
        )
        
        # Convert lessons to response format
        lessons_response = []
        for lesson in module_content.lessons:
            lesson_dict = {
                "id": lesson.id,
                "title": lesson.title,
                "type": lesson.type,
                "content_markdown": lesson.content_markdown,
                "key_concepts": lesson.key_concepts,
                "difficulty": lesson.difficulty,
                "code_examples": [ex.dict() for ex in lesson.code_examples],
                "interactive_elements": [ie.dict() for ie in lesson.interactive_elements],
                "practice_tasks": [pt.dict() for pt in lesson.practice_tasks],
                "estimated_duration": lesson.estimated_duration
            }
            lessons_response.append(lesson_dict)
        
        return ModuleResponse(
            module_id=module_id,
            title=module_content.title,
            description=module_content.description,
            learning_objectives=module_content.learning_objectives,
            estimated_duration=module_content.estimated_duration,
            lessons=lessons_response,
            module_assessment=module_content.module_assessment.dict() if module_content.module_assessment else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create module: {str(e)}")

@router.get("/modules/{module_id}", response_model=ModuleResponse)
async def get_module(module_id: str):
    """Retrieve complete module content including all lessons."""
    try:
        # Get module from repository
        module = mentor_service.module_repo.get_module(module_id)
        if not module:
            raise HTTPException(status_code=404, detail=f"Module with id '{module_id}' not found")
        
        # Get lessons from repository
        lessons = lesson_repo.get_lessons_by_module(module_id)
        
        # Convert lessons to response format
        lessons_response = []
        for lesson in lessons:
            lesson_dict = {
                "id": lesson.id,
                "title": lesson.title,
                "type": lesson.type,
                "content_markdown": lesson.content_markdown or "",
                "key_concepts": lesson.key_concepts,
                "difficulty": lesson.difficulty,
                "code_examples": lesson.code_examples or [],
                "interactive_elements": lesson.interactive_elements or [],
                "practice_tasks": lesson.practice_tasks or [],
                "estimated_duration": lesson.estimated_duration or 0
            }
            lessons_response.append(lesson_dict)
        
        return ModuleResponse(
            module_id=module.id,
            title=module.title,
            description=module.description,
            learning_objectives=module.learning_objectives,
            estimated_duration=module.estimated_duration,
            lessons=lessons_response,
            module_assessment=None  # TODO: Add assessment retrieval if needed
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve module: {str(e)}")
