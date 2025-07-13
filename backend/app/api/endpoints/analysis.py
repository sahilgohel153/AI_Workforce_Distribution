from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...schemas.analysis import (
    WorkforceDistributionRequest, WorkforceDistributionResponse,
    SalaryBenchmarkRequest, SalaryBenchmarkResponse,
    SkillsAnalysisRequest, SkillsAnalysisResponse
)
from ...services.workforce_analysis import WorkforceAnalysisService

router = APIRouter()
analysis_service = WorkforceAnalysisService()

@router.post("/distribute", response_model=WorkforceDistributionResponse)
def analyze_workforce_distribution(
    request: WorkforceDistributionRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze workforce distribution and find optimal candidate matches
    """
    try:
        result = analysis_service.analyze_workforce_distribution(db, request)
        return WorkforceDistributionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/salary-benchmark", response_model=SalaryBenchmarkResponse)
def get_salary_benchmark(
    job_title: str = Query(..., description="Job title to benchmark"),
    location: str = Query("US", description="Location for salary data"),
    experience_level: str = Query("Mid", description="Experience level"),
    db: Session = Depends(get_db)
):
    """
    Get salary benchmark for a specific job title and experience level
    """
    try:
        result = analysis_service.get_salary_benchmark(job_title, location, experience_level)
        return SalaryBenchmarkResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Salary benchmark failed: {str(e)}")

@router.post("/skills-gaps", response_model=SkillsAnalysisResponse)
def analyze_skills_gaps(
    request: SkillsAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze skills gaps across multiple candidates
    """
    try:
        result = analysis_service.analyze_skills_gaps(
            db, 
            request.candidate_ids, 
            request.focus_skills
        )
        return SkillsAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skills analysis failed: {str(e)}")

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get dashboard statistics for overview
    """
    try:
        from ...models.candidate import Candidate
        from ...models.job import Job
        
        # Get basic counts
        total_candidates = db.query(Candidate).count()
        active_candidates = db.query(Candidate).filter(Candidate.is_available == True).count()
        total_jobs = db.query(Job).count()
        active_jobs = db.query(Job).filter(Job.is_active == True).count()
        
        # Get experience distribution
        experience_stats = db.query(Candidate.years_experience).all()
        experience_values = [stat[0] for stat in experience_stats]
        
        avg_experience = sum(experience_values) / len(experience_values) if experience_values else 0
        
        # Get education distribution
        education_stats = db.query(Candidate.education_level).all()
        education_counts = {}
        for stat in education_stats:
            level = stat[0]
            education_counts[level] = education_counts.get(level, 0) + 1
        
        # Get department distribution
        department_stats = db.query(Job.department).all()
        department_counts = {}
        for stat in department_stats:
            dept = stat[0]
            department_counts[dept] = department_counts.get(dept, 0) + 1
        
        return {
            "total_candidates": total_candidates,
            "active_candidates": active_candidates,
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "avg_experience_years": round(avg_experience, 1),
            "education_distribution": education_counts,
            "department_distribution": department_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard stats failed: {str(e)}")

@router.get("/candidates/top-skilled")
def get_top_skilled_candidates(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get top candidates by overall skill score
    """
    try:
        from ...models.candidate import Candidate
        
        candidates = db.query(Candidate)\
            .filter(Candidate.overall_score.isnot(None))\
            .order_by(Candidate.overall_score.desc())\
            .limit(limit)\
            .all()
        
        return [
            {
                "id": c.id,
                "name": f"{c.first_name} {c.last_name}",
                "overall_score": c.overall_score,
                "years_experience": c.years_experience,
                "education_level": c.education_level,
                "current_position": c.current_position
            }
            for c in candidates
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Top candidates query failed: {str(e)}")

@router.get("/jobs/high-demand")
def get_high_demand_jobs(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get jobs with highest salary ranges (indicating high demand)
    """
    try:
        from ...models.job import Job
        
        jobs = db.query(Job)\
            .filter(Job.is_active == True)\
            .order_by((Job.max_salary - Job.min_salary).desc())\
            .limit(limit)\
            .all()
        
        return [
            {
                "id": j.id,
                "title": j.title,
                "department": j.department,
                "level": j.level,
                "salary_range": f"${j.min_salary:,.0f} - ${j.max_salary:,.0f}",
                "salary_spread": j.max_salary - j.min_salary,
                "required_skills_count": len(j.required_skills)
            }
            for j in jobs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"High demand jobs query failed: {str(e)}")

@router.get("/skills/market-demand")
def get_skills_market_demand(db: Session = Depends(get_db)):
    """
    Analyze skills market demand based on job requirements
    """
    try:
        from ...models.job import Job
        
        # Get all required skills from active jobs
        all_skills = []
        jobs = db.query(Job).filter(Job.is_active == True).all()
        
        for job in jobs:
            all_skills.extend(job.required_skills)
        
        # Count skill frequency
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Sort by frequency
        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {
                "skill": skill,
                "demand_count": count,
                "demand_percentage": round((count / len(jobs)) * 100, 1)
            }
            for skill, count in sorted_skills[:20]  # Top 20 skills
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skills market demand analysis failed: {str(e)}") 