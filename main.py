from fastapi import FastAPI
from database import engine, Base
import models
from routers import repositories

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SentinelAI", version="1.0")

app.include_router(repositories.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
