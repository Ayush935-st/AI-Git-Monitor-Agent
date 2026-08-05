from backend.config import settings
from backend.services.git_service import GitService
from backend.agents.review_agent import ReviewAgent
from backend.agents.report_agent import ReportAgent
from backend.agents.notification_agent import NotificationAgent
from backend.utils.logger import logger


class WebhookAgent:
    """
    Orchestrates the complete AI code review pipeline.
    """

    def __init__(self):
        self.git_service = GitService(settings.repo_path)
        self.review_agent = ReviewAgent()
        self.report_agent = ReportAgent()
        self.notification_agent = NotificationAgent()

    def process(self, payload: dict):

        logger.info("GitHub webhook received.")

        # Load repository
        self.git_service.load_repository()

        # Pull latest changes
        self.git_service.pull_latest_changes()

        # Latest commit
        latest_commit = self.git_service.get_latest_commit()

        # Changed files
        changed_files = self.git_service.get_changed_files()

        # Git diff
        git_diff = self.git_service.get_commit_diff()
        logger.info("Generating AI Review...")
        review = self.review_agent.review_code(git_diff)

        logger.info("Generating reports...")

        markdown_report = self.report_agent.generate_markdown(
            review,
            latest_commit.hexsha
        )

        pdf_report = self.report_agent.generate_pdf(
            review,
            latest_commit.hexsha
        )

        logger.info("Reports generated successfully.")
 

        return {
            "status": "success",
            "repository": payload.get("repository", {}).get("full_name"),
            "branch": payload.get("ref"),
            "latest_commit": latest_commit.hexsha,
            "changed_files": changed_files,
            "markdown_report": markdown_report,
            "pdf_report": pdf_report
        }