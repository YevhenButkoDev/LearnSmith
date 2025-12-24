from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class UserContext(BaseModel):
    skill_level: str
    learning_style: str
    time_commitment: int
    prior_knowledge: List[str]


class CourseContext(BaseModel):
    course_title: str
    difficulty_level: str
    topic_domain: str
    user_instructions: Optional[str] = None


class LessonOutline(BaseModel):
    id: str
    title: str
    type: str
    key_concepts: List[str]
    difficulty: str


class Module(BaseModel):
    id: str
    title: str
    description: str
    learning_objectives: List[str]
    estimated_duration: int
    dependencies: List[str]
    lessons: List[LessonOutline]


class CodeExample(BaseModel):
    language: str
    code: str
    explanation: str
    is_runnable: bool


class InteractiveElement(BaseModel):
    type: str
    content: Dict[str, Any]
    validation_logic: str


class TestCase(BaseModel):
    input_data: str
    expected_output: str
    description: str


class PracticeTask(BaseModel):
    id: str
    title: str
    description: str
    task_type: str
    starter_code: Optional[str]
    solution: str
    test_cases: List[TestCase]
    hints: List[str]


class Question(BaseModel):
    id: str
    type: str
    question_text: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str
    points: int


class Assessment(BaseModel):
    id: str
    title: str
    questions: List[Question]
    passing_score: int
    time_limit: Optional[int] = None


class LessonContent(BaseModel):
    id: str
    title: str
    type: str
    content_markdown: str
    key_concepts: List[str]
    difficulty: str
    code_examples: List[CodeExample]
    interactive_elements: List[InteractiveElement]
    practice_tasks: List[PracticeTask]
    estimated_duration: int


class ModuleContent(BaseModel):
    module_id: str
    title: str
    description: str
    learning_objectives: List[str]
    estimated_duration: int
    lessons: List[LessonContent]
    module_assessment: Optional[Assessment] = None


class ContentGenerationError(Exception):
    pass


class CodeValidationError(Exception):
    pass


class InvalidModuleError(Exception):
    pass
