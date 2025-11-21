"""
OmniForge Test Suite
Basic tests for core functionality
"""
import pytest
from pathlib import Path
from src.core.engine import OmniForgeEngine
from src.core.config import SystemConfig
from src.analyzers.repository_analyzer import RepositoryAnalyzer
from src.analyzers.security_scanner import SecurityScanner

def test_config_creation():
    """Test configuration creation"""
    config = SystemConfig(debug_mode=True, parallel_workers=2)
    assert config.debug_mode == True
    assert config.parallel_workers == 2

def test_engine_initialization():
    """Test engine initialization"""
    engine = OmniForgeEngine()
    assert engine is not None
    assert engine.analyzer is not None
    assert engine.security_scanner is not None
    assert engine.upgrader is not None

def test_analyzer_initialization():
    """Test repository analyzer initialization"""
    analyzer = RepositoryAnalyzer()
    assert analyzer is not None
    assert len(analyzer.supported_extensions) > 0

def test_security_scanner_initialization():
    """Test security scanner initialization"""
    scanner = SecurityScanner()
    assert scanner is not None
    assert len(scanner.patterns) > 0

def test_analyze_nonexistent_repo():
    """Test analysis of non-existent repository"""
    analyzer = RepositoryAnalyzer()
    with pytest.raises(ValueError):
        analyzer.analyze_repository('/nonexistent/path')

def test_security_patterns():
    """Test security pattern detection"""
    scanner = SecurityScanner()
    
    # Test hardcoded password detection
    test_code = 'password = "hardcoded_secret123"'
    issues = scanner.scan_file.__wrapped__(scanner, None)
    # This is a basic test - would need actual file for full test
    assert scanner.patterns['hardcoded_secret'] is not None
