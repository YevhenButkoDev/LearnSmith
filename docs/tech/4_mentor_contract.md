# Mentor Module - Technical Contract

## Overview
The Mentor module is the main orchestrator that coordinates learning experiences through natural language interaction. It contains an AI agent that communicates with users, creates courses via Architect/Builder services, and persists data using Infrastructure services.

## Core Function: `process_user_query`

### Input Contract
```python
def process_user_query(
    user_id: str,
    query: str,
    session_context: Optional[SessionContext] = None
) -> MentorResponse
```

**Parameters:**
- `user_id` (str): Unique identifier for the user
- `query` (str): Natural language input from user
- `session_context` (Optional[SessionContext]): Current conversation and learning context

**SessionContext Schema:**
```python
class SessionContext(BaseModel):
    session_id: str
    current_course_id: Optional[str]
    current_module_id: Optional[str]
    current_lesson_id: Optional[str]
    conversation_history: List[Message]
    user_preferences: UserContext
    
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
```

### Output Contract
```python
class MentorResponse(BaseModel):
    response_text: str
    response_type: str  # "answer", "course_created", "lesson_delivered", "clarification_needed"
    actions_taken: List[Action]
    next_suggestions: List[str]
    updated_context: SessionContext
    
class Action(BaseModel):
    type: str  # "course_created", "module_generated", "progress_updated"
    resource_id: str
    details: dict
```

## AI Agent Tools (Adapter Functions)

### Course Creation Adapter
```python
def create_course_with_persistence(
    topic: str,
    user_instructions: Optional[str] = None,
    user_context: Optional[UserContext] = None,
    user_id: str
) -> CourseCreationResult
```

**Functionality:**
1. Calls `architect.create_syllabus()` to generate course plan
2. Persists course structure via `infrastructure.course_repository.save()`
3. Returns course ID and summary for AI agent

**Output:**
```python
class CourseCreationResult(BaseModel):
    course_id: str
    course_title: str
    modules_count: int
    estimated_duration: int
    success: bool
    error_message: Optional[str]
```

### Module Content Generation Adapter
```python
def generate_module_with_persistence(
    module_outline: Module,
    course_context: CourseContext,
    user_context: Optional[UserContext] = None
) -> ModuleGenerationResult
```

**Functionality:**
1. Calls `builder.generate_module_content()` to create detailed content
2. Persists module content via `infrastructure.content_repository.save()`
3. Returns module ID and generation status

**Output:**
```python
class ModuleGenerationResult(BaseModel):
    module_id: str
    lessons_generated: int
    content_ready: bool
    success: bool
    error_message: Optional[str]
```

### Progress Tracking Adapter
```python
def update_user_progress(
    user_id: str,
    lesson_id: str,
    progress_type: str,  # "theory_read", "practice_completed", "assessment_submitted"
    data: dict
) -> ProgressUpdateResult
```

**Functionality:**
1. Updates progress via `infrastructure.progress_repository.update()`
2. Calculates next recommendations
3. Returns updated progress state

### Course Retrieval Adapter
```python
def get_user_courses(user_id: str) -> List[CourseInfo]
def get_course_progress(user_id: str, course_id: str) -> CourseProgress
def get_next_content(user_id: str, course_id: str) -> NextContentRecommendation
```

## AI Agent Prompt Template

### System Prompt
```
You are LearnSmith, an AI learning mentor. You help users create personalized courses and guide them through interactive learning experiences.

Available Tools:
- create_course_with_persistence: Create new courses on any topic
- generate_module_with_persistence: Generate detailed content for course modules
- update_user_progress: Track learning progress
- get_user_courses: Retrieve user's courses
- get_course_progress: Check progress on specific course
- get_next_content: Get next recommended lesson/module

Guidelines:
- Always respond in a helpful, encouraging tone
- Ask clarifying questions when user requests are ambiguous
- Suggest next steps based on user's current progress
- Provide specific, actionable guidance
- Use tools to create courses and track progress automatically
```

### User Query Processing Logic
```python
def _process_query_with_ai(query: str, context: SessionContext) -> MentorResponse:
    """
    AI agent processes user query and decides which tools to use
    
    Query Types:
    - Course creation: "I want to learn Python"
    - Progress questions: "What should I do next?"
    - Content questions: "Explain SQL joins"
    - Navigation: "Show my courses"
    """
```

## Business Rules

**Course Creation:**
- Automatically generate first module content after course creation
- Store user preferences for future course customization
- Suggest related topics based on user's learning history

**Progress Management:**
- Track completion timestamps for analytics
- Unlock next content based on dependencies
- Provide personalized recommendations

**Session Management:**
- Maintain conversation context across interactions
- Store user preferences and learning patterns
- Handle session timeouts gracefully

**Error Handling:**
- Graceful degradation when services are unavailable
- Retry logic for transient failures
- Clear error messages to users

## Integration Points

**Dependencies:**
- Architect Service (course planning)
- Builder Service (content generation)
- Infrastructure Services (persistence, LLM client)
- Auditor Service (analytics and recommendations)

**External Interfaces:**
- REST API endpoints for web/mobile clients
- WebSocket for real-time chat interface
- Event publishing for analytics

## Example Usage Scenarios

### Scenario 1: New Course Creation
```
User: "I want to learn advanced SQL with focus on performance"
AI Agent: 
1. Calls create_course_with_persistence()
2. Generates first module content
3. Responds: "I've created an Advanced SQL course for you! Let's start with Module 1: Query Optimization Fundamentals. Ready to begin?"
```

### Scenario 2: Progress Inquiry
```
User: "What should I study next?"
AI Agent:
1. Calls get_course_progress()
2. Calls get_next_content()
3. Responds: "You've completed 3 lessons in SQL Joins. Next up is 'Self-Joins and Recursive Queries' - this builds on what you just learned!"
```

### Scenario 3: Content Question
```
User: "I don't understand window functions"
AI Agent:
1. Checks current lesson context
2. Provides explanation based on user's current level
3. Suggests practice exercises or review materials
```

## Performance Requirements
- Response time: < 3 seconds for simple queries
- Support concurrent user sessions
- Cache frequently accessed course data
- Async processing for content generation

## Error Handling
- `ServiceUnavailableError`: When Architect/Builder services are down
- `ContentGenerationError`: When AI content generation fails
- `PersistenceError`: When database operations fail
- `InvalidQueryError`: When user query cannot be processed

## Validation Rules
- User ID must be valid and authenticated
- Session context must be consistent
- Tool calls must include required parameters
- Generated content must pass validation before persistence
