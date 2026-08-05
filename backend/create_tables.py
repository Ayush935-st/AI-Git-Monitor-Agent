from backend.database import Base, engine
from backend.models.commit import Commit
from backend.models.report import Report

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")