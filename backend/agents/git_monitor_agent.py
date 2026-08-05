from backend.services.git_service import GitService
from backend.utils.logger import logger


class GitMonitorAgent:
    """
    AI Agent responsible for monitoring Git repositories.
    """

    def __init__(self, git_service: GitService):
        self.git_service = git_service
        self.last_commit = None

    def initialize(self):
        """
        Initialize monitoring by loading the latest commit.
        """
        self.git_service.load_repository()
        self.last_commit = self.git_service.get_latest_commit().hexsha

        logger.info(f"Monitoring started from commit: {self.last_commit}")

    def check_for_new_commit(self):
        """
        Check whether a new commit has been pushed.
        """

        self.git_service.pull_latest_changes()

        latest_commit = self.git_service.get_latest_commit().hexsha

        if latest_commit != self.last_commit:

            logger.info(f"New commit detected: {latest_commit}")

            self.last_commit = latest_commit

            return latest_commit

        logger.info("No new commits found.")

        return None