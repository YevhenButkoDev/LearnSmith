"""Content generator for individual lessons."""

from ..models import Module, ModuleContent, CourseContext, UserContext

class ContentGenerator:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def generate_module_content(
        self,
        module: Module,
        course_context: CourseContext,
        user_context: UserContext = None
    ) -> ModuleContent:
        """Generate detailed module content from outline."""
        pass
