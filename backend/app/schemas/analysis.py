from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class WorkforceDistributionRequest(BaseModel):
    department: Optional[str] = None
    required_skills: List[str] = Field(..., min_items=1)
    experience_level: str = Field(..., description="Junior, Mid, Senior, Lead")
    budget_range: Optional[Dict[str, float]] = Field(None, description="min and max salary")
    location: Optional[str] = None
    work_type: Optional[str] = Field(None, description="Full-time, Part-time, Contract, Remote")

class CandidateMatch(BaseModel):
    candidate_id: int
    candidate_name: str
    match_score: float
    skill_matches: Dict[str, float]
    salary_fit: bool
    location_fit: bool
    experience_fit: bool

class WorkforceDistributionResponse(BaseModel):
    department: str
    total_candidates: int
    matched_candidates: List[CandidateMatch]
    distribution_score: float
    recommendations: List[str]
    analysis_date: datetime = Field(default_factory=datetime.now)

class SalaryBenchmarkRequest(BaseModel):
    job_title: str
    location: Optional[str] = None
    experience_level: Optional[str] = None
    skills: Optional[List[str]] = None

class SalaryBenchmarkResponse(BaseModel):
    job_title: str
    location: str
    experience_level: str
    market_average: float
    percentile_25: float
    percentile_50: float
    percentile_75: float
    percentile_90: float
    currency: str = "USD"
    data_points: int
    last_updated: datetime = Field(default_factory=datetime.now)

class SkillsAnalysisRequest(BaseModel):
    candidate_ids: List[int] = Field(..., min_items=1)
    focus_skills: Optional[List[str]] = None

class SkillsAnalysisResponse(BaseModel):
    candidate_skills_matrix: Dict[str, Dict[str, float]]
    skill_gaps: Dict[str, List[str]]
    top_skills: List[str]
    skill_recommendations: Dict[str, List[str]]
    analysis_date: datetime = Field(default_factory=datetime.now) 