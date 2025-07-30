"""
Static analysis module for Python code quality assessment.

This module provides comprehensive Python code analysis using multiple tools:
- flake8: Style and syntax checking
- pylint: Code quality and best practices
- mypy: Type checking and annotations
- AST analysis: Code structure and complexity
"""

import ast
import logging
import subprocess
import tempfile
import os
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class StaticAnalyzer:
    """Comprehensive Python static analysis using multiple tools."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the static analyzer.
        
        Args:
            config: Optional configuration for analysis tools
        """
        self.config = config or {}
        self.tools_available = self._check_tool_availability()
        logger.info(f"Static analyzer initialized with tools: {list(self.tools_available.keys())}")
    
    def _check_tool_availability(self) -> Dict[str, bool]:
        """Check which analysis tools are available."""
        tools = {}
        
        # Check flake8
        try:
            result = subprocess.run(['flake8', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            tools['flake8'] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            tools['flake8'] = False
        
        # Check pylint
        try:
            result = subprocess.run(['pylint', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            tools['pylint'] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            tools['pylint'] = False
        
        # Check mypy
        try:
            result = subprocess.run(['mypy', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            tools['mypy'] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            tools['mypy'] = False
        
        return tools
    
    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary containing all analysis results
        """
        if not os.path.exists(file_path) or not file_path.endswith('.py'):
            return {'error': 'Invalid Python file path'}
        
        analysis_results = {
            'file_path': file_path,
            'analysis_timestamp': str(datetime.now() if 'datetime' in globals() else 'unknown'),
            'tools_used': [],
            'flake8_analysis': {},
            'pylint_analysis': {},
            'mypy_analysis': {},
            'ast_analysis': {},
            'summary': {}
        }
        
        # Read source code for AST analysis
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            analysis_results['source_length'] = len(source_code)
        except Exception as e:
            logger.error(f"Could not read source file {file_path}: {e}")
            analysis_results['error'] = str(e)
            return analysis_results
        
        # Run flake8 analysis
        if self.tools_available.get('flake8', False):
            analysis_results['flake8_analysis'] = self._run_flake8(file_path)
            analysis_results['tools_used'].append('flake8')
        
        # Run pylint analysis
        if self.tools_available.get('pylint', False):
            analysis_results['pylint_analysis'] = self._run_pylint(file_path)
            analysis_results['tools_used'].append('pylint')
        
        # Run mypy analysis
        if self.tools_available.get('mypy', False):
            analysis_results['mypy_analysis'] = self._run_mypy(file_path)
            analysis_results['tools_used'].append('mypy')
        
        # Run AST analysis
        analysis_results['ast_analysis'] = self._analyze_ast(source_code)
        analysis_results['tools_used'].append('ast_analysis')
        
        # Generate summary
        analysis_results['summary'] = self._generate_summary(analysis_results)
        
        return analysis_results
    
    def _run_flake8(self, file_path: str) -> Dict[str, Any]:
        """Run flake8 analysis on a Python file."""
        try:
            # Run flake8 with JSON output if possible, otherwise parse text
            result = subprocess.run([
                'flake8', 
                '--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s',
                '--max-line-length=88',  # More modern line length
                '--extend-ignore=E203,W503',  # Common false positives
                file_path
            ], capture_output=True, text=True, timeout=30)
            
            flake8_result = {
                'return_code': result.returncode,
                'issues': [],
                'summary': {'errors': 0, 'warnings': 0, 'total_issues': 0}
            }
            
            if result.stdout:
                lines = result.stdout.strip().split('\\n')
                for line in lines:
                    if ':' in line and file_path in line:
                        parts = line.split(': ', 1)
                        if len(parts) == 2:
                            location, issue = parts
                            location_parts = location.split(':')
                            if len(location_parts) >= 3:
                                flake8_result['issues'].append({
                                    'line': int(location_parts[-2]) if location_parts[-2].isdigit() else 0,
                                    'column': int(location_parts[-1]) if location_parts[-1].isdigit() else 0,
                                    'message': issue.strip(),
                                    'code': issue.split()[0] if issue else 'UNKNOWN'
                                })
                
                # Categorize issues
                for issue in flake8_result['issues']:
                    code = issue.get('code', '')
                    if code.startswith('E'):
                        flake8_result['summary']['errors'] += 1
                    elif code.startswith('W'):
                        flake8_result['summary']['warnings'] += 1
                
                flake8_result['summary']['total_issues'] = len(flake8_result['issues'])
            
            return flake8_result
        
        except subprocess.TimeoutExpired:
            logger.warning(f"flake8 analysis timed out for {file_path}")
            return {'error': 'Analysis timed out', 'timeout': True}
        except Exception as e:
            logger.error(f"flake8 analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _run_pylint(self, file_path: str) -> Dict[str, Any]:
        """Run pylint analysis on a Python file."""
        try:
            # Run pylint with JSON output
            result = subprocess.run([
                'pylint',
                '--output-format=json',
                '--disable=C0114,C0115,C0116',  # Disable missing docstring warnings
                '--max-line-length=88',
                file_path
            ], capture_output=True, text=True, timeout=60)
            
            pylint_result = {
                'return_code': result.returncode,
                'score': 0.0,
                'issues': [],
                'summary': {'convention': 0, 'refactor': 0, 'warning': 0, 'error': 0, 'fatal': 0}
            }
            
            # Parse JSON output
            if result.stdout:
                try:
                    issues = json.loads(result.stdout)
                    pylint_result['issues'] = issues
                    
                    # Categorize issues
                    for issue in issues:
                        issue_type = issue.get('type', 'unknown')
                        if issue_type in pylint_result['summary']:
                            pylint_result['summary'][issue_type] += 1
                
                except json.JSONDecodeError:
                    # Fallback to text parsing if JSON fails
                    lines = result.stdout.split('\\n')
                    for line in lines:
                        if 'Your code has been rated at' in line:
                            try:
                                score_part = line.split('rated at ')[1].split('/')[0]
                                pylint_result['score'] = float(score_part)
                            except (IndexError, ValueError):
                                pass
            
            # Extract score from stderr if not found in stdout
            if pylint_result['score'] == 0.0 and result.stderr:
                lines = result.stderr.split('\\n')
                for line in lines:
                    if 'Your code has been rated at' in line:
                        try:
                            score_part = line.split('rated at ')[1].split('/')[0]
                            pylint_result['score'] = float(score_part)
                        except (IndexError, ValueError):
                            pass
            
            return pylint_result
        
        except subprocess.TimeoutExpired:
            logger.warning(f"pylint analysis timed out for {file_path}")
            return {'error': 'Analysis timed out', 'timeout': True}
        except Exception as e:
            logger.error(f"pylint analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _run_mypy(self, file_path: str) -> Dict[str, Any]:
        """Run mypy analysis on a Python file."""
        try:
            result = subprocess.run([
                'mypy',
                '--ignore-missing-imports',
                '--no-error-summary',
                file_path
            ], capture_output=True, text=True, timeout=30)
            
            mypy_result = {
                'return_code': result.returncode,
                'issues': [],
                'summary': {'errors': 0, 'notes': 0, 'total_issues': 0}
            }
            
            if result.stdout:
                lines = result.stdout.strip().split('\\n')
                for line in lines:
                    if ':' in line and file_path in line:
                        parts = line.split(': ', 2)
                        if len(parts) >= 3:
                            location, severity, message = parts
                            location_parts = location.split(':')
                            mypy_result['issues'].append({
                                'line': int(location_parts[-1]) if location_parts[-1].isdigit() else 0,
                                'severity': severity.strip(),
                                'message': message.strip()
                            })
                            
                            if severity.strip().lower() == 'error':
                                mypy_result['summary']['errors'] += 1
                            else:
                                mypy_result['summary']['notes'] += 1
                
                mypy_result['summary']['total_issues'] = len(mypy_result['issues'])
            
            return mypy_result
        
        except subprocess.TimeoutExpired:
            logger.warning(f"mypy analysis timed out for {file_path}")
            return {'error': 'Analysis timed out', 'timeout': True}
        except Exception as e:
            logger.error(f"mypy analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _analyze_ast(self, source_code: str) -> Dict[str, Any]:
        """Analyze Python code using AST (Abstract Syntax Tree)."""
        try:
            tree = ast.parse(source_code)
            
            ast_result = {
                'functions': [],
                'classes': [],
                'imports': [],
                'complexity_metrics': {
                    'cyclomatic_complexity': 0,
                    'total_functions': 0,
                    'total_classes': 0,
                    'total_lines': len(source_code.split('\\n')),
                    'total_imports': 0
                },
                'code_quality': {
                    'has_main_guard': False,
                    'has_docstrings': False,
                    'function_docstring_coverage': 0.0,
                    'class_docstring_coverage': 0.0
                }
            }
            
            # Walk through AST nodes
            for node in ast.walk(tree):
                # Analyze functions
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'args_count': len(node.args.args),
                        'has_docstring': ast.get_docstring(node) is not None,
                        'is_private': node.name.startswith('_'),
                        'complexity': self._calculate_function_complexity(node)
                    }
                    ast_result['functions'].append(func_info)
                    ast_result['complexity_metrics']['total_functions'] += 1
                    ast_result['complexity_metrics']['cyclomatic_complexity'] += func_info['complexity']
                    
                    if func_info['has_docstring']:
                        ast_result['code_quality']['has_docstrings'] = True
                
                # Analyze classes
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'methods_count': len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                        'has_docstring': ast.get_docstring(node) is not None,
                        'is_private': node.name.startswith('_')
                    }
                    ast_result['classes'].append(class_info)
                    ast_result['complexity_metrics']['total_classes'] += 1
                    
                    if class_info['has_docstring']:
                        ast_result['code_quality']['has_docstrings'] = True
                
                # Analyze imports
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            ast_result['imports'].append({
                                'type': 'import',
                                'module': alias.name,
                                'alias': alias.asname,
                                'line': node.lineno
                            })
                    else:  # ast.ImportFrom
                        for alias in node.names:
                            ast_result['imports'].append({
                                'type': 'from_import',
                                'module': node.module,
                                'name': alias.name,
                                'alias': alias.asname,
                                'line': node.lineno
                            })
                    
                    ast_result['complexity_metrics']['total_imports'] += 1
                
                # Check for main guard
                elif isinstance(node, ast.If):
                    if (isinstance(node.test, ast.Compare) and
                        isinstance(node.test.left, ast.Name) and
                        node.test.left.id == '__name__' and
                        any(isinstance(comp, ast.Eq) for comp in node.test.ops) and
                        any(isinstance(comp, ast.Str) and comp.s == '__main__' 
                            for comp in node.test.comparators)):
                        ast_result['code_quality']['has_main_guard'] = True
            
            # Calculate docstring coverage
            if ast_result['complexity_metrics']['total_functions'] > 0:
                documented_functions = sum(1 for f in ast_result['functions'] if f['has_docstring'])
                ast_result['code_quality']['function_docstring_coverage'] = (
                    documented_functions / ast_result['complexity_metrics']['total_functions']
                )
            
            if ast_result['complexity_metrics']['total_classes'] > 0:
                documented_classes = sum(1 for c in ast_result['classes'] if c['has_docstring'])
                ast_result['code_quality']['class_docstring_coverage'] = (
                    documented_classes / ast_result['complexity_metrics']['total_classes']
                )
            
            return ast_result
        
        except SyntaxError as e:
            logger.warning(f"Syntax error in code: {e}")
            return {'error': f'Syntax error: {e}', 'syntax_error': True}
        except Exception as e:
            logger.error(f"AST analysis failed: {e}")
            return {'error': str(e)}
    
    def _calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            # Control flow statements that increase complexity
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of all analysis results."""
        summary = {
            'overall_quality': 'unknown',
            'total_issues': 0,
            'critical_issues': 0,
            'code_style_score': 0.0,
            'complexity_assessment': 'unknown',
            'recommendations': []
        }
        
        # Aggregate issue counts
        if 'flake8_analysis' in analysis_results:
            flake8 = analysis_results['flake8_analysis']
            if 'summary' in flake8:
                summary['total_issues'] += flake8['summary'].get('total_issues', 0)
                summary['critical_issues'] += flake8['summary'].get('errors', 0)
        
        if 'pylint_analysis' in analysis_results:
            pylint = analysis_results['pylint_analysis']
            if 'summary' in pylint:
                summary['total_issues'] += pylint['summary'].get('error', 0)
                summary['total_issues'] += pylint['summary'].get('warning', 0)
                summary['critical_issues'] += pylint['summary'].get('error', 0)
            
            # Use pylint score as base code style score
            if 'score' in pylint and pylint['score'] > 0:
                summary['code_style_score'] = pylint['score']
        
        if 'mypy_analysis' in analysis_results:
            mypy = analysis_results['mypy_analysis']
            if 'summary' in mypy:
                summary['total_issues'] += mypy['summary'].get('total_issues', 0)
                summary['critical_issues'] += mypy['summary'].get('errors', 0)
        
        # Assess complexity
        if 'ast_analysis' in analysis_results:
            ast_data = analysis_results['ast_analysis']
            if 'complexity_metrics' in ast_data:
                metrics = ast_data['complexity_metrics']
                total_functions = metrics.get('total_functions', 0)
                total_complexity = metrics.get('cyclomatic_complexity', 0)
                
                if total_functions > 0:
                    avg_complexity = total_complexity / total_functions
                    if avg_complexity <= 3:
                        summary['complexity_assessment'] = 'low'
                    elif avg_complexity <= 7:
                        summary['complexity_assessment'] = 'moderate'
                    else:
                        summary['complexity_assessment'] = 'high'
        
        # Generate overall quality assessment
        if summary['critical_issues'] == 0 and summary['total_issues'] <= 2:
            summary['overall_quality'] = 'excellent'
        elif summary['critical_issues'] <= 1 and summary['total_issues'] <= 5:
            summary['overall_quality'] = 'good'
        elif summary['critical_issues'] <= 3 and summary['total_issues'] <= 10:
            summary['overall_quality'] = 'fair'
        else:
            summary['overall_quality'] = 'needs_improvement'
        
        # Generate recommendations
        if summary['critical_issues'] > 0:
            summary['recommendations'].append('Fix critical errors and syntax issues')
        
        if summary['code_style_score'] < 7.0:
            summary['recommendations'].append('Improve code style and PEP 8 compliance')
        
        if summary['complexity_assessment'] == 'high':
            summary['recommendations'].append('Consider refactoring complex functions')
        
        if 'ast_analysis' in analysis_results:
            ast_data = analysis_results['ast_analysis']
            quality = ast_data.get('code_quality', {})
            if not quality.get('has_main_guard', False):
                summary['recommendations'].append('Add main guard (__name__ == "__main__")')
            
            if quality.get('function_docstring_coverage', 0) < 0.5:
                summary['recommendations'].append('Add docstrings to functions')
        
        return summary


# Add datetime import at module level
from datetime import datetime