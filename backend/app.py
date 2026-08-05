from fastapi import FastAPI, logger

from backend.database import Base, engine
from backend.scheduler import SchedulerService

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

from typing import Dict, Any

@app.post("/webhook/github")
async def github_webhook(payload: Dict[str, Any]):

    repository = payload.get("repository", {}).get("full_name")
    branch = payload.get("ref")
    commit_id = payload.get("head_commit", {}).get("id")
    commit_message = payload.get("head_commit", {}).get("message")
    author = (
        payload.get("head_commit", {})
        .get("author", {})
        .get("name")
    )

    return {
        "status": "success",
        "repository": repository,
        "branch": branch,
        "commit_id": commit_id,
        "commit_message": commit_message,
        "author": author
    }