from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    department: str = Field(..., min_length=1, max_length=100)
    level: str = Field(..., min_length=1, max_length=50)
    min_salary: float = Field(..., gt=0)
    max_salary: float = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    required_skills: List[str] = Field(..., min_items=1)
    preferred_skills: Optional[List[str]] = None
    experience_years: int = Field(..., ge=0)
    education_level: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)
    responsibilities: List[str] = Field(..., min_items=1)
    benefits: Optional[List[str]] = None
    location: str = Field(..., min_length=1, max_length=255)
    work_type: str = Field(default="Full-time", min_length=1, max_length=50)

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    level: Optional[str] = Field(None, min_length=1, max_length=50)
    min_salary: Optional[float] = Field(None, gt=0)
    max_salary: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    required_skills: Optional[List[str]] = Field(None, min_items=1)
    preferred_skills: Optional[List[str]] = None
    experience_years: Optional[int] = Field(None, ge=0)
    education_level: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    responsibilities: Optional[List[str]] = Field(None, min_items=1)
    benefits: Optional[List[str]] = None
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    work_type: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None

class JobResponse(JobBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    size: int 