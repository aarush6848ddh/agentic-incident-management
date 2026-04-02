from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class PRStatus(str, enum.Enum):
    open = "open"
    closed = "closed"
    merged = "merged"

class ReviewStatus(str, enum.Enum):
    pending = "pending"
    reviewing = "reviewing"
    completed = "completed"

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    github_pr_id = Column(Integer, unique=True)
    number = Column(Integer)
    title = Column(String)
    author = Column(String)
    base_branch = Column(String)
    head_branch = Column(String)
    status = Column(Enum(PRStatus), default=PRStatus.open)
    review_status = Column(Enum(ReviewStatus), default=ReviewStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    repository = relationship("Repository", back_populates="pull_requests")
    issues = relationship("Issue", back_populates="pull_request")