# Workforce Distribution.ai - Setup Guide

This guide will help you set up and run the Workforce Distribution.ai project on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation Steps

### 1. Clone and Setup Project

```bash
# Navigate to your project directory
cd "Intel Proj"

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory with the following content:

```env
# Database Configuration
DATABASE_URL=sqlite:///./workforce_ai.db

# Security Configuration
SECRET_KEY=your-secret-key-change-in-production

# API Configuration
DEBUG=False

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8501"]

# AI/ML Configuration
MODEL_PATH=models/
SKILLS_THRESHOLD=0.7
```

### 3. Database Setup

The application uses SQLite by default, which will be created automatically when you first run the backend.

For production, you can change the `DATABASE_URL` to use PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@localhost/workforce_ai
```

### 4. Start the Backend Server

```bash
# Option 1: Use the startup script
python start_backend.py

# Option 2: Run directly with uvicorn
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Start the Streamlit Frontend

```bash
# Option 1: Use the startup script
python start_frontend.py

# Option 2: Run directly with streamlit
streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

The frontend will be available at: http://localhost:8501

### 6. Populate Sample Data (Optional)

To get started quickly with sample data:

```bash
python sample_data.py
```

This will create:
- 3 sample job roles (Software Engineer, Data Scientist, Product Manager)
- 5 sample candidates with various skills and experience levels

## Project Structure

```
workforce-distribution-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── jobs.py
│   │   │       ├── candidates.py
│   │   │       └── analysis.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── job.py
│   │   │   ├── candidate.py
│   │   │   └── skill.py
│   │   ├── schemas/
│   │   │   ├── job.py
│   │   │   ├── candidate.py
│   │   │   └── analysis.py
│   │   ├── services/
│   │   │   ├── skills_assessment.py
│   │   │   └── workforce_analysis.py
│   │   └── main.py
│   └── alembic/
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
├── start_backend.py
├── start_frontend.py
├── sample_data.py
└── README.md
```

## Features Overview

### Backend Features

1. **Job Management**
   - Create, read, update, delete job roles
   - Salary range management
   - Skills requirements tracking
   - Department and level categorization

2. **Candidate Management**
   - Add candidates with skills assessment
   - AI-powered skills scoring
   - Experience and education tracking
   - Availability and preferences management

3. **AI/ML Services**
   - Skills assessment using machine learning
   - Candidate-job matching algorithms
   - Workforce distribution analysis
   - Salary benchmarking

4. **Analysis & Reporting**
   - Workforce distribution optimization
   - Skills gap analysis
   - Market demand analysis
   - Dashboard statistics

### Frontend Features

1. **Dashboard**
   - Overview statistics
   - Education and department distributions
   - Top skilled candidates visualization

2. **Jobs Management**
   - Create and manage job roles
   - Filter and search jobs
   - Market analysis and high-demand jobs

3. **Candidates Management**
   - Add candidates with skills assessment
   - View and filter candidates
   - Skills reassessment tools

4. **Workforce Analysis**
   - Distribution analysis with AI recommendations
   - Salary benchmarking
   - Skills gap analysis across teams

## API Endpoints

### Jobs
- `POST /api/v1/jobs/` - Create job
- `GET /api/v1/jobs/` - List jobs
- `GET /api/v1/jobs/{id}` - Get job details
- `PUT /api/v1/jobs/{id}` - Update job
- `DELETE /api/v1/jobs/{id}` - Delete job

### Candidates
- `POST /api/v1/candidates/` - Add candidate
- `GET /api/v1/candidates/` - List candidates
- `GET /api/v1/candidates/{id}` - Get candidate details
- `PUT /api/v1/candidates/{id}` - Update candidate
- `POST /api/v1/candidates/{id}/assess` - Reassess skills

### Analysis
- `POST /api/v1/analysis/distribute` - Workforce distribution
- `GET /api/v1/analysis/salary-benchmark` - Salary benchmarking
- `POST /api/v1/analysis/skills-gaps` - Skills gap analysis
- `GET /api/v1/analysis/dashboard/stats` - Dashboard statistics

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   
   # Or use different port
   uvicorn app.main:app --port 8001
   ```

2. **Database connection issues**
   - Check if the database file exists
   - Ensure write permissions in the directory
   - For PostgreSQL, verify connection credentials

3. **Frontend not connecting to backend**
   - Verify backend is running on http://localhost:8000
   - Check CORS settings in backend configuration
   - Ensure no firewall blocking the connection

4. **Import errors**
   ```bash
   # Make sure you're in the correct directory
   cd backend
   python -m app.main
   ```

### Development Tips

1. **Enable debug mode**
   ```env
   DEBUG=True
   ```

2. **Use different database for development**
   ```env
   DATABASE_URL=sqlite:///./dev_workforce_ai.db
   ```

3. **Hot reload for development**
   ```bash
   uvicorn app.main:app --reload
   ```

## Production Deployment

For production deployment, consider:

1. **Database**: Use PostgreSQL instead of SQLite
2. **Security**: Change default secret key
3. **Environment**: Set DEBUG=False
4. **CORS**: Configure allowed origins properly
5. **SSL**: Use HTTPS in production
6. **Process Management**: Use Gunicorn or similar

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the API documentation at http://localhost:8000/docs
- Review the code comments and docstrings
- Create an issue in the repository 