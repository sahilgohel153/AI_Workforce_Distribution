#!/usr/bin/env python3
"""
Sample data population script for Workforce Distribution.ai
"""

import sys
import os
import requests
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

API_BASE_URL = "http://localhost:8000/api/v1"

def create_sample_jobs():
    """Create sample job roles"""
    jobs_data = [
        {
            "title": "Senior Software Engineer",
            "department": "Engineering",
            "level": "Senior",
            "min_salary": 120000,
            "max_salary": 180000,
            "currency": "USD",
            "required_skills": ["Python", "JavaScript", "SQL", "System Design"],
            "preferred_skills": ["React", "Docker", "AWS"],
            "experience_years": 5,
            "education_level": "Bachelor",
            "description": "We are looking for a Senior Software Engineer to join our growing team...",
            "responsibilities": ["Design and implement scalable software solutions", "Mentor junior developers", "Collaborate with cross-functional teams"],
            "benefits": ["Health insurance", "401k matching", "Flexible work hours"],
            "location": "San Francisco, CA",
            "work_type": "Full-time"
        },
        {
            "title": "Data Scientist",
            "department": "Data Science",
            "level": "Mid",
            "min_salary": 90000,
            "max_salary": 130000,
            "currency": "USD",
            "required_skills": ["Python", "Machine Learning", "Statistics", "SQL"],
            "preferred_skills": ["TensorFlow", "PyTorch", "Big Data"],
            "experience_years": 3,
            "education_level": "Master",
            "description": "Join our data science team to build innovative ML solutions...",
            "responsibilities": ["Develop machine learning models", "Analyze large datasets", "Present findings to stakeholders"],
            "benefits": ["Health insurance", "Professional development", "Remote work options"],
            "location": "New York, NY",
            "work_type": "Full-time"
        },
        {
            "title": "Product Manager",
            "department": "Product",
            "level": "Senior",
            "min_salary": 110000,
            "max_salary": 160000,
            "currency": "USD",
            "required_skills": ["Product Strategy", "User Research", "Agile", "Analytics"],
            "preferred_skills": ["SQL", "A/B Testing", "User Experience"],
            "experience_years": 4,
            "education_level": "Bachelor",
            "description": "Lead product development initiatives and drive user growth...",
            "responsibilities": ["Define product roadmap", "Work with engineering teams", "Analyze user feedback"],
            "benefits": ["Health insurance", "Stock options", "Flexible PTO"],
            "location": "Austin, TX",
            "work_type": "Full-time"
        }
    ]
    
    print("Creating sample jobs...")
    for job_data in jobs_data:
        response = requests.post(f"{API_BASE_URL}/jobs/", json=job_data)
        if response.status_code == 200:
            print(f"✅ Created job: {job_data['title']}")
        else:
            print(f"❌ Failed to create job: {job_data['title']} - {response.text}")

def create_sample_candidates():
    """Create sample candidates"""
    candidates_data = [
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@email.com",
            "phone": "+1-555-0101",
            "current_position": "Software Engineer",
            "current_company": "Tech Corp",
            "years_experience": 4.5,
            "education_level": "Bachelor",
            "skills": {
                "Python": 8,
                "JavaScript": 7,
                "SQL": 8,
                "System Design": 6,
                "React": 7,
                "Docker": 6
            },
            "expected_salary": 140000,
            "salary_currency": "USD",
            "preferred_locations": ["San Francisco, CA", "Remote"],
            "preferred_work_type": "Full-time",
            "preferred_departments": ["Engineering"],
            "is_available": True
        },
        {
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@email.com",
            "phone": "+1-555-0102",
            "current_position": "Data Analyst",
            "current_company": "Data Inc",
            "years_experience": 2.5,
            "education_level": "Master",
            "skills": {
                "Python": 7,
                "Machine Learning": 6,
                "Statistics": 8,
                "SQL": 7,
                "TensorFlow": 5,
                "Data Visualization": 7
            },
            "expected_salary": 95000,
            "salary_currency": "USD",
            "preferred_locations": ["New York, NY", "Remote"],
            "preferred_work_type": "Full-time",
            "preferred_departments": ["Data Science"],
            "is_available": True
        },
        {
            "first_name": "Carol",
            "last_name": "Davis",
            "email": "carol.davis@email.com",
            "phone": "+1-555-0103",
            "current_position": "Product Manager",
            "current_company": "Product Co",
            "years_experience": 5.0,
            "education_level": "MBA",
            "skills": {
                "Product Strategy": 8,
                "User Research": 7,
                "Agile": 8,
                "Analytics": 7,
                "SQL": 6,
                "A/B Testing": 7
            },
            "expected_salary": 130000,
            "salary_currency": "USD",
            "preferred_locations": ["Austin, TX", "Remote"],
            "preferred_work_type": "Full-time",
            "preferred_departments": ["Product"],
            "is_available": True
        },
        {
            "first_name": "David",
            "last_name": "Wilson",
            "email": "david.wilson@email.com",
            "phone": "+1-555-0104",
            "current_position": "Senior Developer",
            "current_company": "Dev Solutions",
            "years_experience": 7.0,
            "education_level": "Bachelor",
            "skills": {
                "Python": 9,
                "JavaScript": 8,
                "SQL": 9,
                "System Design": 8,
                "React": 8,
                "Docker": 8,
                "AWS": 7,
                "Leadership": 7
            },
            "expected_salary": 160000,
            "salary_currency": "USD",
            "preferred_locations": ["San Francisco, CA", "Seattle, WA"],
            "preferred_work_type": "Full-time",
            "preferred_departments": ["Engineering"],
            "is_available": True
        },
        {
            "first_name": "Eva",
            "last_name": "Brown",
            "email": "eva.brown@email.com",
            "phone": "+1-555-0105",
            "current_position": "Data Scientist",
            "current_company": "AI Labs",
            "years_experience": 3.5,
            "education_level": "PhD",
            "skills": {
                "Python": 9,
                "Machine Learning": 9,
                "Statistics": 9,
                "SQL": 7,
                "TensorFlow": 8,
                "PyTorch": 8,
                "Research": 8
            },
            "expected_salary": 120000,
            "salary_currency": "USD",
            "preferred_locations": ["New York, NY", "Boston, MA"],
            "preferred_work_type": "Full-time",
            "preferred_departments": ["Data Science"],
            "is_available": True
        }
    ]
    
    print("Creating sample candidates...")
    for candidate_data in candidates_data:
        response = requests.post(f"{API_BASE_URL}/candidates/", json=candidate_data)
        if response.status_code == 200:
            print(f"✅ Created candidate: {candidate_data['first_name']} {candidate_data['last_name']}")
        else:
            print(f"❌ Failed to create candidate: {candidate_data['first_name']} {candidate_data['last_name']} - {response.text}")

def main():
    """Main function to populate sample data"""
    print("🎯 Populating Workforce Distribution.ai with sample data...")
    print("Make sure the backend server is running on http://localhost:8000")
    
    try:
        # Test API connection
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Backend server is not running. Please start it first.")
            return
        
        print("✅ Backend server is running!")
        
        # Create sample data
        create_sample_jobs()
        create_sample_candidates()
        
        print("\n🎉 Sample data population completed!")
        print("You can now use the Streamlit frontend to explore the data.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Please make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 