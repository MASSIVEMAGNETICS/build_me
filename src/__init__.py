"""
OmniForge Package
Main entry point for the application
"""

__version__ = "1.0.0"
__author__ = "OmniForge Team"
__description__ = "The Absolute Upgrade Engine - Repository Analysis and Transformation"

from src.core.engine import OmniForgeEngine
from src.core.config import SystemConfig

__all__ = ['OmniForgeEngine', 'SystemConfig']
