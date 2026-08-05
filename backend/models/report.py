from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    commit_id = Column(
        Integer,
        ForeignKey("commits.id"),
        nullable=False,
        unique=True,
    )

    review_summary = Column(Text)

    security_score = Column(Integer)
    code_quality_score = Column(Integer)
    performance_score = Column(Integer)
    maintainability_score = Column(Integer)

    risk_level = Column(String(50))

    recommendations = Column(Text)

    report_path = Column(String(500))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    commit = relationship(
        "Commit",
        back_populates="report",
    )