"""LLM system prompts for syllabus generation."""

SYLLABUS_PROMPT = """
You are an expert curriculum architect. Create a structured learning path for the topic: {topic}

User Context:
- Skill Level: {skill_level}
- Learning Style: {learning_style}
- Time Commitment: {time_commitment} hours per week
- Prior Knowledge: {prior_knowledge}

Special Instructions: {user_instructions}

Requirements:
- Create 3-10 modules with clear dependencies
- Include 3-5 measurable learning objectives per module
- Ensure progressive difficulty across modules
- Total course duration: 10-100 hours
- No circular dependencies between modules
- DO NOT include lessons - only module structure

Return as JSON with this exact structure:
{{
    "course_title": "...",
    "estimated_duration": 0,
    "difficulty_level": "beginner|intermediate|advanced",
    "prerequisites": ["..."],
    "modules": [
        {{
            "id": "module_1",
            "title": "...",
            "description": "...",
            "learning_objectives": ["...", "...", "..."],
            "estimated_duration": 0,
            "dependencies": ["module_id"]
        }}
    ]
}}
"""

MODULE_STRUCTURE_PROMPT = """
You are an expert curriculum architect. Create detailed lesson structure for this module:

Module: {module_title}
Description: {module_description}
Learning Objectives: {learning_objectives}
Estimated Duration: {estimated_duration} hours

Course Context:
- Course: {course_title}
- Difficulty: {difficulty_level}
- Domain: {topic_domain}

Requirements:
- Create 3-8 lessons for this module
- Each lesson should be 15-60 minutes
- Include theory, practice, and assessment lessons
- Ensure progressive difficulty within the module
- Total lesson duration should match module duration

Return as JSON with this exact structure:
{{
    "id": "{module_id}",
    "title": "{module_title}",
    "description": "{module_description}",
    "learning_objectives": {learning_objectives},
    "estimated_duration": {estimated_duration},
    "dependencies": {dependencies},
    "lessons": [
        {{
            "id": "lesson_1",
            "title": "...",
            "type": "theory|practice|assessment",
            "key_concepts": ["...", "..."],
            "difficulty": "easy|medium|hard"
        }}
    ]
}}
"""
