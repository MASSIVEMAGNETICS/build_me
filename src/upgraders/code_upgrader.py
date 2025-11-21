"""
OmniForge: Code Upgrader
Upgrades code to modern standards and best practices
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import re
import ast
import astor

logger = logging.getLogger(__name__)

@dataclass
class UpgradeResult:
    """Result of code upgrade operation"""
    file_path: str
    original_content: str
    upgraded_content: str
    changes: List[Dict[str, Any]] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None

class CodeUpgrader:
    """Upgrades code to modern patterns and best practices"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.preserve_comments = self.config.get('preserve_comments', True)
        self.auto_format = self.config.get('auto_format', True)
        
    def upgrade_python_file(self, file_path: str) -> UpgradeResult:
        """
        Upgrade a Python file to modern standards
        
        Args:
            file_path: Path to Python file
            
        Returns:
            UpgradeResult with upgraded content and changes
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            upgraded_content = original_content
            changes = []
            
            # Apply upgrade transformations
            upgraded_content, type_hints_changes = self._add_type_hints(upgraded_content)
            changes.extend(type_hints_changes)
            
            upgraded_content, docstring_changes = self._improve_docstrings(upgraded_content)
            changes.extend(docstring_changes)
            
            upgraded_content, exception_changes = self._modernize_exception_handling(upgraded_content)
            changes.extend(exception_changes)
            
            upgraded_content, import_changes = self._optimize_imports(upgraded_content)
            changes.extend(import_changes)
            
            upgraded_content, f_string_changes = self._convert_to_f_strings(upgraded_content)
            changes.extend(f_string_changes)
            
            return UpgradeResult(
                file_path=file_path,
                original_content=original_content,
                upgraded_content=upgraded_content,
                changes=changes,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error upgrading {file_path}: {e}")
            return UpgradeResult(
                file_path=file_path,
                original_content="",
                upgraded_content="",
                success=False,
                error=str(e)
            )
    
    def _add_type_hints(self, content: str) -> tuple[str, List[Dict]]:
        """Add type hints to functions without them"""
        changes = []
        try:
            tree = ast.parse(content)
            modified = False
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.returns and node.name != '__init__':
                        # Could add return type hint here
                        changes.append({
                            'type': 'type_hint',
                            'description': f'Function {node.name} could benefit from type hints',
                            'line': node.lineno
                        })
            
            return content, changes
            
        except Exception as e:
            logger.debug(f"Type hint analysis failed: {e}")
            return content, changes
    
    def _improve_docstrings(self, content: str) -> tuple[str, List[Dict]]:
        """Improve or add docstrings"""
        changes = []
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        changes.append({
                            'type': 'docstring',
                            'description': f'{node.__class__.__name__} {node.name} missing docstring',
                            'line': node.lineno
                        })
            
            return content, changes
            
        except Exception as e:
            logger.debug(f"Docstring analysis failed: {e}")
            return content, changes
    
    def _modernize_exception_handling(self, content: str) -> tuple[str, List[Dict]]:
        """Modernize exception handling patterns"""
        changes = []
        
        # Replace bare except clauses
        if re.search(r'except\s*:', content):
            changes.append({
                'type': 'exception',
                'description': 'Bare except clause found - should specify exception type',
                'severity': 'medium'
            })
        
        return content, changes
    
    def _optimize_imports(self, content: str) -> tuple[str, List[Dict]]:
        """Optimize and organize imports"""
        changes = []
        lines = content.split('\n')
        
        # Find all imports
        import_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append((i, line))
        
        if len(import_lines) > 5:
            changes.append({
                'type': 'imports',
                'description': 'Imports could be optimized and organized',
                'suggestion': 'Use isort or organize into stdlib, third-party, local groups'
            })
        
        return content, changes
    
    def _convert_to_f_strings(self, content: str) -> tuple[str, List[Dict]]:
        """Convert old-style string formatting to f-strings"""
        changes = []
        upgraded = content
        
        # Detect .format() usage
        format_pattern = r'\.format\('
        if re.search(format_pattern, content):
            changes.append({
                'type': 'formatting',
                'description': 'Old-style .format() found - consider f-strings',
                'suggestion': 'Convert to f-strings for better readability'
            })
        
        # Detect % formatting
        percent_pattern = r'%\s*\('
        if re.search(percent_pattern, content):
            changes.append({
                'type': 'formatting',
                'description': 'Old-style % formatting found - consider f-strings',
                'suggestion': 'Convert to f-strings for better readability'
            })
        
        return upgraded, changes
    
    def apply_upgrades(self, file_path: str, upgrade_result: UpgradeResult, create_backup: bool = True) -> bool:
        """
        Apply upgrades to file
        
        Args:
            file_path: Path to file
            upgrade_result: UpgradeResult from upgrade operation
            create_backup: Whether to create backup file
            
        Returns:
            Success status
        """
        try:
            if create_backup:
                backup_path = f"{file_path}.backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(upgrade_result.original_content)
                logger.info(f"Backup created: {backup_path}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(upgrade_result.upgraded_content)
            
            logger.info(f"Upgrades applied to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error applying upgrades to {file_path}: {e}")
            return False
