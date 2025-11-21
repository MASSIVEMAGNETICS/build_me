"""
OmniForge: The Absolute Upgrade Engine
Core configuration and constants
"""
from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel, Field

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Analysis configuration
class AnalysisConfig(BaseModel):
    """Configuration for code analysis"""
    max_file_size_mb: int = Field(default=10, description="Max file size to analyze")
    supported_languages: List[str] = Field(
        default=["python", "javascript", "typescript", "java", "go", "rust", "cpp"],
        description="Languages to analyze"
    )
    complexity_threshold: int = Field(default=10, description="Max cyclomatic complexity")
    maintainability_threshold: float = Field(default=20.0, description="Min maintainability index")
    security_scan_enabled: bool = Field(default=True, description="Enable security scanning")
    
class UpgradeConfig(BaseModel):
    """Configuration for code upgrading"""
    preserve_comments: bool = Field(default=True, description="Preserve code comments")
    auto_format: bool = Field(default=True, description="Auto format upgraded code")
    create_backups: bool = Field(default=True, description="Create backups before upgrade")
    min_test_coverage: float = Field(default=80.0, description="Minimum test coverage %")
    
class SystemConfig(BaseModel):
    """Global system configuration"""
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    upgrade: UpgradeConfig = Field(default_factory=UpgradeConfig)
    debug_mode: bool = Field(default=False, description="Enable debug logging")
    parallel_workers: int = Field(default=4, description="Number of parallel workers")
    cache_enabled: bool = Field(default=True, description="Enable result caching")

# Severity levels
SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"
SEVERITY_INFO = "info"

# File patterns to ignore
IGNORE_PATTERNS = [
    "node_modules/",
    "__pycache__/",
    ".git/",
    ".venv/",
    "venv/",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".DS_Store",
    "*.swp",
    "*.swo",
    ".coverage",
    "htmlcov/",
    "dist/",
    "build/",
    "*.egg-info/",
]

# Default configuration instance
DEFAULT_CONFIG = SystemConfig()
