#!/usr/bin/env python3
"""Test script to combine Architect and Builder services with persistence."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv
from mentor_app.architect.service import ArchitectService
from mentor_app.builder.service import ContentGenerator
from mentor_app.models import UserContext, CourseContext
from mentor_app.infrastructure.database import DatabaseService
from mentor_app.infrastructure.repositories import CourseRepository, ModuleRepository


def main():
    """Test Architect + Builder integration with persistence."""
    load_dotenv()
    
    print("🏗️  Testing Architect + Builder + Persistence Integration")
    print("=" * 60)
    
    # Initialize services
    architect = ArchitectService()
    builder = ContentGenerator()
    
    # Initialize database
    db_service = DatabaseService()
    db_service.create_tables()
    
    course_repo = CourseRepository(db_service)
    module_repo = ModuleRepository(db_service)
    
    # User context
    user_context = UserContext(
        skill_level="intermediate",
        learning_style="hands-on",
        time_commitment=8,
        prior_knowledge=["basic SQL", "database design"]
    )
    
    print("📋 Step 1: Generating course syllabus with Architect...")
    
    # Generate course plan
    course_plan = architect.create_syllabus(
        topic="Advanced SQL",
        user_instructions="Focus on complex joins, window functions, and performance optimization",
        user_context=user_context
    )
    
    print(f"✅ Generated course: {course_plan.course_title}")
    print(f"📚 Modules: {len(course_plan.modules)}")
    print(f"⏱️  Duration: {course_plan.estimated_duration} hours")
    
    print("\n💾 Step 2: Persisting course plan to PostgreSQL...")
    
    # Save course plan
    course_id = course_repo.save_course_plan(course_plan)
    print(f"✅ Saved course to database with ID: {course_id}")
    
    # Show modules
    print(f"\n📖 Course Modules:")
    for i, module in enumerate(course_plan.modules, 1):
        print(f"  {i}. {module.title} ({len(module.lessons)} lessons)")
    
    print("\n🔨 Step 3: Generating detailed content with Builder...")
    
    # Course context for builder
    course_context = CourseContext(
        course_title=course_plan.course_title,
        difficulty_level=course_plan.difficulty_level,
        topic_domain="data",
        user_instructions="Focus on complex joins, window functions, and performance optimization"
    )
    
    # Generate content for first module
    first_module = course_plan.modules[0]
    print(f"🎯 Generating content for: {first_module.title}")
    
    module_content = builder.generate_module_content(
        module=first_module,
        course_context=course_context,
        user_context=user_context
    )
    
    print(f"✅ Generated detailed content for {len(module_content.lessons)} lessons")
    
    print("\n💾 Step 4: Persisting module content to PostgreSQL...")
    
    # Save module content
    module_id = module_repo.save_module_content(module_content)
    print(f"✅ Saved module content to database: {module_id}")
    
    print(f"\n📊 Final Results:")
    print(f"  🗄️  Course ID: {course_id}")
    print(f"  📚 Modules: {len(course_plan.modules)} (1 with detailed content)")
    print(f"  📖 Lessons: {sum(len(m.lessons) for m in course_plan.modules)} total")
    print(f"  💾 Content: {sum(len(l.content_markdown or '') for l in module_content.lessons)} characters")
    
    # Show lesson details
    print(f"\n📄 Generated Lesson Content:")
    for lesson in module_content.lessons:
        print(f"  - {lesson.title} ({lesson.estimated_duration} min)")
        content_preview = lesson.content_markdown[:100].replace('\n', ' ') if lesson.content_markdown else "No content"
        print(f"    Preview: {content_preview}...")
    
    print("\n🎉 Full integration test completed successfully!")
    print("✅ Course planned, content generated, and data persisted to PostgreSQL")


if __name__ == "__main__":
    main()
