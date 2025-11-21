"""
OmniForge: FastAPI Server
Production-grade API server with error handling and monitoring
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
import logging
import tempfile
import shutil
from pathlib import Path
import uuid

from src.core.engine import OmniForgeEngine, TransformationReport
from src.core.config import SystemConfig, DEFAULT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="OmniForge API",
    description="The Absolute Upgrade Engine - Repository Analysis and Transformation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
engine = OmniForgeEngine(config=DEFAULT_CONFIG)

# In-memory job storage (use Redis/DB in production)
jobs: Dict[str, Dict[str, Any]] = {}

# Request/Response Models
class AnalysisRequest(BaseModel):
    """Request model for repository analysis"""
    repo_path: str = Field(..., description="Path to repository to analyze")
    
class AnalysisResponse(BaseModel):
    """Response model for analysis results"""
    job_id: str
    status: str
    message: str

class JobStatus(BaseModel):
    """Job status response"""
    job_id: str
    status: str  # pending, running, completed, failed
    progress: int
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "OmniForge",
        "version": "1.0.0"
    }

# Main analysis endpoint
@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Analyze a repository and generate transformation report
    
    This endpoint starts an asynchronous analysis job.
    Use /api/jobs/{job_id} to check status and get results.
    """
    try:
        # Validate repository path
        repo_path = Path(request.repo_path)
        if not repo_path.exists():
            raise HTTPException(status_code=400, detail="Repository path does not exist")
        
        # Create job
        job_id = str(uuid.uuid4())
        jobs[job_id] = {
            "status": "pending",
            "progress": 0,
            "result": None,
            "error": None
        }
        
        # Start background analysis
        background_tasks.add_task(run_analysis, job_id, str(repo_path))
        
        return AnalysisResponse(
            job_id=job_id,
            status="pending",
            message="Analysis job started"
        )
        
    except Exception as e:
        logger.error(f"Error starting analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Job status endpoint
@app.get("/api/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get status of an analysis job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return JobStatus(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        result=job["result"],
        error=job["error"]
    )

# Quick analysis endpoint (synchronous, for small repos)
@app.post("/api/analyze-sync")
async def analyze_repository_sync(request: AnalysisRequest):
    """
    Synchronous repository analysis (for small repositories)
    
    Warning: This endpoint may timeout for large repositories.
    Use /api/analyze for asynchronous processing.
    """
    try:
        repo_path = Path(request.repo_path)
        if not repo_path.exists():
            raise HTTPException(status_code=400, detail="Repository path does not exist")
        
        # Run analysis
        report = engine.analyze_repository(str(repo_path))
        
        # Generate summary
        summary = engine.generate_summary(report)
        
        return {
            "status": "completed",
            "report": {
                "timestamp": report.timestamp,
                "repository_path": report.repository_path,
                "success": report.success,
                "analysis": report.analysis,
                "security_scan": report.security_scan,
                "recommendations": report.recommendations,
                "upgrades": report.upgrades
            },
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error in synchronous analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# System info endpoint
@app.get("/api/info")
async def get_system_info():
    """Get OmniForge system information"""
    return {
        "name": "OmniForge",
        "version": "1.0.0",
        "description": "The Absolute Upgrade Engine",
        "features": [
            "Repository analysis",
            "Security scanning",
            "Code quality metrics",
            "Architecture detection",
            "Upgrade recommendations",
            "Self-healing capabilities"
        ],
        "supported_languages": [
            "Python",
            "JavaScript",
            "TypeScript",
            "Java",
            "Go",
            "Rust",
            "C/C++"
        ]
    }

# Configuration endpoint
@app.get("/api/config")
async def get_config():
    """Get current system configuration"""
    return {
        "analysis": engine.config.analysis.dict(),
        "upgrade": engine.config.upgrade.dict(),
        "debug_mode": engine.config.debug_mode,
        "parallel_workers": engine.config.parallel_workers
    }

# Background task function
async def run_analysis(job_id: str, repo_path: str):
    """Background task for running analysis"""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["progress"] = 10
        
        # Run analysis
        report = engine.analyze_repository(repo_path)
        
        jobs[job_id]["progress"] = 90
        
        # Generate summary
        summary = engine.generate_summary(report)
        
        # Update job with results
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["result"] = {
            "timestamp": report.timestamp,
            "repository_path": report.repository_path,
            "success": report.success,
            "analysis": report.analysis,
            "security_scan": report.security_scan,
            "recommendations": report.recommendations,
            "upgrades": report.upgrades,
            "summary": summary
        }
        
        logger.info(f"Analysis job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Analysis job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
