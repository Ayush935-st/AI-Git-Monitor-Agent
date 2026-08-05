from backend.database import SessionLocal

db = SessionLocal()

print("Database connected successfully!")

db.close()

print("Database session closed successfully!")