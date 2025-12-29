"""Database models for PostgreSQL persistence."""

from sqlalchemy import Column, String, Integer, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(String, primary_key=True)
    course_title = Column(String, nullable=False)
    estimated_duration = Column(Integer, nullable=False)
    difficulty_level = Column(String, nullable=False)
    prerequisites = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"
    
    id = Column(String, primary_key=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    learning_objectives = Column(JSON, nullable=False)
    estimated_duration = Column(Integer, nullable=False)
    dependencies = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(String, primary_key=True)
    module_id = Column(String, ForeignKey("modules.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    key_concepts = Column(JSON, nullable=False)
    difficulty = Column(String, nullable=False)
    content_markdown = Column(Text)
    estimated_duration = Column(Integer)
    code_examples = Column(JSON)
    interactive_elements = Column(JSON)
    practice_tasks = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    module = relationship("Module", back_populates="lessons")
