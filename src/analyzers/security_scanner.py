"""
OmniForge: Security Scanner
Scans code for security vulnerabilities and issues
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import re
import subprocess
import json

logger = logging.getLogger(__name__)

@dataclass
class SecurityIssue:
    """Security vulnerability or issue"""
    severity: str  # critical, high, medium, low
    type: str
    file: str
    line: Optional[int]
    description: str
    recommendation: str
    cwe_id: Optional[str] = None

@dataclass
class SecurityScanResult:
    """Results from security scan"""
    total_issues: int
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    issues: List[SecurityIssue] = field(default_factory=list)

class SecurityScanner:
    """Scans code for security vulnerabilities"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # Common security patterns
        self.patterns = {
            'hardcoded_secret': [
                (r'password\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded password detected'),
                (r'api_key\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded API key detected'),
                (r'secret\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded secret detected'),
            ],
            'sql_injection': [
                (r'execute\s*\(\s*["\'].*%s.*["\']', 'Potential SQL injection vulnerability'),
                (r'executemany\s*\(\s*["\'].*%s.*["\']', 'Potential SQL injection vulnerability'),
            ],
            'command_injection': [
                (r'os\.system\s*\(', 'Use of os.system can lead to command injection'),
                (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', 'Shell=True can lead to command injection'),
            ],
            'path_traversal': [
                (r'open\s*\(\s*.*\+.*\)', 'Potential path traversal in file operations'),
            ],
            'weak_crypto': [
                (r'md5\(', 'MD5 is cryptographically broken'),
                (r'sha1\(', 'SHA1 is cryptographically weak'),
            ],
        }
    
    def scan_file(self, file_path: str) -> List[SecurityIssue]:
        """
        Scan a single file for security issues
        
        Args:
            file_path: Path to file to scan
            
        Returns:
            List of SecurityIssue objects
        """
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Pattern-based scanning
            for issue_type, patterns in self.patterns.items():
                for pattern, description in patterns:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            severity = self._determine_severity(issue_type)
                            issues.append(SecurityIssue(
                                severity=severity,
                                type=issue_type,
                                file=file_path,
                                line=line_num,
                                description=description,
                                recommendation=self._get_recommendation(issue_type)
                            ))
            
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
        
        return issues
    
    def scan_repository(self, repo_path: str) -> SecurityScanResult:
        """
        Scan entire repository for security issues
        
        Args:
            repo_path: Path to repository
            
        Returns:
            SecurityScanResult with all findings
        """
        logger.info(f"Starting security scan of {repo_path}")
        
        all_issues = []
        repo_path_obj = Path(repo_path)
        
        # Scan Python files
        for py_file in repo_path_obj.rglob('*.py'):
            if self._should_scan_file(py_file):
                issues = self.scan_file(str(py_file))
                all_issues.extend(issues)
        
        # Scan JavaScript/TypeScript files
        for js_file in list(repo_path_obj.rglob('*.js')) + list(repo_path_obj.rglob('*.ts')):
            if self._should_scan_file(js_file):
                issues = self.scan_file(str(js_file))
                all_issues.extend(issues)
        
        # Aggregate results
        result = SecurityScanResult(total_issues=len(all_issues))
        
        for issue in all_issues:
            if issue.severity == 'critical':
                result.critical += 1
            elif issue.severity == 'high':
                result.high += 1
            elif issue.severity == 'medium':
                result.medium += 1
            elif issue.severity == 'low':
                result.low += 1
        
        result.issues = all_issues
        
        logger.info(f"Security scan complete: {result.total_issues} issues found")
        return result
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned"""
        ignore_dirs = {'node_modules', '__pycache__', '.git', 'venv', '.venv', 'test', 'tests'}
        
        for parent in file_path.parents:
            if parent.name in ignore_dirs:
                return False
        
        return True
    
    def _determine_severity(self, issue_type: str) -> str:
        """Determine severity based on issue type"""
        severity_map = {
            'hardcoded_secret': 'critical',
            'sql_injection': 'critical',
            'command_injection': 'high',
            'path_traversal': 'high',
            'weak_crypto': 'medium',
        }
        return severity_map.get(issue_type, 'medium')
    
    def _get_recommendation(self, issue_type: str) -> str:
        """Get recommendation for fixing issue"""
        recommendations = {
            'hardcoded_secret': 'Use environment variables or a secret management system',
            'sql_injection': 'Use parameterized queries or an ORM',
            'command_injection': 'Avoid shell=True, use list arguments, validate inputs',
            'path_traversal': 'Validate and sanitize file paths, use os.path.join safely',
            'weak_crypto': 'Use SHA-256 or stronger algorithms',
        }
        return recommendations.get(issue_type, 'Review and fix the security issue')
    
    def export_report(self, result: SecurityScanResult, output_path: str) -> None:
        """Export security scan report to JSON"""
        report = {
            'summary': {
                'total_issues': result.total_issues,
                'critical': result.critical,
                'high': result.high,
                'medium': result.medium,
                'low': result.low,
            },
            'issues': [
                {
                    'severity': issue.severity,
                    'type': issue.type,
                    'file': issue.file,
                    'line': issue.line,
                    'description': issue.description,
                    'recommendation': issue.recommendation,
                }
                for issue in result.issues
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Security report exported to {output_path}")
