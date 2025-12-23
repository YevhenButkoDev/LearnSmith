# Architect Module - Technical Contract

## Overview
The Architect module is responsible for strategic course planning and curriculum design. It creates structured learning paths with logical dependencies and progressive difficulty.

## Core Function: `create_syllabus`

### Input Contract
```python
def create_syllabus(
    topic: str, 
    user_instructions: Optional[str] = None,
    user_context: Optional[UserContext] = None
) -> CoursePlan
```

**Parameters:**
- `topic` (str): The subject matter to create a course for (e.g., "SQL Basics", "Python OOP")
- `user_instructions` (Optional[str]): Natural language instructions for course customization (e.g., "focus more on advanced SQL joins and subqueries", "include real-world projects", "emphasize performance optimization")
- `user_context` (Optional[UserContext]): User's skill level, learning preferences, and background

**UserContext Schema:**
```python
class UserContext(BaseModel):
    skill_level: str  # "beginner", "intermediate", "advanced"
    learning_style: str  # "visual", "hands-on", "theoretical"
    time_commitment: int  # hours per week
    prior_knowledge: List[str]  # related topics user already knows
```

### Output Contract
```python
class CoursePlan(BaseModel):
    course_title: str
    estimated_duration: int  # total hours
    difficulty_level: str
    prerequisites: List[str]
    modules: List[Module]
    
class Module(BaseModel):
    id: str
    title: str
    description: str
    learning_objectives: List[str]
    estimated_duration: int  # hours
    dependencies: List[str]  # module IDs this depends on
    lessons: List[LessonOutline]
    
class LessonOutline(BaseModel):
    id: str
    title: str
    type: str  # "theory", "practice", "assessment"
    key_concepts: List[str]
    difficulty: str
```

### Business Rules

**Dependency Management:**
- Each module must declare its dependencies
- No circular dependencies allowed
- Foundation concepts must come before advanced topics

**Progressive Difficulty:**
- Lessons within a module progress from basic to advanced
- Each module builds upon previous modules
- Difficulty curve should be smooth, not steep

**Learning Objectives:**
- Each module must have 3-5 clear learning objectives
- Objectives must be measurable and specific
- Must align with overall course goals

### Error Handling
- Invalid topic: Return `InvalidTopicError`
- Conflicting user context: Return `ContextConflictError`
- LLM generation failure: Return `GenerationError`

### Performance Requirements
- Response time: < 10 seconds for standard topics
- Cache frequently requested topics
- Fallback to template-based generation if LLM fails

### Integration Points
- **Input from:** Mentor module (user requests)
- **Output to:** Builder module (lesson generation), Database (course storage)
- **Dependencies:** LLM Client, Course Repository

### Example Usage
```python
architect = ArchitectService(llm_client)
user_context = UserContext(
    skill_level="intermediate",
    learning_style="hands-on",
    time_commitment=8,
    prior_knowledge=["basic SQL", "database design"]
)

# Example with custom instructions
course_plan = architect.create_syllabus(
    topic="Advanced SQL",
    user_instructions="Focus heavily on complex joins, window functions, and query optimization. Include performance tuning exercises with real datasets.",
    user_context=user_context
)
```

**User Instructions Examples:**
- "Include more practical projects and less theory"
- "Focus on industry best practices and real-world scenarios"
- "Add extra depth to error handling and debugging techniques"
- "Emphasize security considerations throughout the course"
- "Include comparisons with alternative technologies"

### Validation Rules
- Course must have 3-10 modules
- Each module must have 3-8 lessons
- Total estimated duration: 10-100 hours
- All dependencies must reference existing modules
