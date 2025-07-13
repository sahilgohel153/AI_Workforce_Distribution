# Workforce Distribution.ai

An AI-powered workforce management and distribution system that helps organizations optimize their human resources allocation, analyze job roles, salaries, and candidate skills.

## Features

- **Job Role Management**: Create, update, and manage job roles with detailed requirements
- **Salary Analysis**: Comprehensive salary benchmarking and analysis tools
- **Skills Assessment**: AI-powered candidate skills evaluation and rating
- **Workforce Distribution**: Intelligent allocation of resources based on skills and requirements
- **Streamlit Integration**: User-friendly web interface for data visualization and interaction
- **RESTful API**: Complete backend API for seamless integration

## Project Structure

```
workforce-distribution-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── alembic/
│   └── tests/
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
└── README.md
```

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database and API configurations
   ```

3. **Run Database Migrations**:
   ```bash
   cd backend
   alembic upgrade head
   ```

4. **Start the Backend Server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Start the Streamlit Frontend**:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Key Endpoints

- `POST /api/v1/jobs/` - Create new job role
- `GET /api/v1/jobs/` - List all job roles
- `POST /api/v1/candidates/` - Add candidate with skills
- `GET /api/v1/candidates/` - List all candidates
- `POST /api/v1/analysis/distribute` - Analyze workforce distribution
- `GET /api/v1/analysis/salary-benchmark` - Get salary benchmarks

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **AI/ML**: scikit-learn, pandas, numpy
- **Frontend**: Streamlit
- **Authentication**: JWT tokens
- **Database**: PostgreSQL with Alembic migrations 