# LearnSmith API Documentation

## Base URL
`http://localhost:8000/api/v1`

## Authentication
All endpoints require authentication via Bearer token in the Authorization header.

---

## Course Management

### Create Course
**POST** `/courses`

Creates a new course with syllabus generation.

**Request Body:**
```json
{
  "topic": "Advanced SQL",
  "user_instructions": "Focus on performance optimization and complex joins",
  "user_context": {
    "skill_level": "intermediate",
    "learning_style": "hands-on",
    "time_commitment": 8,
    "prior_knowledge": ["basic SQL", "database design"]
  }
}
```

**Response:** `201 Created`
```json
{
  "id": "course_123",
  "course_title": "Advanced SQL",
  "estimated_duration": 40,
  "difficulty_level": "intermediate",
  "prerequisites": ["Basic SQL", "Database Fundamentals"],
  "modules": [
    {
      "id": "mod_1",
      "title": "Complex Joins",
      "description": "Master advanced join techniques",
      "learning_objectives": ["Understand inner/outer joins", "Apply self-joins"],
      "estimated_duration": 8,
      "dependencies": []
    }
  ],
  "created_at": "2025-12-24T17:10:21Z"
}
```

### Get Course
**GET** `/courses/{course_id}`

Retrieves course details and complete structure including lessons if they have been generated.

**Response:** `200 OK`
```json
{
  "id": "course_123",
  "course_title": "Advanced SQL",
  "estimated_duration": 40,
  "difficulty_level": "intermediate",
  "prerequisites": ["Basic SQL"],
  "modules": [
    {
      "id": "mod_1",
      "title": "Complex Joins",
      "description": "Master advanced join techniques",
      "learning_objectives": ["Understand inner/outer joins", "Apply self-joins"],
      "estimated_duration": 8,
      "dependencies": [],
      "lessons": [
        {
          "id": "lesson_1",
          "title": "Inner vs Outer Joins",
          "type": "theory",
          "key_concepts": ["JOIN types", "NULL handling"],
          "difficulty": "intermediate"
        }
      ]
    }
  ],
  "progress": {
    "completed_modules": 1,
    "total_modules": 4,
    "completion_percentage": 25
  }
}
```

### Delete Course
**DELETE** `/courses/{course_id}`

Permanently removes a course and all associated content.

**Response:** `204 No Content`

---

## Module Management

### Create Module
**POST** `/courses/{course_id}/modules`

Generates detailed content for a module from its outline.

**Request Body:**
```json
{
  "module_outline": {
    "id": "mod_1",
    "title": "Complex Joins",
    "description": "Master advanced join techniques",
    "learning_objectives": ["Understand inner/outer joins"],
    "estimated_duration": 8,
    "dependencies": [],
    "lessons": [
      {
        "id": "lesson_1",
        "title": "Inner vs Outer Joins",
        "type": "theory",
        "key_concepts": ["JOIN types", "NULL handling"],
        "difficulty": "intermediate"
      }
    ]
  }
}
```

**Response:** `201 Created`
```json
{
  "module_id": "mod_1",
  "title": "Complex Joins",
  "description": "Master advanced join techniques",
  "learning_objectives": ["Understand inner/outer joins"],
  "estimated_duration": 8,
  "lessons": [
    {
      "id": "lesson_1",
      "title": "Inner vs Outer Joins",
      "type": "theory",
      "content_markdown": "# Inner vs Outer Joins\n\nJoins are fundamental...",
      "key_concepts": ["JOIN types", "NULL handling"],
      "difficulty": "intermediate",
      "code_examples": [
        {
          "language": "sql",
          "code": "SELECT * FROM users u INNER JOIN orders o ON u.id = o.user_id",
          "explanation": "Basic inner join example",
          "is_runnable": true
        }
      ],
      "interactive_elements": [
        {
          "type": "quiz",
          "content": {
            "question": "What happens with unmatched rows in INNER JOIN?",
            "options": ["Included with NULLs", "Excluded", "Error thrown"],
            "correct": 1
          },
          "validation_logic": "answer === 1"
        }
      ],
      "practice_tasks": [
        {
          "id": "task_1",
          "title": "Write an INNER JOIN",
          "description": "Join users and orders tables",
          "task_type": "sql",
          "starter_code": "SELECT * FROM users u",
          "solution": "SELECT * FROM users u INNER JOIN orders o ON u.id = o.user_id",
          "test_cases": [
            {
              "input_data": "users: [(1,'John'), (2,'Jane')], orders: [(1,1,'book')]",
              "expected_output": "[(1,'John',1,'book')]",
              "description": "Basic join test"
            }
          ],
          "hints": ["Use INNER JOIN keyword", "Match on user_id"]
        }
      ],
      "estimated_duration": 45
    }
  ],
  "module_assessment": {
    "id": "assess_1",
    "title": "Complex Joins Assessment",
    "questions": [
      {
        "id": "q1",
        "type": "multiple_choice",
        "question_text": "Which JOIN returns all rows from both tables?",
        "options": ["INNER", "LEFT", "RIGHT", "FULL OUTER"],
        "correct_answer": "FULL OUTER",
        "explanation": "FULL OUTER JOIN returns all rows from both tables",
        "points": 10
      }
    ],
    "passing_score": 70,
    "time_limit": 30
  }
}
```

