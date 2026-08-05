from fastapi import FastAPI
from backend.utils.logger import logger
from starlette.exceptions import HTTPException
from backend.agents.webhook_agent import WebhookAgent

from backend.database import Base, engine
from backend.scheduler import SchedulerService

from backend.services.git_service import GitService
from backend.config import settings

app = FastAPI(
    title="AI Git Monitoring Agent",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "AI Git Monitoring Agent Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }


@app.post("/review")
def review():
    """
    Module 9 integration will be added here.
    """
    return {
        "message": "Review Triggered"
    }


@app.get("/commits")
def commits():
    """
    Module 5 integration.
    """
    return {
        "message": "Commit History"
    }


@app.get("/reports")
def reports():
    """
    Module 10 integration.
    """
    return {
        "message": "Reports"
    }

scheduler = SchedulerService()


@app.on_event("startup")
def startup():
    scheduler.start()

webhook_agent = WebhookAgent()
from typing import Dict, Any

@app.post("/webhook/github")
async def github_webhook(payload: Dict[str, Any]):

    return webhook_agent.process(payload)
