"""Pydantic models for course structure."""

from pydantic import BaseModel
from typing import List

class Lesson(BaseModel):
    title: str
    content_markdown: str
    key_concepts: List[str]
    task_prompt: str
    validation_logic: str

class Module(BaseModel):
    title: str
    objectives: List[str]
    lessons: List[str]

class CoursePlan(BaseModel):
    course_title: str
    modules: List[Module]
