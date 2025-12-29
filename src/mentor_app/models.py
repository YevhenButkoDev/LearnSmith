"""Pydantic models for the AI Mentor application."""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# User Context Models
class UserContext(BaseModel):
    skill_level: str  # "beginner", "intermediate", "advanced"
    learning_style: str  # "visual", "hands-on", "theoretical"
    time_commitment: int  # hours per week
    prior_knowledge: List[str]  # related topics user already knows

# Architect Models
class LessonOutline(BaseModel):
    id: str
    title: str
    type: str  # "theory", "practice", "assessment"
    key_concepts: List[str]
    difficulty: str

class Module(BaseModel):
    id: str
    title: str
    description: str
    learning_objectives: List[str]
    estimated_duration: int  # hours
    dependencies: List[str]  # module IDs this depends on
    lessons: Optional[List[LessonOutline]] = None  # Only populated when detailed structure is generated

class CoursePlan(BaseModel):
    course_title: str
    estimated_duration: int  # total hours
    difficulty_level: str
    prerequisites: List[str]
    modules: List[Module]

# Builder Models
class CourseContext(BaseModel):
    course_title: str
    difficulty_level: str
    topic_domain: str  # "programming", "data", "web", etc.
    user_instructions: Optional[str] = None  # custom instructions from user

class CodeExample(BaseModel):
    language: str
    code: str
    explanation: str
    is_runnable: bool

class InteractiveElement(BaseModel):
    type: str  # "quiz", "drag_drop", "fill_blank", "code_challenge"
    content: Dict[str, Any]  # flexible structure based on type
    validation_logic: str

class TestCase(BaseModel):
    input_data: str
    expected_output: str
    description: str

class PracticeTask(BaseModel):
    id: str
    title: str
    description: str
    task_type: str  # "coding", "sql", "design", "analysis"
    starter_code: Optional[str] = None
    solution: str
    test_cases: List[TestCase]
    hints: List[str]

class LessonContent(BaseModel):
    id: str
    title: str
    type: str  # "theory", "practice", "assessment"
    content_markdown: str  # main lesson content
    key_concepts: List[str]
    difficulty: str
    code_examples: List[CodeExample]
    interactive_elements: List[InteractiveElement]
    practice_tasks: List[PracticeTask]
    estimated_duration: int  # minutes

class Question(BaseModel):
    id: str
    type: str  # "multiple_choice", "code", "short_answer"
    question_text: str
    options: Optional[List[str]] = None  # for multiple choice
    correct_answer: str
    explanation: str
    points: int

class Assessment(BaseModel):
    id: str
    title: str
    questions: List[Question]
    passing_score: int  # percentage
    time_limit: Optional[int] = None  # minutes

class ModuleContent(BaseModel):
    module_id: str
    title: str
    description: str
    learning_objectives: List[str]
    estimated_duration: int
    lessons: List[LessonContent]
    module_assessment: Optional[Assessment] = None
