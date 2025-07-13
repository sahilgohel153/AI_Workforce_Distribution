import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import numpy as np

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Page configuration
st.set_page_config(
    page_title="TalentForge Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern dark theme
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e0e0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Custom Header */
    .hero-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #b8b8b8;
        font-weight: 300;
    }
    
    /* Card Styles */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #b8b8b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #b8b8b8;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Form Styles */
    .stForm {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(45deg, #00b894, #00cec9);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: none;
    }
    
    .error-message {
        background: linear-gradient(45deg, #e17055, #d63031);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: none;
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
    }
    
    /* Dataframe Styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Custom Icons */
    .icon-large {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint, method="GET", data=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def create_metric_card(label, value, icon="📊"):
    """Create a custom metric card"""
    st.markdown(f"""
    <div class="metric-card">
        <div style="text-align: center;">
            <div class="icon-large">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main_dashboard():
    """Main dashboard with modern design"""
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">TalentForge Pro</div>
        <div class="hero-subtitle">AI-Powered Workforce Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have any data
    stats = make_api_request("/analysis/dashboard/stats")
    has_data = stats and (stats.get("total_candidates", 0) > 0 or stats.get("total_jobs", 0) > 0)
    
    if not has_data:
        st.markdown("""
        <div class="chart-container">
            <div style="text-align: center; padding: 2rem;">
                <h2 style="color: #667eea; margin-bottom: 1rem;">🎉 Welcome to TalentForge Pro!</h2>
                <p style="color: #b8b8b8; font-size: 1.1rem; margin-bottom: 2rem;">
                    Your AI-powered workforce intelligence platform is ready to help you build the perfect team.
                </p>
                <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                    <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
                        <h4 style="color: #4ecdc4; margin-bottom: 0.5rem;">💼 Add Jobs</h4>
                        <p style="color: #b8b8b8; font-size: 0.9rem;">Create job postings with detailed requirements</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
                        <h4 style="color: #ff6b6b; margin-bottom: 0.5rem;">👥 Add Candidates</h4>
                        <p style="color: #b8b8b8; font-size: 0.9rem;">Build your talent network</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
                        <h4 style="color: #667eea; margin-bottom: 0.5rem;">📁 Import Data</h4>
                        <p style="color: #b8b8b8; font-size: 0.9rem;">Import your existing workforce data</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_candidates = stats.get("total_candidates", 0) if stats else 0
        create_metric_card("Total Candidates", total_candidates, "👥")
    
    with col2:
        active_candidates = stats.get("active_candidates", 0) if stats else 0
        create_metric_card("Active Candidates", active_candidates, "✅")
    
    with col3:
        total_jobs = stats.get("total_jobs", 0) if stats else 0
        create_metric_card("Total Jobs", total_jobs, "💼")
    
    with col4:
        active_jobs = stats.get("active_jobs", 0) if stats else 0
        create_metric_card("Active Jobs", active_jobs, "🔥")
        
        # Charts Section
        st.markdown("### 📈 Analytics Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Education distribution
            education_dist = stats.get("education_distribution", {}) if stats else {}
            if education_dist:
                education_df = pd.DataFrame(
                    list(education_dist.items()),
                    columns=["Education Level", "Count"]
                )
                fig = px.pie(education_df, values="Count", names="Education Level", 
                           title="🎓 Education Distribution",
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                    <h3>📊 No Education Data Available</h3>
                    <p>Add candidates to see education distribution</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Department distribution
            dept_dist = stats.get("department_distribution", {}) if stats else {}
            if dept_dist:
                dept_df = pd.DataFrame(
                    list(dept_dist.items()),
                    columns=["Department", "Count"]
                )
                fig = px.bar(dept_df, x="Department", y="Count", 
                           title="🏢 Jobs by Department",
                           color_discrete_sequence=['#667eea'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                    <h3>🏢 No Department Data Available</h3>
                    <p>Add jobs to see department distribution</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Top skilled candidates
        st.markdown("### 🏆 Top Performers")
        top_candidates = make_api_request("/analysis/candidates/top-skilled?limit=10")
        
        if top_candidates:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            candidates_df = pd.DataFrame(top_candidates)
            fig = px.bar(candidates_df, x="name", y="overall_score", 
                        title="🌟 Top Candidates by Skill Score",
                        labels={"name": "Candidate", "overall_score": "Skill Score"},
                        color_discrete_sequence=['#4ecdc4'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                <h3>🏆 No Top Performers Data Available</h3>
                <p>Add candidates and assess their skills to see top performers</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def jobs_management():
    """Jobs management section with modern design"""
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">💼 Job Management</div>
        <div class="hero-subtitle">Create, manage, and analyze job opportunities</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🚀 Create Job", "📋 View Jobs", "📊 Job Analysis"])
    
    with tab1:
        st.markdown("### 🚀 Create New Job Opportunity")
        
        with st.form("create_job_form"):
            st.markdown('<div class="stForm">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Job Title")
                department = st.text_input("Department")
                level = st.selectbox("Level", ["Junior", "Mid", "Senior", "Lead"])
                min_salary = st.number_input("Minimum Salary", min_value=0, value=50000)
                max_salary = st.number_input("Maximum Salary", min_value=0, value=100000)
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
            
            with col2:
                experience_years = st.number_input("Required Experience (Years)", min_value=0, value=3)
                education_level = st.selectbox("Education Level", 
                    ["High School", "Associate", "Bachelor", "Master", "PhD", "MBA", "Certificate"])
                location = st.text_input("Location")
                work_type = st.selectbox("Work Type", ["Full-time", "Part-time", "Contract", "Remote"])
            
            description = st.text_area("Job Description")
            required_skills = st.text_area("Required Skills (comma-separated)")
            responsibilities = st.text_area("Responsibilities (comma-separated)")
            benefits = st.text_area("Benefits (comma-separated)")
            
            submitted = st.form_submit_button("🚀 Launch Job Posting")
            
            if submitted:
                if title and department and description:
                    job_data = {
                        "title": title,
                        "department": department,
                        "level": level,
                        "min_salary": min_salary,
                        "max_salary": max_salary,
                        "currency": currency,
                        "required_skills": [skill.strip() for skill in required_skills.split(",") if skill.strip()],
                        "preferred_skills": [],
                        "experience_years": experience_years,
                        "education_level": education_level,
                        "description": description,
                        "responsibilities": [resp.strip() for resp in responsibilities.split(",") if resp.strip()],
                        "benefits": [benefit.strip() for benefit in benefits.split(",") if benefit.strip()],
                        "location": location,
                        "work_type": work_type
                    }
                    
                    result = make_api_request("/jobs/", method="POST", data=job_data)
                    if result:
                        st.markdown('<div class="success-message">🎉 Job created successfully! Your new opportunity is now live.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📋 Job Opportunities Dashboard")
        
        # Filters
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            department_filter = st.selectbox("Filter by Department", ["All"] + 
                [dept for dept in make_api_request("/jobs/departments/list") or []])
        with col2:
            level_filter = st.selectbox("Filter by Level", ["All"] + 
                [level for level in make_api_request("/jobs/levels/list") or []])
        with col3:
            active_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive"])
        
        # Get jobs
        jobs = make_api_request("/jobs/")
        
        if jobs and jobs.get("jobs"):
            jobs_df = pd.DataFrame(jobs["jobs"])
            
            # Apply filters
            if department_filter != "All":
                jobs_df = jobs_df[jobs_df["department"] == department_filter]
            if level_filter != "All":
                jobs_df = jobs_df[jobs_df["level"] == level_filter]
            if active_filter != "All":
                is_active = active_filter == "Active"
                jobs_df = jobs_df[jobs_df["is_active"] == is_active]
            
            st.dataframe(jobs_df[["id", "title", "department", "level", "min_salary", "max_salary", "is_active"]])
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                <h3>💼 No Jobs Available</h3>
                <p>Create your first job posting to get started</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📊 Market Intelligence")
        
        # High demand jobs
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        high_demand_jobs = make_api_request("/analysis/jobs/high-demand?limit=10")
        
        if high_demand_jobs:
            st.write("**High Demand Jobs (by Salary Range)**")
            demand_df = pd.DataFrame(high_demand_jobs)
            fig = px.bar(demand_df, x="title", y="salary_spread", 
                        title="💰 Jobs by Salary Range Spread",
                        labels={"title": "Job Title", "salary_spread": "Salary Range Spread"},
                        color_discrete_sequence=['#ff6b6b'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                <h3>💰 No High Demand Jobs Data</h3>
                <p>Add more jobs with different salary ranges to see demand analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Skills market demand
        skills_demand = make_api_request("/analysis/skills/market-demand")
        
        if skills_demand:
            st.write("**🔥 Hot Skills in Demand**")
            skills_df = pd.DataFrame(skills_demand)
            fig = px.bar(skills_df, x="skill", y="demand_count", 
                        title="🚀 Skills by Market Demand",
                        labels={"skill": "Skill", "demand_count": "Demand Count"},
                        color_discrete_sequence=['#4ecdc4'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                <h3>🔥 No Skills Demand Data</h3>
                <p>Add jobs with required skills to see market demand analysis</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def candidates_management():
    """Candidates management section with modern design"""
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">👥 Talent Management</div>
        <div class="hero-subtitle">Discover, assess, and manage top talent</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🌟 Add Talent", "📋 View Candidates", "🎯 Skills Assessment"])
    
    with tab1:
        st.markdown("### 🌟 Add New Talent to Your Network")
        
        with st.form("create_candidate_form"):
            st.markdown('<div class="stForm">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                current_position = st.text_input("Current Position")
                current_company = st.text_input("Current Company")
            
            with col2:
                years_experience = st.number_input("Years of Experience", min_value=0.0, value=3.0)
                education_level = st.selectbox("Education Level", 
                    ["High School", "Associate", "Bachelor", "Master", "PhD", "MBA", "Certificate"])
                expected_salary = st.number_input("Expected Salary", min_value=0, value=75000)
                work_type = st.selectbox("Preferred Work Type", ["Full-time", "Part-time", "Contract", "Remote"])
            
            # Skills input
            st.markdown("### 🎯 Skills Assessment (Rate 1-10)")
            col1, col2, col3 = st.columns(3)
            
            skills = {}
            common_skills = ["Python", "JavaScript", "SQL", "Machine Learning", "Data Analysis", 
                           "Project Management", "Communication", "Leadership", "Problem Solving"]
            
            for i, skill in enumerate(common_skills):
                col_idx = i % 3
                if col_idx == 0:
                    skills[skill] = col1.slider(skill, 1, 10, 5)
                elif col_idx == 1:
                    skills[skill] = col2.slider(skill, 1, 10, 5)
                else:
                    skills[skill] = col3.slider(skill, 1, 10, 5)
            
            # Custom skills
            custom_skills_input = st.text_area("Additional Skills (format: skill:rating,skill:rating)")
            
            submitted = st.form_submit_button("🌟 Add Talent to Network")
            
            if submitted:
                if first_name and last_name and email:
                    # Parse custom skills
                    if custom_skills_input:
                        for skill_rating in custom_skills_input.split(","):
                            if ":" in skill_rating:
                                skill, rating = skill_rating.split(":")
                                skills[skill.strip()] = int(rating.strip())
                    
                    candidate_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "current_position": current_position,
                        "current_company": current_company,
                        "years_experience": years_experience,
                        "education_level": education_level,
                        "skills": skills,
                        "expected_salary": expected_salary,
                        "salary_currency": "USD",
                        "preferred_work_type": work_type,
                        "is_available": True
                    }
                    
                    result = make_api_request("/candidates/", method="POST", data=candidate_data)
                    if result:
                        st.markdown('<div class="success-message">🎉 Talent added successfully! New candidate is now in your network.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📋 Talent Network Overview")
        
        # Filters
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All"] + 
                [status for status in make_api_request("/candidates/status/list") or []])
        with col2:
            education_filter = st.selectbox("Filter by Education", ["All"] + 
                [edu for edu in make_api_request("/candidates/education/list") or []])
        with col3:
            available_filter = st.selectbox("Filter by Availability", ["All", "Available", "Not Available"])
        
        # Get candidates
        candidates = make_api_request("/candidates/")
        
        if candidates and candidates.get("candidates"):
            candidates_df = pd.DataFrame(candidates["candidates"])
            
            # Apply filters
            if status_filter != "All":
                candidates_df = candidates_df[candidates_df["status"] == status_filter]
            if education_filter != "All":
                candidates_df = candidates_df[candidates_df["education_level"] == education_filter]
            if available_filter != "All":
                is_available = available_filter == "Available"
                candidates_df = candidates_df[candidates_df["is_available"] == is_available]
            
            st.dataframe(candidates_df[["id", "first_name", "last_name", "email", "years_experience", 
                                      "education_level", "overall_score", "status"]])
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                <h3>👥 No Candidates Available</h3>
                <p>Add candidates to your talent network to get started</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🎯 Skills Assessment Center")
        
        # Get candidates for assessment
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        candidates = make_api_request("/candidates/")
        
        if candidates and candidates.get("candidates"):
            candidate_options = {f"{c['first_name']} {c['last_name']}": c['id'] 
                               for c in candidates["candidates"]}
            
            selected_candidate = st.selectbox("Select Candidate", list(candidate_options.keys()))
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #b8b8b8;">
                <h3>🎯 No Candidates for Assessment</h3>
                <p>Add candidates to your network to assess their skills</p>
            </div>
            """, unsafe_allow_html=True)
            selected_candidate = None
            
            if selected_candidate:
                candidate_id = candidate_options[selected_candidate]
                
                # Reassess skills
                if st.button("🔄 Reassess Skills"):
                    result = make_api_request(f"/candidates/{candidate_id}/assess", method="POST")
                    if result:
                        st.markdown('<div class="success-message">✅ Skills reassessed successfully!</div>', unsafe_allow_html=True)
                
                # Show current assessment
                candidate_data = make_api_request(f"/candidates/{candidate_id}")
                if candidate_data and candidate_data.get("skill_scores"):
                    st.markdown("**📊 Current Skill Scores**")
                    
                    skills_df = pd.DataFrame(
                        list(candidate_data["skill_scores"].items()),
                        columns=["Skill", "Score"]
                    )
                    
                    fig = px.bar(skills_df, x="Skill", y="Score", 
                                title=f"🎯 Skill Assessment for {selected_candidate}",
                                range_y=[0, 1],
                                color_discrete_sequence=['#667eea'])
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e0e0e0'),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    create_metric_card("Overall Score", f"{candidate_data.get('overall_score', 0):.3f}", "🏆")
        st.markdown('</div>', unsafe_allow_html=True)

def workforce_analysis():
    """Workforce analysis section with modern design"""
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">📊 Workforce Intelligence</div>
        <div class="hero-subtitle">Advanced analytics and insights for strategic decisions</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎯 Distribution Analysis", "💰 Salary Benchmarking", "🔍 Skills Gap Analysis"])
    
    with tab1:
        st.markdown("### 🎯 Smart Distribution Analysis")
        
        with st.form("distribution_analysis_form"):
            st.markdown('<div class="stForm">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                department = st.text_input("Department (optional)")
                experience_level = st.selectbox("Experience Level", ["Junior", "Mid", "Senior", "Lead"])
                location = st.text_input("Location (optional)")
                work_type = st.selectbox("Work Type", ["Full-time", "Part-time", "Contract", "Remote"])
            
            with col2:
                min_salary = st.number_input("Minimum Budget", min_value=0, value=50000)
                max_salary = st.number_input("Maximum Budget", min_value=0, value=100000)
            
            required_skills = st.text_area("Required Skills (comma-separated)")
            
            submitted = st.form_submit_button("🚀 Launch Analysis")
            
            if submitted and required_skills:
                analysis_data = {
                    "department": department if department else None,
                    "required_skills": [skill.strip() for skill in required_skills.split(",") if skill.strip()],
                    "experience_level": experience_level,
                    "budget_range": {"min": min_salary, "max": max_salary},
                    "location": location if location else None,
                    "work_type": work_type
                }
                
                result = make_api_request("/analysis/distribute", method="POST", data=analysis_data)
                
                if result:
                    st.markdown('<div class="success-message">🎉 Analysis completed! Found {len(result["matched_candidates"])} matching candidates.</div>', unsafe_allow_html=True)
                    
                    # Display results
                    create_metric_card("Distribution Score", f"{result['distribution_score']:.3f}", "🎯")
                    
                    if result['matched_candidates']:
                        matches_df = pd.DataFrame(result['matched_candidates'])
                        
                        # Match scores chart
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        fig = px.bar(matches_df, x="candidate_name", y="match_score", 
                                    title="🎯 Candidate Match Scores",
                                    labels={"candidate_name": "Candidate", "match_score": "Match Score"},
                                    color_discrete_sequence=['#667eea'])
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#e0e0e0'),
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display recommendations
                        st.markdown("**💡 AI Recommendations:**")
                        for rec in result['recommendations']:
                            st.markdown(f"• {rec}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 💰 Salary Intelligence")
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            job_title = st.text_input("Job Title", value="Software Engineer")
        with col2:
            location = st.text_input("Location", value="US")
        with col3:
            experience_level = st.selectbox("Experience Level", ["Junior", "Mid", "Senior", "Lead"])
        
        if st.button("💰 Get Salary Intelligence"):
            result = make_api_request(f"/analysis/salary-benchmark?job_title={job_title}&location={location}&experience_level={experience_level}")
            
            if result:
                st.markdown('<div class="success-message">💡 Salary intelligence retrieved!</div>', unsafe_allow_html=True)
                
                # Create salary chart
                percentiles = ["25th", "50th", "75th", "90th"]
                values = [result["percentile_25"], result["percentile_50"], 
                         result["percentile_75"], result["percentile_90"]]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=percentiles, y=values, name="Salary Percentiles"))
                fig.add_hline(y=result["market_average"], line_dash="dash", 
                             line_color="red", annotation_text="Market Average")
                
                fig.update_layout(
                    title=f"💰 Salary Benchmark for {job_title} ({experience_level})",
                    xaxis_title="Percentile",
                    yaxis_title="Salary (USD)",
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    create_metric_card("Market Average", f"${result['market_average']:,.0f}", "💰")
                with col2:
                    create_metric_card("50th Percentile", f"${result['percentile_50']:,.0f}", "📊")
                with col3:
                    create_metric_card("90th Percentile", f"${result['percentile_90']:,.0f}", "🏆")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🔍 Skills Gap Intelligence")
        
        # Get candidates for analysis
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        candidates = make_api_request("/candidates/")
        
        if candidates and candidates.get("candidates"):
            candidate_options = {f"{c['first_name']} {c['last_name']}": c['id'] 
                               for c in candidates["candidates"]}
            
            selected_candidates = st.multiselect("Select Candidates for Analysis", 
                                               list(candidate_options.keys()))
            
            focus_skills = st.text_area("Focus Skills (comma-separated, optional)")
            
            if st.button("🔍 Analyze Skills Gaps") and selected_candidates:
                candidate_ids = [candidate_options[name] for name in selected_candidates]
                
                analysis_data = {
                    "candidate_ids": candidate_ids,
                    "focus_skills": [skill.strip() for skill in focus_skills.split(",") if skill.strip()] if focus_skills else None
                }
                
                result = make_api_request("/analysis/skills-gaps", method="POST", data=analysis_data)
                
                if result:
                    st.markdown('<div class="success-message">🎯 Skills gap analysis completed!</div>', unsafe_allow_html=True)
                    
                    # Display skill gaps
                    if result['skill_gaps']:
                        st.markdown("**⚠️ Identified Skill Gaps:**")
                        for skill, candidates_with_gap in result['skill_gaps'].items():
                            st.markdown(f"• **{skill}**: {', '.join(candidates_with_gap)}")
                    
                    # Display top skills
                    if result['top_skills']:
                        st.markdown("**🏆 Top Skills Across Selected Candidates:**")
                        for i, skill in enumerate(result['top_skills'][:10], 1):
                            st.markdown(f"{i}. {skill}")
                    
                    # Display skills matrix
                    if result['candidate_skills_matrix']:
                        st.markdown("**📊 Skills Matrix:**")
                        skills_matrix_df = pd.DataFrame(result['candidate_skills_matrix']).T
                        st.dataframe(skills_matrix_df)
        st.markdown('</div>', unsafe_allow_html=True)

def data_import_section():
    """Data import section with modern design"""
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">📁 Data Intelligence</div>
        <div class="hero-subtitle">Import, analyze, and transform your workforce data</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Data Summary", "🚀 Import Data", "👀 Preview Data"])
    
    with tab1:
        st.markdown("### 📊 Data Intelligence Summary")
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        csv_file_path = st.text_input(
            "CSV File Path", 
            value="WA_Fn-UseC_-HR-Employee-Attrition.csv",
            help="Enter the path to your CSV file"
        )
        
        if st.button("📊 Get Data Summary") and csv_file_path:
            summary = make_api_request(f"/data-import/csv/summary?file_path={csv_file_path}")
            
            if summary:
                st.markdown('<div class="success-message">📊 Data summary retrieved successfully!</div>', unsafe_allow_html=True)
                
                # Display summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    create_metric_card("Total Records", summary["total_records"], "📄")
                
                with col2:
                    create_metric_card("Active Employees", summary["active_employees"], "✅")
                
                with col3:
                    create_metric_card("Attrition Rate", f"{summary['attrition_rate']:.1f}%", "📉")
                
                with col4:
                    create_metric_card("Unique Job Roles", summary["unique_job_roles"], "💼")
                
                # Salary statistics
                st.markdown("### 💰 Salary Intelligence")
                salary_stats = summary["salary_statistics"]
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    create_metric_card("Min Salary", f"${salary_stats['min']:,.0f}", "💰")
                with col2:
                    create_metric_card("Max Salary", f"${salary_stats['max']:,.0f}", "💎")
                with col3:
                    create_metric_card("Mean Salary", f"${salary_stats['mean']:,.0f}", "📊")
                with col4:
                    create_metric_card("Median Salary", f"${salary_stats['median']:,.0f}", "🎯")
                
                # Job roles distribution
                st.markdown("### 🏢 Job Roles Distribution")
                job_roles_df = pd.DataFrame(
                    list(summary["job_roles"].items()),
                    columns=["Job Role", "Count"]
                )
                fig = px.bar(job_roles_df, x="Job Role", y="Count", 
                            title="👥 Employee Distribution by Job Role",
                            color_discrete_sequence=['#667eea'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Departments distribution
                st.markdown("### 📋 Departments Distribution")
                dept_df = pd.DataFrame(
                    list(summary["departments"].items()),
                    columns=["Department", "Count"]
                )
                fig = px.pie(dept_df, values="Count", names="Department", 
                           title="🏢 Employee Distribution by Department",
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0')
                )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🚀 Import Data")
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        csv_file_path = st.text_input(
            "CSV File Path for Import", 
            value="WA_Fn-UseC_-HR-Employee-Attrition.csv",
            help="Enter the path to your CSV file"
        )
        
        if st.button("🚀 Import Data") and csv_file_path:
            with st.spinner("Importing data..."):
                result = make_api_request(
                    f"/data-import/csv/import-from-path?file_path={csv_file_path}",
                    method="POST"
                )
            
            if result:
                st.markdown('<div class="success-message">🎉 Data imported successfully!</div>', unsafe_allow_html=True)
                
                # Display import results
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    create_metric_card("Jobs Created", result["jobs_created"], "💼")
                
                with col2:
                    create_metric_card("Candidates Created", result["candidates_created"], "👥")
                
                with col3:
                    create_metric_card("Skills Created", result["skills_created"], "🎯")
                
                with col4:
                    create_metric_card("Total Records", result["total_records"], "📄")
                
                st.markdown('<div class="success-message">💡 You can now explore the imported data in other sections!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 👀 Data Preview")
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        csv_file_path = st.text_input(
            "CSV File Path for Preview", 
            value="WA_Fn-UseC_-HR-Employee-Attrition.csv",
            help="Enter the path to your CSV file"
        )
        
        rows_to_preview = st.slider("Number of rows to preview", 5, 50, 10)
        
        if st.button("👀 Preview Data") and csv_file_path:
            preview = make_api_request(f"/data-import/csv/preview?file_path={csv_file_path}&rows={rows_to_preview}")
            
            if preview:
                st.markdown('<div class="success-message">👀 Data preview retrieved successfully!</div>', unsafe_allow_html=True)
                
                # Display file info
                col1, col2, col3 = st.columns(3)
                with col1:
                    create_metric_card("Total Rows", preview["total_rows"], "📄")
                with col2:
                    create_metric_card("Total Columns", preview["total_columns"], "📊")
                with col3:
                    create_metric_card("Preview Rows", len(preview["preview_data"]), "👀")
                
                # Display column information
                st.markdown("### 📋 Column Information")
                columns_df = pd.DataFrame(preview["columns_info"])
                st.dataframe(columns_df)
                
                # Display preview data
                st.markdown("### 📄 Preview Data")
                preview_df = pd.DataFrame(preview["preview_data"])
                st.dataframe(preview_df)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application with modern design"""
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2 style="color: #667eea; margin-bottom: 0;">⚡ TalentForge</h2>
        <p style="color: #b8b8b8; font-size: 0.9rem; margin-top: 0;">Pro Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "🚀 Choose Your Destination",
        ["📊 Dashboard", "💼 Jobs Management", "👥 Candidates Management", "📈 Workforce Analysis", "📁 Data Import"]
    )
    
    # Page routing
    if page == "📊 Dashboard":
        main_dashboard()
    elif page == "💼 Jobs Management":
        jobs_management()
    elif page == "👥 Candidates Management":
        candidates_management()
    elif page == "📈 Workforce Analysis":
        workforce_analysis()
    elif page == "📁 Data Import":
        data_import_section()
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🔌 System Status**")
    
    health_check = make_api_request("/health")
    if health_check:
        st.sidebar.markdown('<div style="color: #00b894; font-weight: bold;">✅ API Connected</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div style="color: #e17055; font-weight: bold;">❌ API Disconnected</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🔗 Quick Links**")
    st.sidebar.markdown("[📚 API Documentation](http://localhost:8000/docs)")
    st.sidebar.markdown("[📖 ReDoc Documentation](http://localhost:8000/redoc)")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="color: #b8b8b8; font-size: 0.8rem;">Powered by AI</p>
        <p style="color: #667eea; font-size: 0.7rem;">TalentForge Pro v2.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 