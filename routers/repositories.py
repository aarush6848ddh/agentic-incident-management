from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from models.repository import Repository
from schemas.repository import RepositoryCreate, RepositoryResponse
from typing import List

router = APIRouter(prefix="/repositories", tags=["repositories"])

@router.post("/", response_model=RepositoryResponse)
def create_repository(repo: RepositoryCreate, db: Session = Depends(get_db)):
    # Check if repository with the same GitHub ID already exists
    existing_repo = db.query(Repository).filter(Repository.github_repo_id == repo.github_repo_id).first()
    if existing_repo:
        raise HTTPException(status_code=400, detail="Repository with this GitHub ID already exists")

    new_repo = Repository(
        github_repo_id=repo.github_repo_id,
        full_name=repo.full_name,
        url=repo.url,
        default_branch=repo.default_branch
    )
    db.add(new_repo)
    db.commit()
    db.refresh(new_repo)
    return new_repo

@router.get("/", response_model=List[RepositoryResponse])
def get_repositories(db: Session = Depends(get_db)):
    repos = db.query(Repository).all()
    return repos