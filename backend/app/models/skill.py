from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from ..core.database import Base

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False)  # Technical, Soft Skills, Domain, etc.
    description = Column(Text, nullable=True)
    
    # Market demand and salary impact
    market_demand = Column(Float, default=0.0)  # 0-10 scale
    salary_impact = Column(Float, default=0.0)  # 0-10 scale
    industry_relevance = Column(Float, default=0.0)  # 0-10 scale
    
    # Skill metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', category='{self.category}')>" 