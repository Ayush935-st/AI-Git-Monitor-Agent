from backend.services.llm_services import LLMService
from backend.utils.logger import logger


class ReviewAgent:
    """
    AI Agent responsible for reviewing Git code changes.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def build_prompt(self, git_diff: str) -> str:
        """
        Build a structured prompt for AI code review.
        """

        return f"""
You are a Senior Software Engineer.

Review the following Git diff and provide:

1. Code Quality
2. Security Issues
3. Performance Issues
4. Maintainability
5. Best Practices
6. Complexity
7. Risk Level (Low/Medium/High)
8. Recommendations
9. Overall Score (/10)

Git Diff:
{git_diff}
"""

    def review_code(self, git_diff: str) -> str:
        """
        Generate AI review.
        """

        logger.info("Generating AI code review...")

        prompt = self.build_prompt(git_diff)

        response = self.llm_service.generate_response(prompt)

        logger.info("AI review completed.")

        return response