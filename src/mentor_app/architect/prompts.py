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
- Each module should have 3-8 lessons
- Include 3-5 measurable learning objectives per module
- Ensure progressive difficulty within and across modules
- Total course duration: 10-100 hours
- No circular dependencies between modules

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
            "dependencies": ["module_id"],
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
    ]
}}
"""
