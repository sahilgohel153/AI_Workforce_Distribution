from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...models.job import Job
from ...schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from ...services.skills_assessment import SkillsAssessmentService

router = APIRouter()
skills_service = SkillsAssessmentService()

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job role
    """
    # Validate salary range
    if job.min_salary >= job.max_salary:
        raise HTTPException(status_code=400, detail="Minimum salary must be less than maximum salary")
    
    # Create job object
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    return db_job

@router.get("/", response_model=JobListResponse)
def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department: Optional[str] = None,
    level: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of jobs with optional filtering
    """
    query = db.query(Job)
    
    # Apply filters
    if department:
        query = query.filter(Job.department == department)
    if level:
        query = query.filter(Job.level == level)
    if is_active is not None:
        query = query.filter(Job.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    jobs = query.offset(skip).limit(limit).all()
    
    return JobListResponse(
        jobs=jobs,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a specific job by ID
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    """
    Update a job role
    """
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update fields
    update_data = job_update.dict(exclude_unset=True)
    
    # Validate salary range if both are provided
    if 'min_salary' in update_data and 'max_salary' in update_data:
        if update_data['min_salary'] >= update_data['max_salary']:
            raise HTTPException(status_code=400, detail="Minimum salary must be less than maximum salary")
    elif 'min_salary' in update_data and db_job.max_salary:
        if update_data['min_salary'] >= db_job.max_salary:
            raise HTTPException(status_code=400, detail="Minimum salary must be less than maximum salary")
    elif 'max_salary' in update_data and db_job.min_salary:
        if db_job.min_salary >= update_data['max_salary']:
            raise HTTPException(status_code=400, detail="Minimum salary must be less than maximum salary")
    
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    db.commit()
    db.refresh(db_job)
    
    return db_job

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job role (soft delete by setting is_active to False)
    """
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_job.is_active = False
    db.commit()
    
    return {"message": "Job deleted successfully"}

@router.get("/departments/list")
def get_departments(db: Session = Depends(get_db)):
    """
    Get list of all departments
    """
    departments = db.query(Job.department).distinct().all()
    return [dept[0] for dept in departments]

@router.get("/levels/list")
def get_levels(db: Session = Depends(get_db)):
    """
    Get list of all job levels
    """
    levels = db.query(Job.level).distinct().all()
    return [level[0] for level in levels] 