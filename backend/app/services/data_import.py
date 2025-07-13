import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from ..models.job import Job
from ..models.candidate import Candidate
from ..models.skill import Skill
from ..services.skills_assessment import SkillsAssessmentService
import os

class DataImportService:
    def __init__(self):
        self.skills_service = SkillsAssessmentService()
        
        # Mapping of CSV columns to our system fields
        self.job_role_mapping = {
            'Sales Executive': 'Sales Representative',
            'Research Scientist': 'Data Scientist',
            'Laboratory Technician': 'Research Assistant',
            'Manufacturing Director': 'Operations Manager',
            'Healthcare Representative': 'Healthcare Specialist',
            'Manager': 'Department Manager',
            'Sales Representative': 'Sales Representative',
            'Research Director': 'Research Manager',
            'Human Resources': 'HR Specialist'
        }
        
        # Skills mapping based on job roles and education
        self.skills_mapping = {
            'Sales Executive': {
                'Sales': 8, 'Communication': 7, 'Negotiation': 7, 'Customer Service': 8,
                'Product Knowledge': 6, 'Relationship Building': 7
            },
            'Research Scientist': {
                'Research': 9, 'Data Analysis': 8, 'Statistics': 8, 'Python': 7,
                'Machine Learning': 7, 'Scientific Writing': 8
            },
            'Laboratory Technician': {
                'Laboratory Skills': 8, 'Data Collection': 7, 'Quality Control': 7,
                'Technical Skills': 6, 'Attention to Detail': 8
            },
            'Manufacturing Director': {
                'Operations Management': 8, 'Leadership': 7, 'Process Improvement': 7,
                'Team Management': 8, 'Strategic Planning': 7
            },
            'Healthcare Representative': {
                'Healthcare Knowledge': 8, 'Communication': 7, 'Medical Terminology': 7,
                'Customer Service': 6, 'Sales': 6
            },
            'Manager': {
                'Leadership': 8, 'Team Management': 8, 'Strategic Planning': 7,
                'Communication': 7, 'Decision Making': 8
            },
            'Sales Representative': {
                'Sales': 7, 'Communication': 7, 'Customer Service': 7,
                'Product Knowledge': 6, 'Relationship Building': 6
            },
            'Research Director': {
                'Research': 9, 'Leadership': 8, 'Strategic Planning': 8,
                'Team Management': 8, 'Scientific Writing': 8
            },
            'Human Resources': {
                'HR Management': 8, 'Communication': 7, 'Employee Relations': 7,
                'Recruitment': 7, 'Compliance': 6
            }
        }
        
        # Education level mapping
        self.education_mapping = {
            1: 'High School',
            2: 'Associate',
            3: 'Bachelor',
            4: 'Master',
            5: 'PhD'
        }
        
        # Job level mapping
        self.job_level_mapping = {
            1: 'Junior',
            2: 'Mid',
            3: 'Senior',
            4: 'Lead',
            5: 'Manager'
        }
    
    def import_csv_data(self, csv_file_path: str, db: Session) -> Dict:
        """
        Import data from CSV file and convert to our system format
        """
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path)
            
            # Create jobs from unique job roles
            jobs_created = self._create_jobs_from_csv(df, db)
            
            # Create candidates from employee data
            candidates_created = self._create_candidates_from_csv(df, db)
            
            # Create skills
            skills_created = self._create_skills_from_csv(df, db)
            
            return {
                "success": True,
                "jobs_created": jobs_created,
                "candidates_created": candidates_created,
                "skills_created": skills_created,
                "total_records": len(df)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "jobs_created": 0,
                "candidates_created": 0,
                "skills_created": 0
            }
    
    def _create_jobs_from_csv(self, df: pd.DataFrame, db: Session) -> int:
        """
        Create job roles from unique job roles in the CSV
        """
        unique_jobs = df[['JobRole', 'Department', 'JobLevel', 'MonthlyIncome']].drop_duplicates()
        jobs_created = 0
        
        for _, row in unique_jobs.iterrows():
            job_role = row['JobRole']
            department = row['Department']
            job_level = self.job_level_mapping.get(row['JobLevel'], 'Mid')
            monthly_income = row['MonthlyIncome']
            
            # Calculate salary range based on job level and income
            min_salary = monthly_income * 0.8
            max_salary = monthly_income * 1.2
            
            # Get required skills for this job role
            required_skills = list(self.skills_mapping.get(job_role, {}).keys())
            
            # Create job object
            job_data = {
                "title": self.job_role_mapping.get(job_role, job_role),
                "department": department,
                "level": job_level,
                "min_salary": float(min_salary),
                "max_salary": float(max_salary),
                "currency": "USD",
                "required_skills": required_skills,
                "preferred_skills": [],
                "experience_years": self._get_experience_for_level(job_level),
                "education_level": "Bachelor",  # Default education level
                "description": f"Position for {job_role} in {department} department",
                "responsibilities": [
                    f"Perform {job_role.lower()} duties",
                    "Collaborate with team members",
                    "Meet performance targets"
                ],
                "benefits": ["Health insurance", "401k", "Paid time off"],
                "location": "Remote",  # Default location
                "work_type": "Full-time"
            }
            
            # Check if job already exists
            existing_job = db.query(Job).filter(
                Job.title == job_data["title"],
                Job.department == job_data["department"]
            ).first()
            
            if not existing_job:
                db_job = Job(**job_data)
                db.add(db_job)
                jobs_created += 1
        
        db.commit()
        return jobs_created
    
    def _create_candidates_from_csv(self, df: pd.DataFrame, db: Session) -> int:
        """
        Create candidates from employee data in the CSV
        """
        candidates_created = 0
        
        for _, row in df.iterrows():
            # Skip if employee has left (attrition = 'Yes')
            if row['Attrition'] == 'Yes':
                continue
            
            # Generate candidate data
            candidate_data = self._convert_employee_to_candidate(row)
            
            # Check if candidate already exists (by email)
            email = f"employee{row['EmployeeNumber']}@company.com"
            existing_candidate = db.query(Candidate).filter(Candidate.email == email).first()
            
            if not existing_candidate:
                # Assess skills and calculate overall score
                skill_scores = self.skills_service.assess_candidate_skills(
                    self._create_candidate_object(candidate_data)
                )
                overall_score = self.skills_service.calculate_overall_score(
                    self._create_candidate_object(candidate_data), skill_scores
                )
                
                # Update candidate data with AI-generated scores
                candidate_data["skill_scores"] = skill_scores
                candidate_data["overall_score"] = overall_score
                
                db_candidate = Candidate(**candidate_data)
                db.add(db_candidate)
                candidates_created += 1
        
        db.commit()
        return candidates_created
    
    def _create_skills_from_csv(self, df: pd.DataFrame, db: Session) -> int:
        """
        Create skills from the skills mapping
        """
        skills_created = 0
        all_skills = set()
        
        # Collect all skills from the mapping
        for skills_dict in self.skills_mapping.values():
            all_skills.update(skills_dict.keys())
        
        # Create skill categories
        skill_categories = {
            'Sales': 'Business',
            'Communication': 'Soft Skills',
            'Negotiation': 'Business',
            'Customer Service': 'Business',
            'Product Knowledge': 'Domain',
            'Relationship Building': 'Soft Skills',
            'Research': 'Technical',
            'Data Analysis': 'Technical',
            'Statistics': 'Technical',
            'Python': 'Technical',
            'Machine Learning': 'Technical',
            'Scientific Writing': 'Communication',
            'Laboratory Skills': 'Technical',
            'Data Collection': 'Technical',
            'Quality Control': 'Technical',
            'Technical Skills': 'Technical',
            'Attention to Detail': 'Soft Skills',
            'Operations Management': 'Business',
            'Leadership': 'Soft Skills',
            'Process Improvement': 'Business',
            'Team Management': 'Business',
            'Strategic Planning': 'Business',
            'Healthcare Knowledge': 'Domain',
            'Medical Terminology': 'Domain',
            'HR Management': 'Business',
            'Employee Relations': 'Business',
            'Recruitment': 'Business',
            'Compliance': 'Business'
        }
        
        for skill_name in all_skills:
            # Check if skill already exists
            existing_skill = db.query(Skill).filter(Skill.name == skill_name).first()
            
            if not existing_skill:
                skill_data = {
                    "name": skill_name,
                    "category": skill_categories.get(skill_name, "Other"),
                    "description": f"Skill in {skill_name}",
                    "market_demand": np.random.uniform(6.0, 9.0),  # Random demand score
                    "salary_impact": np.random.uniform(5.0, 8.0),  # Random salary impact
                    "industry_relevance": np.random.uniform(7.0, 9.0)  # Random relevance
                }
                
                db_skill = Skill(**skill_data)
                db.add(db_skill)
                skills_created += 1
        
        db.commit()
        return skills_created
    
    def _convert_employee_to_candidate(self, row: pd.Series) -> Dict:
        """
        Convert employee data to candidate format
        """
        job_role = row['JobRole']
        education_level = self.education_mapping.get(row['Education'], 'Bachelor')
        
        # Generate skills based on job role and other factors
        base_skills = self.skills_mapping.get(job_role, {})
        
        # Adjust skills based on performance and satisfaction
        adjusted_skills = {}
        for skill, base_score in base_skills.items():
            # Adjust based on job satisfaction and performance
            satisfaction_bonus = (row['JobSatisfaction'] - 2.5) * 0.2
            performance_bonus = (row['PerformanceRating'] - 2.5) * 0.2
            adjusted_score = base_score + satisfaction_bonus + performance_bonus
            adjusted_skills[skill] = max(1, min(10, int(adjusted_score)))
        
        # Add some additional skills based on education and experience
        if row['Education'] >= 4:  # Master's or higher
            adjusted_skills['Leadership'] = 7
            adjusted_skills['Strategic Thinking'] = 6
        
        if row['TotalWorkingYears'] > 10:
            adjusted_skills['Experience'] = 9
            adjusted_skills['Problem Solving'] = 8
        
        # Generate candidate data
        candidate_data = {
            "first_name": f"Employee{row['EmployeeNumber']}",
            "last_name": f"From{row['Department']}",
            "email": f"employee{row['EmployeeNumber']}@company.com",
            "phone": f"+1-555-{row['EmployeeNumber']:04d}",
            "current_position": self.job_role_mapping.get(job_role, job_role),
            "current_company": "Current Company",
            "years_experience": float(row['TotalWorkingYears']),
            "education_level": education_level,
            "skills": adjusted_skills,
            "expected_salary": float(row['MonthlyIncome'] * 12),  # Annual salary
            "salary_currency": "USD",
            "preferred_locations": ["Remote", "Current Location"],
            "preferred_work_type": "Full-time",
            "preferred_departments": [row['Department']],
            "is_available": True,
            "status": "Active"
        }
        
        return candidate_data
    
    def _create_candidate_object(self, candidate_data: Dict) -> Candidate:
        """
        Create a Candidate object from data for skills assessment
        """
        candidate = Candidate()
        for key, value in candidate_data.items():
            if hasattr(candidate, key):
                setattr(candidate, key, value)
        return candidate
    
    def _get_experience_for_level(self, level: str) -> int:
        """
        Get required experience years for job level
        """
        level_experience = {
            'Junior': 1,
            'Mid': 3,
            'Senior': 6,
            'Lead': 8,
            'Manager': 10
        }
        return level_experience.get(level, 3)
    
    def get_import_summary(self, csv_file_path: str) -> Dict:
        """
        Get summary of data to be imported without actually importing
        """
        try:
            df = pd.read_csv(csv_file_path)
            
            # Count active employees (no attrition)
            active_employees = len(df[df['Attrition'] == 'No'])
            total_employees = len(df)
            
            # Get unique job roles
            unique_jobs = df['JobRole'].nunique()
            unique_departments = df['Department'].nunique()
            
            # Get salary statistics
            salary_stats = {
                'min': float(df['MonthlyIncome'].min()),
                'max': float(df['MonthlyIncome'].max()),
                'mean': float(df['MonthlyIncome'].mean()),
                'median': float(df['MonthlyIncome'].median())
            }
            
            # Get experience statistics
            experience_stats = {
                'min': float(df['TotalWorkingYears'].min()),
                'max': float(df['TotalWorkingYears'].max()),
                'mean': float(df['TotalWorkingYears'].mean())
            }
            
            return {
                "total_records": total_employees,
                "active_employees": active_employees,
                "attrition_rate": (total_employees - active_employees) / total_employees * 100,
                "unique_job_roles": unique_jobs,
                "unique_departments": unique_departments,
                "salary_statistics": salary_stats,
                "experience_statistics": experience_stats,
                "job_roles": df['JobRole'].value_counts().to_dict(),
                "departments": df['Department'].value_counts().to_dict()
            }
            
        except Exception as e:
            return {
                "error": str(e)
            } 