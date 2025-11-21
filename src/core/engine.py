"""
OmniForge: Main Engine
Orchestrates analysis, upgrading, and transformation
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
from datetime import datetime

from src.analyzers.repository_analyzer import RepositoryAnalyzer, RepositoryAnalysis
from src.analyzers.security_scanner import SecurityScanner, SecurityScanResult
from src.upgraders.code_upgrader import CodeUpgrader, UpgradeResult
from src.core.config import SystemConfig, DEFAULT_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TransformationReport:
    """Complete transformation report"""
    timestamp: str
    repository_path: str
    analysis: Dict[str, Any]
    security_scan: Dict[str, Any]
    upgrades: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    success: bool = True

class OmniForgeEngine:
    """
    The Absolute Upgrade Engine
    Orchestrates repository analysis, security scanning, and code upgrading
    """
    
    def __init__(self, config: Optional[SystemConfig] = None):
        self.config = config or DEFAULT_CONFIG
        self.analyzer = RepositoryAnalyzer(config=self.config.analysis.dict())
        self.security_scanner = SecurityScanner()
        self.upgrader = CodeUpgrader(config=self.config.upgrade.dict())
        
        logger.info("OmniForge Engine initialized")
    
    def analyze_repository(self, repo_path: str) -> TransformationReport:
        """
        Perform complete repository analysis and transformation
        
        Args:
            repo_path: Path to repository to analyze
            
        Returns:
            TransformationReport with complete analysis and recommendations
        """
        logger.info(f"Starting OmniForge transformation for: {repo_path}")
        
        # Initialize report
        report = TransformationReport(
            timestamp=datetime.now().isoformat(),
            repository_path=repo_path,
            analysis={},
            security_scan={}
        )
        
        try:
            # Step 1: Repository Analysis
            logger.info("Step 1: Analyzing repository structure and code quality...")
            repo_analysis = self.analyzer.analyze_repository(repo_path)
            report.analysis = self._serialize_analysis(repo_analysis)
            
            # Step 2: Security Scan
            logger.info("Step 2: Scanning for security vulnerabilities...")
            security_result = self.security_scanner.scan_repository(repo_path)
            report.security_scan = self._serialize_security_scan(security_result)
            
            # Step 3: Generate Recommendations
            logger.info("Step 3: Generating recommendations...")
            report.recommendations = self._generate_recommendations(repo_analysis, security_result)
            
            # Step 4: Optional Code Upgrades
            logger.info("Step 4: Identifying upgrade opportunities...")
            upgrade_suggestions = self._identify_upgrades(repo_analysis)
            report.upgrades = upgrade_suggestions
            
            report.success = True
            logger.info("OmniForge transformation complete!")
            
        except Exception as e:
            logger.error(f"Error during transformation: {e}")
            report.success = False
            report.recommendations.append(f"Error occurred: {str(e)}")
        
        return report
    
    def _serialize_analysis(self, analysis: RepositoryAnalysis) -> Dict[str, Any]:
        """Convert RepositoryAnalysis to dictionary"""
        return {
            'total_files': analysis.total_files,
            'total_lines': analysis.total_lines,
            'languages': analysis.languages,
            'complexity_stats': analysis.complexity_stats,
            'maintainability_score': analysis.maintainability_score,
            'architecture_type': analysis.architecture_type,
            'issues_count': len(analysis.issues),
            'top_issues': analysis.issues[:10]
        }
    
    def _serialize_security_scan(self, scan_result: SecurityScanResult) -> Dict[str, Any]:
        """Convert SecurityScanResult to dictionary"""
        return {
            'total_issues': scan_result.total_issues,
            'critical': scan_result.critical,
            'high': scan_result.high,
            'medium': scan_result.medium,
            'low': scan_result.low,
            'top_issues': [
                {
                    'severity': issue.severity,
                    'type': issue.type,
                    'file': issue.file,
                    'description': issue.description
                }
                for issue in scan_result.issues[:10]
            ]
        }
    
    def _generate_recommendations(
        self, 
        analysis: RepositoryAnalysis, 
        security: SecurityScanResult
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Architecture recommendations
        if analysis.architecture_type == 'unknown':
            recommendations.append(
                "Consider organizing code into a clear architecture pattern (MVC, layered, microservices)"
            )
        
        # Complexity recommendations
        if analysis.complexity_stats.get('avg', 0) > 10:
            recommendations.append(
                f"Average complexity is {analysis.complexity_stats['avg']:.1f}. "
                "Refactor complex functions into smaller, more maintainable units."
            )
        
        # Maintainability recommendations
        if analysis.maintainability_score < 50:
            recommendations.append(
                f"Maintainability score is {analysis.maintainability_score:.1f}. "
                "Add documentation, improve naming, and reduce code duplication."
            )
        
        # Security recommendations
        if security.critical > 0:
            recommendations.append(
                f"CRITICAL: {security.critical} critical security issues found. "
                "Address these immediately before deployment."
            )
        
        if security.high > 0:
            recommendations.append(
                f"HIGH: {security.high} high-severity security issues found. "
                "Review and fix these issues as soon as possible."
            )
        
        # Testing recommendations
        test_files = sum(1 for f in analysis.file_analyses if 'test' in f.path.lower())
        if test_files == 0:
            recommendations.append(
                "No test files detected. Add comprehensive unit and integration tests."
            )
        
        # Documentation recommendations
        if not any('README' in f.path for f in analysis.file_analyses):
            recommendations.append(
                "Add a comprehensive README with setup instructions and documentation."
            )
        
        return recommendations
    
    def _identify_upgrades(self, analysis: RepositoryAnalysis) -> List[Dict[str, Any]]:
        """Identify potential code upgrades"""
        upgrades = []
        
        for file_analysis in analysis.file_analyses:
            if file_analysis.language == 'python':
                upgrades.append({
                    'file': file_analysis.path,
                    'type': 'modernization',
                    'suggestions': [
                        'Add type hints for better IDE support',
                        'Convert to f-strings for string formatting',
                        'Add comprehensive docstrings',
                        'Use dataclasses for data structures'
                    ]
                })
        
        return upgrades[:10]  # Limit to top 10
    
    def export_report(self, report: TransformationReport, output_path: str) -> None:
        """Export transformation report to JSON file"""
        report_dict = {
            'timestamp': report.timestamp,
            'repository_path': report.repository_path,
            'success': report.success,
            'analysis': report.analysis,
            'security_scan': report.security_scan,
            'recommendations': report.recommendations,
            'upgrades': report.upgrades
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        logger.info(f"Transformation report exported to {output_path}")
    
    def generate_summary(self, report: TransformationReport) -> str:
        """Generate human-readable summary"""
        lines = [
            "=" * 60,
            "OMNIFORGE TRANSFORMATION REPORT",
            "=" * 60,
            f"Repository: {report.repository_path}",
            f"Timestamp: {report.timestamp}",
            "",
            "CODE ANALYSIS",
            "-" * 60,
            f"Total Files: {report.analysis.get('total_files', 0)}",
            f"Total Lines: {report.analysis.get('total_lines', 0)}",
            f"Languages: {', '.join(report.analysis.get('languages', {}).keys())}",
            f"Architecture: {report.analysis.get('architecture_type', 'unknown')}",
            f"Maintainability: {report.analysis.get('maintainability_score', 0):.1f}/100",
            f"Avg Complexity: {report.analysis.get('complexity_stats', {}).get('avg', 0):.1f}",
            "",
            "SECURITY SCAN",
            "-" * 60,
            f"Total Issues: {report.security_scan.get('total_issues', 0)}",
            f"  Critical: {report.security_scan.get('critical', 0)}",
            f"  High: {report.security_scan.get('high', 0)}",
            f"  Medium: {report.security_scan.get('medium', 0)}",
            f"  Low: {report.security_scan.get('low', 0)}",
            "",
            "RECOMMENDATIONS",
            "-" * 60,
        ]
        
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}")
        
        lines.extend([
            "",
            "=" * 60,
        ])
        
        return "\n".join(lines)
