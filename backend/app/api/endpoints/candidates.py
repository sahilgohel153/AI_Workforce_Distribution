from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...models.candidate import Candidate
from ...models.job import Job
from ...schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse, CandidateListResponse, CandidateSkillAssessment
from ...services.skills_assessment import SkillsAssessmentService

router = APIRouter()
skills_service = SkillsAssessmentService()

@router.post("/", response_model=CandidateResponse)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    """
    Create a new candidate with skills assessment
    """
    # Check if email already exists
    existing_candidate = db.query(Candidate).filter(Candidate.email == candidate.email).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create candidate object
    db_candidate = Candidate(**candidate.dict())
    
    # Assess skills and calculate overall score
    skill_scores = skills_service.assess_candidate_skills(db_candidate)
    overall_score = skills_service.calculate_overall_score(db_candidate, skill_scores)
    
    # Update candidate with AI-generated scores
    db_candidate.skill_scores = skill_scores
    db_candidate.overall_score = overall_score
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.get("/", response_model=CandidateListResponse)
def get_candidates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    is_available: Optional[bool] = None,
    min_experience: Optional[float] = None,
    max_experience: Optional[float] = None,
    education_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of candidates with optional filtering
    """
    query = db.query(Candidate)
    
    # Apply filters
    if status:
        query = query.filter(Candidate.status == status)
    if is_available is not None:
        query = query.filter(Candidate.is_available == is_available)
    if min_experience is not None:
        query = query.filter(Candidate.years_experience >= min_experience)
    if max_experience is not None:
        query = query.filter(Candidate.years_experience <= max_experience)
    if education_level:
        query = query.filter(Candidate.education_level == education_level)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    candidates = query.offset(skip).limit(limit).all()
    
    return CandidateListResponse(
        candidates=candidates,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Get a specific candidate by ID
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidate

@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(candidate_id: int, candidate_update: CandidateUpdate, db: Session = Depends(get_db)):
    """
    Update a candidate
    """
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Update fields
    update_data = candidate_update.dict(exclude_unset=True)
    
    # Check email uniqueness if email is being updated
    if 'email' in update_data and update_data['email'] != db_candidate.email:
        existing_candidate = db.query(Candidate).filter(Candidate.email == update_data['email']).first()
        if existing_candidate:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for field, value in update_data.items():
        setattr(db_candidate, field, value)
    
    # Reassess skills if skills were updated
    if 'skills' in update_data:
        skill_scores = skills_service.assess_candidate_skills(db_candidate)
        overall_score = skills_service.calculate_overall_score(db_candidate, skill_scores)
        db_candidate.skill_scores = skill_scores
        db_candidate.overall_score = overall_score
    
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """
    Delete a candidate (soft delete by setting status to 'Deleted')
    """
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    db_candidate.status = "Deleted"
    db_candidate.is_available = False
    db.commit()
    
    return {"message": "Candidate deleted successfully"}

@router.post("/{candidate_id}/assess", response_model=CandidateSkillAssessment)
def assess_candidate_skills(candidate_id: int, db: Session = Depends(get_db)):
    """
    Reassess candidate skills and update scores
    """
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Reassess skills
    skill_scores = skills_service.assess_candidate_skills(db_candidate)
    overall_score = skills_service.calculate_overall_score(db_candidate, skill_scores)
    
    # Update candidate
    db_candidate.skill_scores = skill_scores
    db_candidate.overall_score = overall_score
    db.commit()
    
    return CandidateSkillAssessment(
        candidate_id=candidate_id,
        skill_scores=skill_scores,
        overall_score=overall_score
    )

@router.get("/{candidate_id}/match/{job_id}")
def match_candidate_to_job(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    """
    Match a candidate to a specific job
    """
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get match score and skill matches
    match_score, skill_matches = skills_service.match_candidate_to_job(candidate, job)
    
    # Get skill recommendations
    recommendations = skills_service.get_skill_recommendations(candidate, job)
    
    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "match_score": match_score,
        "skill_matches": skill_matches,
        "recommendations": recommendations,
        "candidate_name": f"{candidate.first_name} {candidate.last_name}",
        "job_title": job.title
    }

@router.get("/status/list")
def get_candidate_statuses(db: Session = Depends(get_db)):
    """
    Get list of all candidate statuses
    """
    statuses = db.query(Candidate.status).distinct().all()
    return [status[0] for status in statuses]

@router.get("/education/list")
def get_education_levels(db: Session = Depends(get_db)):
    """
    Get list of all education levels
    """
    education_levels = db.query(Candidate.education_level).distinct().all()
    return [level[0] for level in education_levels] 