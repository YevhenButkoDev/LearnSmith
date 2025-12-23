# Builder Module - Technical Contract

## Overview
The Builder module is responsible for generating detailed lesson content from module outlines. It transforms high-level lesson plans into comprehensive educational materials with interactive elements.

## Core Function: `generate_module_content`

### Input Contract
```python
def generate_module_content(
    module: Module,
    course_context: CourseContext,
    user_context: Optional[UserContext] = None
) -> ModuleContent
```

**Parameters:**
- `module` (Module): Module outline from Architect (contains lesson outlines, objectives, etc.)
- `course_context` (CourseContext): Overall course information and context
- `user_context` (Optional[UserContext]): User's learning preferences and background

**CourseContext Schema:**
```python
class CourseContext(BaseModel):
    course_title: str
    difficulty_level: str
    topic_domain: str  # "programming", "data", "web", etc.
    user_instructions: Optional[str]  # custom instructions from user
```

### Output Contract
```python
class ModuleContent(BaseModel):
    module_id: str
    title: str
    description: str
    learning_objectives: List[str]
    estimated_duration: int
    lessons: List[LessonContent]
    module_assessment: Optional[Assessment]

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

class CodeExample(BaseModel):
    language: str
    code: str
    explanation: str
    is_runnable: bool

class InteractiveElement(BaseModel):
    type: str  # "quiz", "drag_drop", "fill_blank", "code_challenge"
    content: dict  # flexible structure based on type
    validation_logic: str

class PracticeTask(BaseModel):
    id: str
    title: str
    description: str
    task_type: str  # "coding", "sql", "design", "analysis"
    starter_code: Optional[str]
    solution: str
    test_cases: List[TestCase]
    hints: List[str]

class TestCase(BaseModel):
    input_data: str
    expected_output: str
    description: str

class Assessment(BaseModel):
    id: str
    title: str
    questions: List[Question]
    passing_score: int  # percentage
    time_limit: Optional[int]  # minutes

class Question(BaseModel):
    id: str
    type: str  # "multiple_choice", "code", "short_answer"
    question_text: str
    options: Optional[List[str]]  # for multiple choice
    correct_answer: str
    explanation: str
    points: int
```

### Business Rules

**Content Generation:**
- Theory lessons must include clear explanations with examples
- Practice lessons must have hands-on exercises
- Assessment lessons must test understanding of key concepts
- Content must match specified difficulty level

**Code Examples:**
- Include working, tested code snippets
- Provide clear explanations for each example
- Mark examples as runnable when appropriate
- Use consistent coding style and best practices

**Interactive Elements:**
- Each lesson should have 2-4 interactive elements
- Mix different interaction types for engagement
- Include immediate feedback mechanisms
- Validate user responses appropriately

**Practice Tasks:**
- Provide progressive difficulty within lessons
- Include starter code when helpful
- Offer 2-3 hints without giving away solution
- Include comprehensive test cases

### Error Handling
- Invalid module structure: Return `InvalidModuleError`
- Content generation failure: Return `ContentGenerationError`
- Code compilation errors: Return `CodeValidationError`

### Performance Requirements
- Response time: < 30 seconds per module
- Cache generated content for reuse
- Validate all code examples before output
- Support concurrent lesson generation

### Integration Points
- **Input from:** Architect module (Module outlines)
- **Output to:** Mentor module (lesson delivery), Database (content storage)
- **Dependencies:** LLM Client, Code Validator, Content Repository

### Example Usage
```python
builder = ContentGenerator(llm_client, code_validator)

course_context = CourseContext(
    course_title="Advanced SQL",
    difficulty_level="intermediate",
    topic_domain="data",
    user_instructions="Focus on performance optimization"
)

module_content = builder.generate_module_content(
    module=architect_module,
    course_context=course_context,
    user_context=user_context
)
```

### Validation Rules
- Each lesson must have content_markdown (min 500 words for theory)
- Practice lessons must include at least 1 practice task
- Code examples must be syntactically valid
- Interactive elements must have proper validation logic
- Assessment questions must have correct answers and explanations
