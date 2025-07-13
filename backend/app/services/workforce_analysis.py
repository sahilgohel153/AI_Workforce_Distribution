import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from ..models.candidate import Candidate
from ..models.job import Job
from ..services.skills_assessment import SkillsAssessmentService
from ..schemas.analysis import WorkforceDistributionRequest, CandidateMatch

class WorkforceAnalysisService:
    def __init__(self):
        self.skills_service = SkillsAssessmentService()
        self.scaler = StandardScaler()
        
        # Salary benchmark data (mock data - in production, this would come from external APIs)
        self.salary_benchmarks = {
            'Software Engineer': {
                'Junior': {'25': 60000, '50': 75000, '75': 90000, '90': 110000},
                'Mid': {'25': 80000, '50': 95000, '75': 115000, '90': 140000},
                'Senior': {'25': 100000, '50': 120000, '75': 150000, '90': 180000},
                'Lead': {'25': 130000, '50': 160000, '75': 200000, '90': 250000}
            },
            'Data Scientist': {
                'Junior': {'25': 70000, '50': 85000, '75': 100000, '90': 120000},
                'Mid': {'25': 90000, '50': 110000, '75': 130000, '90': 160000},
                'Senior': {'25': 120000, '50': 140000, '75': 170000, '90': 200000},
                'Lead': {'25': 150000, '50': 180000, '75': 220000, '90': 280000}
            },
            'Product Manager': {
                'Junior': {'25': 65000, '50': 80000, '75': 95000, '90': 115000},
                'Mid': {'25': 85000, '50': 100000, '75': 120000, '90': 150000},
                'Senior': {'25': 110000, '50': 130000, '75': 160000, '90': 190000},
                'Lead': {'25': 140000, '50': 170000, '75': 210000, '90': 260000}
            }
        }
    
    def analyze_workforce_distribution(
        self, 
        db: Session, 
        request: WorkforceDistributionRequest
    ) -> Dict:
        """
        Analyze workforce distribution and find optimal candidate matches
        """
        # Get all available candidates
        candidates = db.query(Candidate).filter(Candidate.is_available == True).all()
        
        if not candidates:
            return {
                "department": request.department or "General",
                "total_candidates": 0,
                "matched_candidates": [],
                "distribution_score": 0.0,
                "recommendations": ["No available candidates found"],
                "analysis_date": pd.Timestamp.now()
            }
        
        # Find matching candidates
        matched_candidates = []
        for candidate in candidates:
            # Create a mock job for matching
            mock_job = self._create_mock_job_from_request(request)
            
            # Get match score
            match_score, skill_matches = self.skills_service.match_candidate_to_job(candidate, mock_job)
            
            # Check if candidate meets minimum threshold
            if match_score >= 0.6:  # 60% match threshold
                # Check salary fit
                salary_fit = self._check_salary_fit(candidate, request.budget_range)
                
                # Check location fit
                location_fit = self._check_location_fit(candidate, request.location)
                
                # Check experience fit
                experience_fit = self._check_experience_fit(candidate, request.experience_level)
                
                matched_candidates.append(CandidateMatch(
                    candidate_id=candidate.id,
                    candidate_name=f"{candidate.first_name} {candidate.last_name}",
                    match_score=match_score,
                    skill_matches=skill_matches,
                    salary_fit=salary_fit,
                    location_fit=location_fit,
                    experience_fit=experience_fit
                ))
        
        # Sort by match score
        matched_candidates.sort(key=lambda x: x.match_score, reverse=True)
        
        # Calculate distribution score
        distribution_score = self._calculate_distribution_score(matched_candidates)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(matched_candidates, request)
        
        return {
            "department": request.department or "General",
            "total_candidates": len(candidates),
            "matched_candidates": matched_candidates,
            "distribution_score": distribution_score,
            "recommendations": recommendations,
            "analysis_date": pd.Timestamp.now()
        }
    
    def get_salary_benchmark(
        self, 
        job_title: str, 
        location: str = "US", 
        experience_level: str = "Mid"
    ) -> Dict:
        """
        Get salary benchmark for a specific job title and experience level
        """
        # Get benchmark data
        benchmark_data = self.salary_benchmarks.get(job_title, {})
        level_data = benchmark_data.get(experience_level, {})
        
        if not level_data:
            # Return default benchmark if not found
            level_data = {'25': 70000, '50': 85000, '75': 100000, '90': 120000}
        
        # Calculate market average
        market_average = np.mean(list(level_data.values()))
        
        return {
            "job_title": job_title,
            "location": location,
            "experience_level": experience_level,
            "market_average": round(market_average, 2),
            "percentile_25": level_data.get('25', 0),
            "percentile_50": level_data.get('50', 0),
            "percentile_75": level_data.get('75', 0),
            "percentile_90": level_data.get('90', 0),
            "currency": "USD",
            "data_points": 1000,  # Mock data point count
            "last_updated": pd.Timestamp.now()
        }
    
    def analyze_skills_gaps(
        self, 
        db: Session, 
        candidate_ids: List[int], 
        focus_skills: Optional[List[str]] = None
    ) -> Dict:
        """
        Analyze skills gaps across multiple candidates
        """
        candidates = db.query(Candidate).filter(Candidate.id.in_(candidate_ids)).all()
        
        if not candidates:
            return {
                "candidate_skills_matrix": {},
                "skill_gaps": {},
                "top_skills": [],
                "skill_recommendations": {},
                "analysis_date": pd.Timestamp.now()
            }
        
        # Create skills matrix
        skills_matrix = {}
        all_skills = set()
        
        for candidate in candidates:
            candidate_name = f"{candidate.first_name} {candidate.last_name}"
            skill_scores = self.skills_service.assess_candidate_skills(candidate)
            skills_matrix[candidate_name] = skill_scores
            all_skills.update(skill_scores.keys())
        
        # Focus on specific skills if provided
        if focus_skills:
            all_skills = all_skills.intersection(set(focus_skills))
        
        # Find skill gaps
        skill_gaps = {}
        for skill in all_skills:
            skill_values = [skills_matrix[name].get(skill, 0) for name in skills_matrix]
            avg_skill = np.mean(skill_values)
            
            if avg_skill < 0.6:  # Threshold for skill gap
                skill_gaps[skill] = [name for name in skills_matrix if skills_matrix[name].get(skill, 0) < 0.6]
        
        # Find top skills
        skill_averages = {}
        for skill in all_skills:
            skill_values = [skills_matrix[name].get(skill, 0) for name in skills_matrix]
            skill_averages[skill] = np.mean(skill_values)
        
        top_skills = sorted(skill_averages.items(), key=lambda x: x[1], reverse=True)[:10]
        top_skills = [skill[0] for skill in top_skills]
        
        # Generate recommendations
        skill_recommendations = {}
        for candidate_name in skills_matrix:
            candidate_skills = skills_matrix[candidate_name]
            recommendations = []
            
            for skill in all_skills:
                if candidate_skills.get(skill, 0) < 0.6:
                    recommendations.append(f"Improve {skill} skills")
            
            skill_recommendations[candidate_name] = recommendations[:3]  # Top 3 recommendations
        
        return {
            "candidate_skills_matrix": skills_matrix,
            "skill_gaps": skill_gaps,
            "top_skills": top_skills,
            "skill_recommendations": skill_recommendations,
            "analysis_date": pd.Timestamp.now()
        }
    
    def _create_mock_job_from_request(self, request: WorkforceDistributionRequest) -> Job:
        """
        Create a mock job object from distribution request
        """
        mock_job = Job()
        mock_job.required_skills = request.required_skills
        mock_job.experience_years = self._get_experience_years(request.experience_level)
        mock_job.min_salary = request.budget_range.get('min', 50000) if request.budget_range else 50000
        mock_job.max_salary = request.budget_range.get('max', 100000) if request.budget_range else 100000
        mock_job.location = request.location or "Remote"
        mock_job.work_type = request.work_type or "Full-time"
        return mock_job
    
    def _get_experience_years(self, level: str) -> int:
        """
        Convert experience level to years
        """
        level_mapping = {
            'Junior': 2,
            'Mid': 5,
            'Senior': 8,
            'Lead': 12
        }
        return level_mapping.get(level, 5)
    
    def _check_salary_fit(self, candidate: Candidate, budget_range: Optional[Dict]) -> bool:
        """
        Check if candidate's salary expectations fit the budget
        """
        if not budget_range or not candidate.expected_salary:
            return True
        
        min_budget = budget_range.get('min', 0)
        max_budget = budget_range.get('max', float('inf'))
        
        return min_budget <= candidate.expected_salary <= max_budget
    
    def _check_location_fit(self, candidate: Candidate, required_location: Optional[str]) -> bool:
        """
        Check if candidate's location preferences match requirements
        """
        if not required_location:
            return True
        
        if not candidate.preferred_locations:
            return True
        
        return required_location in candidate.preferred_locations
    
    def _check_experience_fit(self, candidate: Candidate, required_level: str) -> bool:
        """
        Check if candidate's experience matches required level
        """
        required_years = self._get_experience_years(required_level)
        
        # Allow some flexibility in experience matching
        if required_level == 'Junior':
            return candidate.years_experience <= required_years + 2
        elif required_level == 'Mid':
            return required_years - 2 <= candidate.years_experience <= required_years + 3
        elif required_level == 'Senior':
            return candidate.years_experience >= required_years - 2
        else:  # Lead
            return candidate.years_experience >= required_years - 3
    
    def _calculate_distribution_score(self, matched_candidates: List[CandidateMatch]) -> float:
        """
        Calculate overall distribution quality score
        """
        if not matched_candidates:
            return 0.0
        
        # Calculate average match score
        avg_match_score = np.mean([c.match_score for c in matched_candidates])
        
        # Bonus for having multiple good candidates
        diversity_bonus = min(len(matched_candidates) / 10.0, 0.2)
        
        return min(avg_match_score + diversity_bonus, 1.0)
    
    def _generate_recommendations(
        self, 
        matched_candidates: List[CandidateMatch], 
        request: WorkforceDistributionRequest
    ) -> List[str]:
        """
        Generate recommendations based on analysis results
        """
        recommendations = []
        
        if not matched_candidates:
            recommendations.append("No suitable candidates found. Consider expanding search criteria.")
            return recommendations
        
        # Top match recommendation
        top_candidate = matched_candidates[0]
        recommendations.append(f"Top candidate: {top_candidate.candidate_name} (Match: {top_candidate.match_score:.1%})")
        
        # Diversity recommendation
        if len(matched_candidates) >= 3:
            recommendations.append(f"Found {len(matched_candidates)} qualified candidates for good team diversity")
        elif len(matched_candidates) == 1:
            recommendations.append("Only one candidate found. Consider expanding search or adjusting requirements.")
        
        # Skill gap recommendations
        if request.required_skills:
            missing_skills = set(request.required_skills)
            for candidate in matched_candidates[:3]:  # Check top 3 candidates
                candidate_skills = set(candidate.skill_matches.keys())
                missing = missing_skills - candidate_skills
                if missing:
                    recommendations.append(f"Consider training programs for: {', '.join(list(missing)[:3])}")
                    break
        
        return recommendations 