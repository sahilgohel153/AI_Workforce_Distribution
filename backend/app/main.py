from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .core.database import engine, Base
from .api.endpoints import jobs, candidates, analysis, data_import

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered workforce management and distribution system",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(
    jobs.router,
    prefix=f"{settings.api_v1_prefix}/jobs",
    tags=["Jobs"]
)

app.include_router(
    candidates.router,
    prefix=f"{settings.api_v1_prefix}/candidates",
    tags=["Candidates"]
)

app.include_router(
    analysis.router,
    prefix=f"{settings.api_v1_prefix}/analysis",
    tags=["Analysis"]
)

app.include_router(
    data_import.router,
    prefix=f"{settings.api_v1_prefix}/data-import",
    tags=["Data Import"]
)

from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

app.include_router(router)

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Workforce Distribution.ai API",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    """
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 