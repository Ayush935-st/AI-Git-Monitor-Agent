from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)

    repository_name = Column(String(255), nullable=False)
    branch = Column(String(100), nullable=False)

    commit_hash = Column(String(100), unique=True, nullable=False)

    author = Column(String(255), nullable=False)
    author_email = Column(String(255), nullable=False)

    commit_message = Column(String, nullable=False)
    commit_time = Column(DateTime, nullable=False)

    files_changed = Column(Integer, default=0)

    review_status = Column(String(50), default="Pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    report = relationship(
        "Report",
        back_populates="commit",
        uselist=False,
        cascade="all, delete-orphan",
    )