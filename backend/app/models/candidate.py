from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON, Date
from sqlalchemy.sql import func
from ..core.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    
    # Professional information
    current_position = Column(String(255), nullable=True)
    current_company = Column(String(255), nullable=True)
    years_experience = Column(Float, nullable=False)
    education_level = Column(String(100), nullable=False)
    
    # Skills and assessment
    skills = Column(JSON, nullable=False)  # Dict with skill names and proficiency levels (1-10)
    skill_scores = Column(JSON, nullable=True)  # AI-generated skill scores
    overall_score = Column(Float, nullable=True)  # Overall candidate score
    
    # Salary expectations
    expected_salary = Column(Float, nullable=True)
    salary_currency = Column(String(3), default="USD")
    
    # Preferences
    preferred_locations = Column(JSON, nullable=True)  # List of preferred locations
    preferred_work_type = Column(String(50), nullable=True)  # Full-time, Part-time, etc.
    preferred_departments = Column(JSON, nullable=True)  # List of preferred departments
    
    # Availability
    available_from = Column(Date, nullable=True)
    is_available = Column(Boolean, default=True)
    
    # Status and metadata
    status = Column(String(50), default="Active")  # Active, Hired, Rejected, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Candidate(id={self.id}, name='{self.first_name} {self.last_name}', email='{self.email}')>" 