from backend.config import settings
from backend.services.git_service import GitService
from backend.agents.report_agent import ReportAgent
from backend.agents.notification_agent import NotificationAgent
from backend.agents.code_review_graph import code_review_graph
from backend.utils.logger import logger


class WebhookAgent:
    """
    Orchestrates the complete AI code review pipeline.

    GitHub Webhook
        ↓
    GitService
        ↓
    LangGraph Code Review
        ↓
    Report Generation
        ↓
    Email Notification
    """

    def __init__(self):
        self.git_service = GitService(settings.repo_path)
        self.report_agent = ReportAgent()
        self.notification_agent = NotificationAgent()

    def process(self, payload: dict):

        logger.info("GitHub webhook received.")

        # -------------------------------------------------
        # 1. Load repository
        # -------------------------------------------------

        self.git_service.load_repository()

        # -------------------------------------------------
        # 2. Pull latest changes
        # -------------------------------------------------

        self.git_service.pull_latest_changes()

        # -------------------------------------------------
        # 3. Get latest commit
        # -------------------------------------------------

        latest_commit = self.git_service.get_latest_commit()

        commit_hash = latest_commit.hexsha

        # -------------------------------------------------
        # 4. Get changed files
        # -------------------------------------------------

        changed_files = self.git_service.get_changed_files()

        # -------------------------------------------------
        # 5. Get Git diff
        # -------------------------------------------------

        git_diff = self.git_service.get_commit_diff()

        logger.info("Starting LangGraph code review...")

        # -------------------------------------------------
        # 6. Run LangGraph
        # -------------------------------------------------

        graph_state = {
            "repository": payload.get(
                "repository",
                {}
            ).get(
                "full_name",
                ""
            ),

            "commit": commit_hash,

            "changed_files": changed_files,

            "git_diff": git_diff,
        }

        result = code_review_graph.invoke(graph_state)

        logger.info("LangGraph code review completed.")

        # -------------------------------------------------
        # 7. Extract analysis results
        # -------------------------------------------------

        code_analysis = result.get(
            "code_analysis",
            {}
        )

        security_analysis = result.get(
            "security_analysis",
            {}
        )

        risk_score = result.get(
            "risk_score",
            0
        )

        llm_review = result.get(
            "llm_review",
            ""
        )

        # -------------------------------------------------
        # 8. Generate reports
        # -------------------------------------------------

        logger.info("Generating structured reports...")

        markdown_report = self.report_agent.generate_markdown(
            review=llm_review,
            commit_hash=commit_hash,
            repository=graph_state["repository"],
            changed_files=changed_files,
            code_analysis=code_analysis,
            security_analysis=security_analysis,
            risk_score=risk_score,
        )

        pdf_report = self.report_agent.generate_pdf(
            review=llm_review,
            commit_hash=commit_hash,
            repository=graph_state["repository"],
            changed_files=changed_files,
            code_analysis=code_analysis,
            security_analysis=security_analysis,
            risk_score=risk_score,
        )

        logger.info("Reports generated successfully.")

        # -------------------------------------------------
        # 9. Send email notification
        # -------------------------------------------------

        logger.info("Sending email...")

        self.notification_agent.notify(
            receiver_email=settings.smtp_email,
            report_path=pdf_report,
        )

        logger.info("Email sent successfully.")

        # -------------------------------------------------
        # 10. Return result
        # -------------------------------------------------

        return {
            "status": "success",

            "repository": graph_state["repository"],

            "latest_commit": commit_hash,

            "changed_files": changed_files,

            "risk_score": risk_score,

            "risk_level": code_analysis.get(
                "risk_level",
                "UNKNOWN"
            ),

            "security_findings": security_analysis.get(
                "findings",
                []
            ),

            "markdown_report": markdown_report,

            "pdf_report": pdf_report,

            "email_sent": True,
        }