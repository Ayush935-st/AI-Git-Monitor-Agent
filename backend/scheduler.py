from apscheduler.schedulers.background import BackgroundScheduler

from backend.agents.git_monitor_agent import GitMonitorAgent
from backend.services.git_service import GitService
from backend.utils.logger import logger


class SchedulerService:
    """
    Handles scheduled execution of the Git Monitoring Agent.
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler()

        git_service = GitService("repositories/sample_repo")
        self.agent = GitMonitorAgent(git_service)

    def monitor_repository(self):
        """
        Periodically checks for new commits.
        """

        logger.info("Running scheduled Git monitoring...")

        try:
            self.agent.check_for_new_commit()

        except Exception as e:
            logger.exception(e)

    def start(self):
        """
        Start scheduler.
        """

        self.agent.initialize()

        self.scheduler.add_job(
            self.monitor_repository,
            trigger="interval",
            minutes=1,
            id="git_monitor_job",
            replace_existing=True,
        )

        self.scheduler.start()

        logger.info("Scheduler started.")