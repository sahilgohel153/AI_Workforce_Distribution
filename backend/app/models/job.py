from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from ..core.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    department = Column(String(100), nullable=False)
    level = Column(String(50), nullable=False)  # Junior, Mid, Senior, Lead, etc.
    
    # Salary information
    min_salary = Column(Float, nullable=False)
    max_salary = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    
    # Job requirements
    required_skills = Column(JSON, nullable=False)  # List of required skills
    preferred_skills = Column(JSON, nullable=True)  # List of preferred skills
    experience_years = Column(Integer, nullable=False)
    education_level = Column(String(100), nullable=False)
    
    # Job details
    description = Column(Text, nullable=False)
    responsibilities = Column(JSON, nullable=False)  # List of responsibilities
    benefits = Column(JSON, nullable=True)  # List of benefits
    
    # Location and work type
    location = Column(String(255), nullable=False)
    work_type = Column(String(50), default="Full-time")  # Full-time, Part-time, Contract, Remote
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', department='{self.department}')>" 