"""Course API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from mentor_app.models import UserContext, Module
from mentor_app.mentor.mentor_service import MentorService
from mentor_app.infrastructure.database import DatabaseService
from mentor_app.infrastructure.repositories import LessonRepository

router = APIRouter(prefix="/api/v1", tags=["courses"])

# Request models
class CreateCourseRequest(BaseModel):
    topic: str
    user_instructions: Optional[str] = None
    user_context: Optional[UserContext] = None

# Response models
class CourseResponse(BaseModel):
    id: str
    course_title: str
    estimated_duration: int
    difficulty_level: str
    prerequisites: list[str]
    modules: list[Module]
    created_at: str

class CourseDetailResponse(CourseResponse):
    progress: Optional[dict] = None

# Initialize services
db_service = DatabaseService()
mentor_service = MentorService(db_service)
lesson_repo = LessonRepository(db_service)

@router.post("/courses", response_model=CourseResponse, status_code=201)
async def create_course(request: CreateCourseRequest):
    """Create a new course with syllabus generation."""
    try:
        # Generate course plan using mentor service
        course_plan, course_id = mentor_service.create_course_syllabus(
            topic=request.topic,
            user_instructions=request.user_instructions,
            user_context=request.user_context
        )

        return CourseResponse(
            id=course_id,
            course_title=course_plan.course_title,
            estimated_duration=course_plan.estimated_duration,
            difficulty_level=course_plan.difficulty_level,
            prerequisites=course_plan.prerequisites,
            modules=course_plan.modules,
            created_at=datetime.now().isoformat() + "Z"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create course: {str(e)}")

@router.get("/courses/{course_id}", response_model=CourseDetailResponse)
async def get_course(course_id: str):
    """Retrieve course details and complete structure including lessons if generated."""
    try:
        # Get course from repository
        course = mentor_service.course_repo.get_course(course_id)
        if not course:
            raise HTTPException(status_code=404, detail=f"Course with id '{course_id}' not found")
        
        # Get modules from repository
        modules = mentor_service.module_repo.get_modules_by_course(course_id)
        
        modules_with_lessons = []
        for module in modules:
            # Get lessons using lesson repository
            lessons = lesson_repo.get_lessons_by_module(module.id)
            
            module_dict = {
                "id": module.id,
                "title": module.title,
                "description": module.description,
                "learning_objectives": module.learning_objectives,
                "estimated_duration": module.estimated_duration,
                "dependencies": module.dependencies
            }
            
            if lessons:
                module_dict["lessons"] = [
                    {
                        "id": lesson.id,
                        "title": lesson.title,
                        "type": lesson.type,
                        "key_concepts": lesson.key_concepts,
                        "difficulty": lesson.difficulty
                    }
                    for lesson in lessons
                ]
            
            modules_with_lessons.append(Module(**module_dict))
        
        return CourseDetailResponse(
            id=course.id,
            course_title=course.course_title,
            estimated_duration=course.estimated_duration,
            difficulty_level=course.difficulty_level,
            prerequisites=course.prerequisites,
            modules=modules_with_lessons,
            created_at=course.created_at.isoformat() + "Z",
            progress={
                "completed_modules": 0,
                "total_modules": len(modules_with_lessons),
                "completion_percentage": 0
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve course: {str(e)}")