### Get Module
**GET** `/modules/{module_id}`

Retrieves complete module content including all lessons.

**Response:** `200 OK` - Same structure as Create Module response

### Delete Module
**DELETE** `/modules/{module_id}`

Removes module and all associated lessons.

**Response:** `204 No Content`

---

## Lesson Management

### Create Lesson
**POST** `/modules/{module_id}/lessons`

Generates detailed lesson content from outline.

**Request Body:**
```json
{
  "lesson_outline": {
    "id": "lesson_1",
    "title": "Inner vs Outer Joins",
    "type": "theory",
    "key_concepts": ["JOIN types", "NULL handling"],
    "difficulty": "intermediate"
  }
}
```

**Response:** `201 Created` - Returns LessonContent structure from Create Module

### Get Lesson
**GET** `/lessons/{lesson_id}`

Retrieves complete lesson content.

**Response:** `200 OK`
```json
{
  "id": "lesson_1",
  "title": "Inner vs Outer Joins",
  "type": "theory",
  "content_markdown": "# Inner vs Outer Joins...",
  "key_concepts": ["JOIN types", "NULL handling"],
  "difficulty": "intermediate",
  "code_examples": [...],
  "interactive_elements": [...],
  "practice_tasks": [...],
  "estimated_duration": 45,
  "progress": {
    "theory_read": false,
    "practice_completed": false,
    "assessment_submitted": false,
    "score": null
  }
}
```

### Delete Lesson
**DELETE** `/lessons/{lesson_id}`

Removes lesson content.

**Response:** `204 No Content`

---

## Progress Tracking

### Mark Lesson Theory as Read
**POST** `/lessons/{lesson_id}/theory/complete`

Marks the theory portion of a lesson as read.

**Response:** `200 OK`
```json
{
  "lesson_id": "lesson_1",
  "theory_read": true,
  "completed_at": "2025-12-24T17:15:30Z"
}
```

### Mark Lesson Practice as Complete
**POST** `/lessons/{lesson_id}/practice/complete`

Marks all practice tasks in a lesson as completed.

**Request Body:**
```json
{
  "task_results": [
    {
      "task_id": "task_1",
      "user_solution": "SELECT * FROM users u INNER JOIN orders o ON u.id = o.user_id",
      "passed": true,
      "score": 100
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "lesson_id": "lesson_1",
  "practice_completed": true,
  "overall_score": 95,
  "completed_at": "2025-12-24T17:20:15Z"
}
```

### Submit Lesson Assessment
**POST** `/lessons/{lesson_id}/assessment/submit`

Submits assessment answers for grading.

**Request Body:**
```json
{
  "answers": [
    {
      "question_id": "q1",
      "answer": "FULL OUTER"
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "lesson_id": "lesson_1",
  "assessment_submitted": true,
  "score": 85,
  "passed": true,
  "feedback": [
    {
      "question_id": "q1",
      "correct": true,
      "explanation": "FULL OUTER JOIN returns all rows from both tables"
    }
  ],
  "submitted_at": "2025-12-24T17:25:45Z"
}
```

---

## Navigation

### Get Next Module
**GET** `/courses/{course_id}/next-module`

Returns the next available module based on dependencies and progress.

**Response:** `200 OK`
```json
{
  "module_id": "mod_2",
  "title": "Window Functions",
  "description": "Learn advanced window functions",
  "is_available": true,
  "prerequisites_met": true,
  "dependencies_completed": ["mod_1"]
}
```

**Response:** `204 No Content` - When no next module available

### Get Next Lesson
**GET** `/modules/{module_id}/next-lesson`

Returns the next lesson in the module sequence.

**Response:** `200 OK`
```json
{
  "lesson_id": "lesson_2",
  "title": "Self Joins",
  "type": "practice",
  "is_available": true,
  "previous_lesson_completed": true
}
```

**Response:** `204 No Content` - When no next lesson available

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "InvalidTopicError",
  "message": "Topic 'invalid_topic' is not supported",
  "details": {
    "supported_topics": ["SQL", "Python", "JavaScript"]
  }
}
```

### 404 Not Found
```json
{
  "error": "ResourceNotFound",
  "message": "Course with id 'course_123' not found"
}
```

### 422 Unprocessable Entity
```json
{
  "error": "ValidationError",
  "message": "Invalid request data",
  "details": [
    {
      "field": "skill_level",
      "message": "Must be one of: beginner, intermediate, advanced"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "error": "GenerationError",
  "message": "Failed to generate course content",
  "details": {
    "retry_after": 30
  }
}
```
