"""Main coordinator - orchestrates the learning process."""

from mentor_app.architect.service import ArchitectService

class MentorCoordinator:
    def __init__(self, architect: ArchitectService, repo):
        self.architect = architect
        self.repo = repo
    
    def start_new_journey(self, user_id: str, topic: str):
        """Initialize a new learning journey for a user."""
        plan = self.architect.create_syllabus(topic)
        self.repo.save_course(user_id, plan)
        return f"Course for {topic} is ready!"
    
    def get_next_lesson(self, user_id: str):
        """Get the next lesson for the user."""
        pass
    
    def process_user_response(self, user_id: str, response: str):
        """Process user's answer and determine next action."""
        pass
