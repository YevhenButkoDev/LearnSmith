#!/usr/bin/env python3
"""Test script using MentorService for course creation."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv
from mentor_app.models import UserContext
from mentor_app.mentor.mentor_service import MentorService


def main():
    """Test MentorService integration."""
    load_dotenv()
    
    print("🏗️  Testing MentorService Integration")
    print("=" * 60)
    
    # Initialize mentor service
    mentor = MentorService()
    
    # User context
    user_context = UserContext(
        skill_level="intermediate",
        learning_style="hands-on",
        time_commitment=8,
        prior_knowledge=["basic SQL", "database design"]
    )
    
    print("📋 Step 1: Creating course syllabus...")
    
    # Create course syllabus
    course_plan, course_id = mentor.create_course_syllabus(
        topic="Advanced SQL",
        user_instructions="Focus on complex joins, window functions, and performance optimization",
        user_context=user_context
    )
    
    print(f"✅ Generated course: {course_plan.course_title}")
    print(f"📚 Modules: {len(course_plan.modules)}")
    print(f"⏱️  Duration: {course_plan.estimated_duration} hours")
    print(f"💾 Course ID: {course_id}")
    
    # Show modules
    print(f"\n📖 Course Modules:")
    for i, module in enumerate(course_plan.modules, 1):
        print(f"  {i}. {module.title} ({module.estimated_duration} hours)")
    
    print("\n🔨 Step 2: Creating detailed module content...")
    
    # Generate content for first module using its ID
    first_module_id = course_plan.modules[0].id
    print(f"🎯 Generating content for module: {course_plan.modules[0].title}")
    
    module_content, module_content_id = mentor.create_module(
        course_id=course_id,
        module_id=first_module_id,
        user_context=user_context
    )
    
    print(f"✅ Generated detailed content for {len(module_content.lessons)} lessons")
    print(f"💾 Module Content ID: {module_content_id}")
    
    print(f"\n📊 Final Results:")
    print(f"  🗄️  Course ID: {course_id}")
    print(f"  📚 Modules: {len(course_plan.modules)} (1 with detailed content)")
    print(f"  📖 Generated Lessons: {len(module_content.lessons)}")
    print(f"  💾 Content: {sum(len(l.content_markdown or '') for l in module_content.lessons)} characters")
    
    # Show lesson details
    print(f"\n📄 Generated Lesson Content:")
    for lesson in module_content.lessons:
        print(f"  - {lesson.title} ({lesson.estimated_duration} min)")
        content_preview = lesson.content_markdown[:100].replace('\n', ' ') if lesson.content_markdown else "No content"
        print(f"    Preview: {content_preview}...")
    
    print("\n🎉 MentorService integration test completed successfully!")
    print("✅ Course planned and content generated using MentorService")


if __name__ == "__main__":
    main()
