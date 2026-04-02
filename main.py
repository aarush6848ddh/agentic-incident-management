from fastapi import FastAPI
from database import engine, Base
import models  # Import all models to ensure they are registered with SQLAlchemy

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SentinelAI", version="1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}
