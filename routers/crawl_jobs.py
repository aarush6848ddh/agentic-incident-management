from agents.crawl_agent import run_crawl
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
import models
from models.crawl_job import CrawlJob
from schemas.crawl_job import CrawlJobCreate, CrawlJobResponse
from models.repository import Repository
from typing import List

router = APIRouter(prefix="/crawl-jobs", tags=["crawl-jobs"])

@router.post("/", response_model=CrawlJobResponse)
def create_crawl_job(crawl_job: CrawlJobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing_repo = db.query(Repository).filter(Repository.id == crawl_job.repository_id).first()
    if not existing_repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    new_crawl_job = CrawlJob(repository_id=crawl_job.repository_id)
    db.add(new_crawl_job)
    db.commit()
    db.refresh(new_crawl_job)
    background_tasks.add_task(run_crawl, new_crawl_job.id, crawl_job.repository_id)
    return new_crawl_job

@router.get("/", response_model=List[CrawlJobResponse])
def get_crawl_jobs(db: Session = Depends(get_db)):
    crawl_jobs = db.query(CrawlJob).all()
    return crawl_jobs