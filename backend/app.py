from typing import Dict, Any

from importlib import import_module


# Load FastAPI dynamically so static analysis does not require the package
# to be installed in the currently selected Python environment.
_fastapi = import_module("fastapi")
FastAPI = _fastapi.FastAPI
HTTPException = _fastapi.HTTPException
BackgroundTasks = _fastapi.BackgroundTasks

from backend.config import settings
from backend.utils.logger import logger
from backend.database import Base, engine
from backend.scheduler import SchedulerService
from backend.agents.webhook_agent import WebhookAgent


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Services / Agents
# --------------------------------------------------

scheduler = SchedulerService()
webhook_agent = WebhookAgent()


# --------------------------------------------------
# Basic Routes
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Git Monitoring Agent Running",
        "version": settings.app_version
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }


# --------------------------------------------------
# Existing Module Routes
# --------------------------------------------------

@app.post("/review")
def review():
    """
    Trigger code review.
    """
    return {
        "message": "Review Triggered"
    }


@app.get("/commits")
def commits():
    """
    Return commit history.
    """
    return {
        "message": "Commit History"
    }


@app.get("/reports")
def reports():
    """
    Return generated reports.
    """
    return {
        "message": "Reports"
    }


# --------------------------------------------------
# Scheduler
# --------------------------------------------------

@app.on_event("startup")
def startup():
    logger.info("Starting scheduler...")
    scheduler.start()
    logger.info("Scheduler started successfully.")


# --------------------------------------------------
# GitHub Webhook Background Processing
# --------------------------------------------------

def process_github_webhook(payload: Dict[str, Any]):
    """
    Process the GitHub webhook in the background.

    The long-running AI review pipeline is executed after the
    webhook response has already been returned to GitHub.
    """

    try:
        logger.info("Starting background GitHub webhook processing.")

        webhook_agent.process(payload)

        logger.info(
            "Background GitHub webhook processing completed successfully."
        )

    except Exception:
        logger.exception(
            "Background GitHub webhook processing failed."
        )


# --------------------------------------------------
# GitHub Webhook
# --------------------------------------------------

@app.post("/webhook/github")
async def github_webhook(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """
    Receive GitHub webhook and queue the AI review pipeline.

    Returns immediately so GitHub does not timeout while the
    LLM, report generation, and email notification are running.
    """

    logger.info("GitHub webhook received.")

    background_tasks.add_task(
        process_github_webhook,
        payload
    )

    return {
        "status": "accepted",
        "message": "GitHub webhook received and queued for processing."
    }