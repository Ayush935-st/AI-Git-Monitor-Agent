from typing import Dict, Any

from importlib import import_module


# Load FastAPI dynamically so static analysis does not require the package
# to be installed in the currently selected Python environment.
_fastapi = import_module("fastapi")
FastAPI = _fastapi.FastAPI
HTTPException = _fastapi.HTTPException

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
# GitHub Webhook
# --------------------------------------------------

@app.post("/webhook/github")
async def github_webhook(payload: Dict[str, Any]):

    try:
        logger.info("GitHub webhook received.")

        result = webhook_agent.process(payload)

        logger.info("GitHub webhook processed successfully.")

        return result

    except Exception as e:

        logger.exception("GitHub webhook processing failed.")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )