"""
OmniForge: Repository Analyzer
Analyzes repository structure, architecture, and code quality
"""
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import git
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
import ast
import json

logger = logging.getLogger(__name__)

@dataclass
class FileAnalysis:
    """Analysis results for a single file"""
    path: str
    language: str
    lines_of_code: int
    complexity: float
    maintainability: float
    issues: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
@dataclass
class RepositoryAnalysis:
    """Complete repository analysis results"""
    repo_path: str
    total_files: int
    total_lines: int
    languages: Dict[str, int]
    complexity_stats: Dict[str, float]
    maintainability_score: float
    architecture_type: str
    issues: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    file_analyses: List[FileAnalysis] = field(default_factory=list)

class RepositoryAnalyzer:
    """Analyzes repositories for quality, architecture, and issues"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.hpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
        }
        
    def analyze_repository(self, repo_path: str) -> RepositoryAnalysis:
        """
        Perform comprehensive repository analysis
        
        Args:
            repo_path: Path to repository
            
        Returns:
            RepositoryAnalysis object with complete analysis
        """
        logger.info(f"Starting analysis of repository: {repo_path}")
        
        repo_path_obj = Path(repo_path)
        if not repo_path_obj.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        # Initialize analysis
        analysis = RepositoryAnalysis(
            repo_path=repo_path,
            total_files=0,
            total_lines=0,
            languages={},
            complexity_stats={},
            maintainability_score=0.0,
            architecture_type="unknown"
        )
        
        # Collect all source files
        source_files = self._collect_source_files(repo_path_obj)
        analysis.total_files = len(source_files)
        
        # Analyze files in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {
                executor.submit(self._analyze_file, file_path): file_path
                for file_path in source_files
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    file_analysis = future.result()
                    if file_analysis:
                        analysis.file_analyses.append(file_analysis)
                        analysis.total_lines += file_analysis.lines_of_code
                        
                        # Track language usage
                        lang = file_analysis.language
                        analysis.languages[lang] = analysis.languages.get(lang, 0) + 1
                        
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")
        
        # Calculate aggregate metrics
        analysis.complexity_stats = self._calculate_complexity_stats(analysis.file_analyses)
        analysis.maintainability_score = self._calculate_maintainability_score(analysis.file_analyses)
        analysis.architecture_type = self._detect_architecture(repo_path_obj, analysis)
        analysis.issues = self._aggregate_issues(analysis.file_analyses)
        
        logger.info(f"Analysis complete: {analysis.total_files} files, {analysis.total_lines} LOC")
        return analysis
        
    def _collect_source_files(self, repo_path: Path) -> List[Path]:
        """Collect all source files from repository"""
        source_files = []
        ignore_dirs = {'node_modules', '__pycache__', '.git', 'venv', '.venv', 'build', 'dist'}
        
        for root, dirs, files in os.walk(repo_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.supported_extensions:
                    source_files.append(file_path)
        
        return source_files
    
    def _analyze_file(self, file_path: Path) -> Optional[FileAnalysis]:
        """Analyze a single source file"""
        try:
            language = self.supported_extensions.get(file_path.suffix, 'unknown')
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines_of_code = len([line for line in content.split('\n') if line.strip()])
            
            # Python-specific analysis
            if language == 'python':
                return self._analyze_python_file(file_path, content, lines_of_code)
            else:
                # Basic analysis for other languages
                return FileAnalysis(
                    path=str(file_path),
                    language=language,
                    lines_of_code=lines_of_code,
                    complexity=5.0,  # Default complexity
                    maintainability=50.0,  # Default maintainability
                )
                
        except Exception as e:
            logger.warning(f"Could not analyze {file_path}: {e}")
            return None
    
    def _analyze_python_file(self, file_path: Path, content: str, lines_of_code: int) -> FileAnalysis:
        """Analyze Python file with detailed metrics"""
        try:
            # Calculate complexity
            complexity_results = cc_visit(content)
            avg_complexity = sum(c.complexity for c in complexity_results) / len(complexity_results) if complexity_results else 1.0
            
            # Calculate maintainability
            maintainability = mi_visit(content, multi=True)
            avg_maintainability = maintainability if isinstance(maintainability, (int, float)) else 50.0
            
            # Extract dependencies
            dependencies = self._extract_python_dependencies(content)
            
            # Detect issues
            issues = []
            for func in complexity_results:
                if func.complexity > 10:
                    issues.append({
                        'type': 'complexity',
                        'severity': 'high' if func.complexity > 20 else 'medium',
                        'message': f"High complexity in {func.name}: {func.complexity}",
                        'line': func.lineno
                    })
            
            return FileAnalysis(
                path=str(file_path),
                language='python',
                lines_of_code=lines_of_code,
                complexity=avg_complexity,
                maintainability=avg_maintainability,
                issues=issues,
                dependencies=dependencies
            )
            
        except Exception as e:
            logger.warning(f"Error in Python analysis for {file_path}: {e}")
            return FileAnalysis(
                path=str(file_path),
                language='python',
                lines_of_code=lines_of_code,
                complexity=5.0,
                maintainability=50.0
            )
    
    def _extract_python_dependencies(self, content: str) -> List[str]:
        """Extract import statements from Python code"""
        dependencies = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        dependencies.append(name.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.append(node.module.split('.')[0])
        except:
            pass
        return list(set(dependencies))
    
    def _calculate_complexity_stats(self, file_analyses: List[FileAnalysis]) -> Dict[str, float]:
        """Calculate aggregate complexity statistics"""
        if not file_analyses:
            return {'avg': 0.0, 'max': 0.0, 'min': 0.0}
        
        complexities = [f.complexity for f in file_analyses]
        return {
            'avg': sum(complexities) / len(complexities),
            'max': max(complexities),
            'min': min(complexities)
        }
    
    def _calculate_maintainability_score(self, file_analyses: List[FileAnalysis]) -> float:
        """Calculate overall maintainability score"""
        if not file_analyses:
            return 0.0
        
        maintainabilities = [f.maintainability for f in file_analyses]
        return sum(maintainabilities) / len(maintainabilities)
    
    def _detect_architecture(self, repo_path: Path, analysis: RepositoryAnalysis) -> str:
        """Detect architecture pattern from repository structure"""
        # Check for common patterns
        has_src = (repo_path / 'src').exists()
        has_tests = (repo_path / 'tests').exists() or (repo_path / 'test').exists()
        has_package_json = (repo_path / 'package.json').exists()
        has_requirements = (repo_path / 'requirements.txt').exists()
        has_docker = (repo_path / 'Dockerfile').exists()
        
        if has_package_json and (repo_path / 'src' / 'components').exists():
            return 'react-component-based'
        elif has_src and (repo_path / 'src' / 'api').exists():
            return 'api-backend'
        elif has_src and has_tests:
            return 'modular-library'
        elif has_docker:
            return 'containerized-application'
        else:
            return 'standard-project'
    
    def _aggregate_issues(self, file_analyses: List[FileAnalysis]) -> List[Dict[str, Any]]:
        """Aggregate all issues from file analyses"""
        all_issues = []
        for file_analysis in file_analyses:
            for issue in file_analysis.issues:
                issue_copy = issue.copy()
                issue_copy['file'] = file_analysis.path
                all_issues.append(issue_copy)
        
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
        all_issues.sort(key=lambda x: severity_order.get(x.get('severity', 'info'), 5))
        
        return all_issues
    
    def export_analysis(self, analysis: RepositoryAnalysis, output_path: str) -> None:
        """Export analysis to JSON file"""
        output = {
            'repo_path': analysis.repo_path,
            'total_files': analysis.total_files,
            'total_lines': analysis.total_lines,
            'languages': analysis.languages,
            'complexity_stats': analysis.complexity_stats,
            'maintainability_score': analysis.maintainability_score,
            'architecture_type': analysis.architecture_type,
            'issues_count': len(analysis.issues),
            'issues': analysis.issues[:100],  # Limit to first 100 issues
            'file_count_by_language': analysis.languages
        }
        
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Analysis exported to {output_path}")
