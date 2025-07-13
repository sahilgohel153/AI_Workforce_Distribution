from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class CandidateBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    current_position: Optional[str] = Field(None, max_length=255)
    current_company: Optional[str] = Field(None, max_length=255)
    years_experience: float = Field(..., ge=0)
    education_level: str = Field(..., min_length=1, max_length=100)
    skills: Dict[str, int] = Field(..., description="Skill name to proficiency level (1-10)")
    expected_salary: Optional[float] = Field(None, gt=0)
    salary_currency: str = Field(default="USD", min_length=3, max_length=3)
    preferred_locations: Optional[List[str]] = None
    preferred_work_type: Optional[str] = Field(None, max_length=50)
    preferred_departments: Optional[List[str]] = None
    available_from: Optional[date] = None
    is_available: bool = Field(default=True)

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    current_position: Optional[str] = Field(None, max_length=255)
    current_company: Optional[str] = Field(None, max_length=255)
    years_experience: Optional[float] = Field(None, ge=0)
    education_level: Optional[str] = Field(None, min_length=1, max_length=100)
    skills: Optional[Dict[str, int]] = None
    expected_salary: Optional[float] = Field(None, gt=0)
    salary_currency: Optional[str] = Field(None, min_length=3, max_length=3)
    preferred_locations: Optional[List[str]] = None
    preferred_work_type: Optional[str] = Field(None, max_length=50)
    preferred_departments: Optional[List[str]] = None
    available_from: Optional[date] = None
    is_available: Optional[bool] = None
    status: Optional[str] = Field(None, max_length=50)

class CandidateResponse(CandidateBase):
    id: int
    skill_scores: Optional[Dict[str, float]] = None
    overall_score: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CandidateListResponse(BaseModel):
    candidates: List[CandidateResponse]
    total: int
    page: int
    size: int

class CandidateSkillAssessment(BaseModel):
    candidate_id: int
    skill_scores: Dict[str, float]
    overall_score: float
    assessment_date: datetime = Field(default_factory=datetime.now) 