import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from ..models.candidate import Candidate
from ..models.job import Job
from ..core.config import settings

class SkillsAssessmentService:
    def __init__(self):
        self.scaler = StandardScaler()
        self.skill_weights = {
            'technical': 0.4,
            'soft_skills': 0.3,
            'domain': 0.2,
            'leadership': 0.1
        }
    
    def assess_candidate_skills(self, candidate: Candidate, job: Job = None) -> Dict[str, float]:
        """
        Assess candidate skills and return skill scores
        """
        skill_scores = {}
        
        # Convert self-reported skills to AI-generated scores
        for skill_name, proficiency in candidate.skills.items():
            # Base score from self-reported proficiency (1-10 scale)
            base_score = proficiency / 10.0
            
            # Apply AI enhancement based on experience and education
            experience_multiplier = min(candidate.years_experience / 10.0, 1.5)
            education_bonus = self._get_education_bonus(candidate.education_level)
            
            # Calculate final skill score
            final_score = base_score * experience_multiplier + education_bonus
            skill_scores[skill_name] = min(final_score, 1.0)  # Cap at 1.0
        
        return skill_scores
    
    def calculate_overall_score(self, candidate: Candidate, skill_scores: Dict[str, float]) -> float:
        """
        Calculate overall candidate score based on skills, experience, and other factors
        """
        if not skill_scores:
            return 0.0
        
        # Average skill score
        avg_skill_score = np.mean(list(skill_scores.values()))
        
        # Experience score (normalized to 0-1)
        experience_score = min(candidate.years_experience / 15.0, 1.0)
        
        # Education score
        education_score = self._get_education_score(candidate.education_level)
        
        # Calculate weighted overall score
        overall_score = (
            avg_skill_score * 0.5 +
            experience_score * 0.3 +
            education_score * 0.2
        )
        
        return round(overall_score, 3)
    
    def match_candidate_to_job(self, candidate: Candidate, job: Job) -> Tuple[float, Dict[str, float]]:
        """
        Match candidate to a specific job and return match score and skill matches
        """
        # Get candidate skill scores
        candidate_skill_scores = self.assess_candidate_skills(candidate, job)
        
        # Calculate skill match for required skills
        skill_matches = {}
        required_skills = set(job.required_skills)
        candidate_skills = set(candidate_skill_scores.keys())
        
        # Calculate match for each required skill
        for skill in required_skills:
            if skill in candidate_skill_scores:
                skill_matches[skill] = candidate_skill_scores[skill]
            else:
                skill_matches[skill] = 0.0
        
        # Calculate overall match score
        if required_skills:
            skill_match_score = np.mean([skill_matches[skill] for skill in required_skills])
        else:
            skill_match_score = 0.0
        
        # Experience match
        experience_match = 1.0 - abs(candidate.years_experience - job.experience_years) / max(job.experience_years, 1)
        experience_match = max(0.0, min(1.0, experience_match))
        
        # Salary fit
        salary_fit = 1.0
        if candidate.expected_salary and job.min_salary and job.max_salary:
            if candidate.expected_salary < job.min_salary:
                salary_fit = 0.8  # Slight penalty for under-asking
            elif candidate.expected_salary > job.max_salary * 1.2:
                salary_fit = 0.6  # Penalty for over-asking
            else:
                salary_fit = 1.0
        
        # Calculate final match score
        match_score = (
            skill_match_score * 0.6 +
            experience_match * 0.3 +
            salary_fit * 0.1
        )
        
        return round(match_score, 3), skill_matches
    
    def _get_education_bonus(self, education_level: str) -> float:
        """
        Get education bonus for skill assessment
        """
        education_bonuses = {
            'High School': 0.0,
            'Associate': 0.05,
            'Bachelor': 0.1,
            'Master': 0.15,
            'PhD': 0.2,
            'MBA': 0.15,
            'Certificate': 0.05
        }
        return education_bonuses.get(education_level, 0.0)
    
    def _get_education_score(self, education_level: str) -> float:
        """
        Get education score for overall assessment
        """
        education_scores = {
            'High School': 0.3,
            'Associate': 0.5,
            'Bachelor': 0.7,
            'Master': 0.85,
            'PhD': 1.0,
            'MBA': 0.9,
            'Certificate': 0.6
        }
        return education_scores.get(education_level, 0.5)
    
    def get_skill_recommendations(self, candidate: Candidate, target_job: Job = None) -> List[str]:
        """
        Get skill improvement recommendations for a candidate
        """
        recommendations = []
        
        if target_job:
            # Recommend skills needed for target job
            candidate_skills = set(candidate.skills.keys())
            required_skills = set(target_job.required_skills)
            missing_skills = required_skills - candidate_skills
            
            for skill in missing_skills:
                recommendations.append(f"Learn {skill} for {target_job.title} position")
        
        # General recommendations based on experience level
        if candidate.years_experience < 2:
            recommendations.extend([
                "Focus on building core technical skills",
                "Develop soft skills like communication and teamwork",
                "Gain hands-on project experience"
            ])
        elif candidate.years_experience < 5:
            recommendations.extend([
                "Develop leadership skills",
                "Specialize in a specific domain",
                "Build mentoring capabilities"
            ])
        else:
            recommendations.extend([
                "Focus on strategic thinking",
                "Develop executive presence",
                "Build industry expertise"
            ])
        
        return recommendations[:5]  # Return top 5 recommendations 