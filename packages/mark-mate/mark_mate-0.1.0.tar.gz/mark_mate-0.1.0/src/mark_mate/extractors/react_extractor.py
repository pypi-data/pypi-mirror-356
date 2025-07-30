"""
React/TypeScript project extractor for modern frontend development analysis.

This module handles extraction and analysis of React/TypeScript projects,
providing comprehensive analysis of components, build configuration, and
modern frontend development practices.
"""

import logging
import os
import json
import re
from typing import Dict, Any, List, Optional
from .base_extractor import BaseExtractor

# Import analyzers if available
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from analyzers.react_analysis import ReactAnalyzer, TypeScriptAnalyzer, BuildConfigAnalyzer
    REACT_ANALYZERS_AVAILABLE = True
except ImportError:
    REACT_ANALYZERS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ReactExtractor(BaseExtractor):
    """Extractor for React/TypeScript projects with comprehensive analysis."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.extractor_name = "react_extractor"
        self.supported_extensions = ['.tsx', '.ts', '.jsx', '.json']  # Added .json for package.json
        
        # Initialize analyzers if available
        self.react_analyzer = None
        self.typescript_analyzer = None
        self.build_analyzer = None
        self.react_analyzers_available = REACT_ANALYZERS_AVAILABLE
        
        if self.react_analyzers_available:
            try:
                self.react_analyzer = ReactAnalyzer(config)
                self.typescript_analyzer = TypeScriptAnalyzer(config)
                self.build_analyzer = BuildConfigAnalyzer(config)
                logger.info("React/TypeScript analyzers initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize React analyzers: {e}")
                self.react_analyzers_available = False
    
    def can_extract(self, file_path: str) -> bool:
        """Check if this extractor can handle the given file."""
        ext = os.path.splitext(file_path)[1].lower()
        filename = os.path.basename(file_path).lower()
        
        # Handle specific files
        if filename in ['package.json', 'tsconfig.json', 'vite.config.js', 'webpack.config.js']:
            return True
        
        return ext in self.supported_extensions
    
    def extract_content(self, file_path: str) -> Dict[str, Any]:
        """Extract content and perform analysis on React/TypeScript files."""
        if not self.can_extract(file_path):
            return self.create_error_result(file_path, ValueError("Not a React/TypeScript file"))
        
        try:
            filename = os.path.basename(file_path).lower()
            
            # Handle configuration files
            if filename == 'package.json':
                return self._analyze_package_json(file_path)
            elif filename in ['tsconfig.json', 'vite.config.js', 'webpack.config.js']:
                return self._analyze_build_config(file_path)
            
            # Handle source files
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.tsx', '.jsx']:
                return self._analyze_react_component(file_path)
            elif ext in ['.ts', '.tsx']:
                return self._analyze_typescript_file(file_path)
            else:
                return self.create_error_result(file_path, ValueError(f"Unsupported file type: {ext}"))
        
        except Exception as e:
            logger.error(f"Error extracting React content from {file_path}: {e}")
            return self.create_error_result(file_path, e)
    
    def _analyze_package_json(self, file_path: str) -> Dict[str, Any]:
        """Analyze package.json for dependencies and build configuration."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # Basic analysis
            basic_analysis = self._analyze_package_structure(package_data, file_path)
            
            # Full analysis if available
            build_analysis = {}
            if self.build_analyzer and self.react_analyzers_available:
                try:
                    build_analysis = self.build_analyzer.analyze_package_json(file_path, package_data)
                    logger.info(f"Package.json analysis completed for {os.path.basename(file_path)}")
                except Exception as e:
                    logger.warning(f"Build analysis failed for {file_path}: {e}")
                    build_analysis = {'error': str(e)}
            else:
                build_analysis = {'warning': 'Build analysis tools not available'}
            
            # Create comprehensive content text
            content_text = self._create_package_content_text(package_data, basic_analysis, build_analysis)
            
            # Combine all analysis results
            comprehensive_analysis = {
                'file_type': 'package_json',
                'basic_structure': basic_analysis,
                'build_analysis': build_analysis,
                'package_data': package_data,
                'content_metrics': {
                    'dependencies_count': len(package_data.get('dependencies', {})),
                    'dev_dependencies_count': len(package_data.get('devDependencies', {})),
                    'scripts_count': len(package_data.get('scripts', {}))
                }
            }
            
            return self.create_success_result(file_path, content_text, comprehensive_analysis)
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in {file_path}: {e}")
            return self.create_error_result(file_path, e)
        except Exception as e:
            logger.error(f"Error analyzing package.json {file_path}: {e}")
            return self.create_error_result(file_path, e)
    
    def _analyze_build_config(self, file_path: str) -> Dict[str, Any]:
        """Analyze build configuration files."""
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(file_path).lower()
            
            # Basic analysis
            basic_analysis = self._analyze_config_structure(content, filename)
            
            # Full analysis if available
            config_analysis = {}
            if self.build_analyzer and self.react_analyzers_available:
                try:
                    config_analysis = self.build_analyzer.analyze_build_config(file_path, content)
                    logger.info(f"Build config analysis completed for {os.path.basename(file_path)}")
                except Exception as e:
                    logger.warning(f"Config analysis failed for {file_path}: {e}")
                    config_analysis = {'error': str(e)}
            else:
                config_analysis = {'warning': 'Config analysis tools not available'}
            
            # Create comprehensive content text
            content_text = self._create_config_content_text(content, basic_analysis, config_analysis, filename)
            
            # Combine all analysis results
            comprehensive_analysis = {
                'file_type': 'build_config',
                'config_type': filename,
                'basic_structure': basic_analysis,
                'config_analysis': config_analysis,
                'content_metrics': {
                    'file_size': len(content),
                    'line_count': len(content.split('\n'))
                }
            }
            
            return self.create_success_result(file_path, content_text, comprehensive_analysis)
        
        except Exception as e:
            logger.error(f"Error analyzing build config {file_path}: {e}")
            return self.create_error_result(file_path, e)
    
    def _analyze_react_component(self, file_path: str) -> Dict[str, Any]:
        """Analyze React component files (.tsx/.jsx)."""
        try:
            # Read source code
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            if not source_code.strip():
                logger.warning(f"Empty React component file: {file_path}")
                return self.create_success_result(
                    file_path, 
                    "[EMPTY FILE] React component file contains no code",
                    {'analysis_type': 'empty_file'}
                )
            
            # Basic component analysis
            basic_analysis = self._analyze_react_structure(source_code, file_path)
            
            # Full React analysis if available
            react_analysis = {}
            if self.react_analyzer and self.react_analyzers_available:
                try:
                    react_analysis = self.react_analyzer.analyze_component(file_path, source_code)
                    logger.info(f"React component analysis completed for {os.path.basename(file_path)}")
                except Exception as e:
                    logger.warning(f"React analysis failed for {file_path}: {e}")
                    react_analysis = {'error': str(e)}
            else:
                react_analysis = {'warning': 'React analysis tools not available'}
            
            # TypeScript analysis if it's a .tsx file
            typescript_analysis = {}
            if file_path.endswith('.tsx') and self.typescript_analyzer and self.react_analyzers_available:
                try:
                    typescript_analysis = self.typescript_analyzer.analyze_typescript(file_path, source_code)
                    logger.info(f"TypeScript analysis completed for {os.path.basename(file_path)}")
                except Exception as e:
                    logger.warning(f"TypeScript analysis failed for {file_path}: {e}")
                    typescript_analysis = {'error': str(e)}
            
            # Create comprehensive content text
            content_text = self._create_react_content_text(source_code, basic_analysis, react_analysis, typescript_analysis)
            
            # Combine all analysis results
            comprehensive_analysis = {
                'file_type': 'react_component',
                'language': 'typescript' if file_path.endswith('.tsx') else 'javascript',
                'basic_structure': basic_analysis,
                'react_analysis': react_analysis,
                'typescript_analysis': typescript_analysis,
                'content_metrics': {
                    'source_lines': len(source_code.split('\n')),
                    'source_size': len(source_code),
                    'non_empty_lines': len([line for line in source_code.split('\n') if line.strip()]),
                    'comment_lines': len([line for line in source_code.split('\n') if line.strip().startswith('//')])
                }
            }
            
            return self.create_success_result(file_path, content_text, comprehensive_analysis)
        
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error reading {file_path}: {e}")
            return self.create_error_result(file_path, e)
        except Exception as e:
            logger.error(f"Error extracting React component from {file_path}: {e}")
            return self.create_error_result(file_path, e)
    
    def _analyze_typescript_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze pure TypeScript files (.ts)."""
        try:
            # Read source code
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            if not source_code.strip():
                logger.warning(f"Empty TypeScript file: {file_path}")
                return self.create_success_result(
                    file_path, 
                    "[EMPTY FILE] TypeScript file contains no code",
                    {'analysis_type': 'empty_file'}
                )
            
            # Basic TypeScript analysis
            basic_analysis = self._analyze_typescript_structure(source_code, file_path)
            
            # Full TypeScript analysis if available
            typescript_analysis = {}
            if self.typescript_analyzer and self.react_analyzers_available:
                try:
                    typescript_analysis = self.typescript_analyzer.analyze_typescript(file_path, source_code)
                    logger.info(f"TypeScript analysis completed for {os.path.basename(file_path)}")
                except Exception as e:
                    logger.warning(f"TypeScript analysis failed for {file_path}: {e}")
                    typescript_analysis = {'error': str(e)}
            else:
                typescript_analysis = {'warning': 'TypeScript analysis tools not available'}
            
            # Create comprehensive content text
            content_text = self._create_typescript_content_text(source_code, basic_analysis, typescript_analysis)
            
            # Combine all analysis results
            comprehensive_analysis = {
                'file_type': 'typescript',
                'basic_structure': basic_analysis,
                'typescript_analysis': typescript_analysis,
                'content_metrics': {
                    'source_lines': len(source_code.split('\n')),
                    'source_size': len(source_code),
                    'non_empty_lines': len([line for line in source_code.split('\n') if line.strip()]),
                    'comment_lines': len([line for line in source_code.split('\n') if line.strip().startswith('//')])
                }
            }
            
            return self.create_success_result(file_path, content_text, comprehensive_analysis)
        
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error reading {file_path}: {e}")
            return self.create_error_result(file_path, e)
        except Exception as e:
            logger.error(f"Error extracting TypeScript from {file_path}: {e}")
            return self.create_error_result(file_path, e)
    
    def _analyze_package_structure(self, package_data: Dict[str, Any], file_path: str) -> Dict[str, Any]:
        """Perform basic package.json structure analysis."""
        try:
            analysis = {
                'name': package_data.get('name', 'unnamed'),
                'version': package_data.get('version', '0.0.0'),
                'description': package_data.get('description', ''),
                'has_react': False,
                'has_typescript': False,
                'build_tool': 'unknown',
                'framework_type': 'unknown',
                'dependencies': {
                    'production': list(package_data.get('dependencies', {}).keys()),
                    'development': list(package_data.get('devDependencies', {}).keys()),
                    'total_count': len(package_data.get('dependencies', {})) + len(package_data.get('devDependencies', {}))
                },
                'scripts': list(package_data.get('scripts', {}).keys()),
                'quality_indicators': {}
            }
            
            # Detect React
            all_deps = analysis['dependencies']['production'] + analysis['dependencies']['development']
            if 'react' in all_deps or '@types/react' in all_deps:
                analysis['has_react'] = True
                analysis['framework_type'] = 'react'
            
            # Detect TypeScript
            if 'typescript' in all_deps or '@types/node' in all_deps or any(dep.startswith('@types/') for dep in all_deps):
                analysis['has_typescript'] = True
            
            # Detect build tools
            if 'vite' in all_deps:
                analysis['build_tool'] = 'vite'
            elif 'webpack' in all_deps:
                analysis['build_tool'] = 'webpack'
            elif 'create-react-app' in all_deps or 'react-scripts' in all_deps:
                analysis['build_tool'] = 'create-react-app'
            elif 'next' in all_deps:
                analysis['build_tool'] = 'next.js'
                analysis['framework_type'] = 'next.js'
            
            # Quality indicators
            analysis['quality_indicators'] = {
                'has_testing': any('test' in dep or 'jest' in dep or 'vitest' in dep for dep in all_deps),
                'has_linting': any('eslint' in dep for dep in all_deps),
                'has_formatting': any('prettier' in dep for dep in all_deps),
                'has_type_checking': analysis['has_typescript'],
                'has_build_scripts': any('build' in script for script in analysis['scripts']),
                'has_dev_scripts': any('dev' in script or 'start' in script for script in analysis['scripts'])
            }
            
            return analysis
        
        except Exception as e:
            logger.error(f"Package structure analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _analyze_config_structure(self, content: str, filename: str) -> Dict[str, Any]:
        """Perform basic build configuration analysis."""
        try:
            analysis = {
                'config_type': filename,
                'file_size': len(content),
                'estimated_complexity': 'low',
                'contains_plugins': False,
                'contains_loaders': False,
                'has_typescript_config': False,
                'has_path_mapping': False
            }
            
            # Basic complexity estimation
            line_count = len(content.split('\n'))
            if line_count > 100:
                analysis['estimated_complexity'] = 'high'
            elif line_count > 50:
                analysis['estimated_complexity'] = 'medium'
            
            # Feature detection
            if 'plugin' in content.lower():
                analysis['contains_plugins'] = True
            if 'loader' in content.lower():
                analysis['contains_loaders'] = True
            if 'typescript' in content.lower() or '.ts' in content:
                analysis['has_typescript_config'] = True
            if '@/' in content or 'paths' in content:
                analysis['has_path_mapping'] = True
            
            return analysis
        
        except Exception as e:
            logger.error(f"Config structure analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_react_structure(self, source_code: str, file_path: str) -> Dict[str, Any]:
        """Perform basic React component structure analysis."""
        try:
            analysis = {
                'component_type': 'unknown',
                'has_jsx': False,
                'has_hooks': False,
                'has_state': False,
                'has_effects': False,
                'has_props_interface': False,
                'imports': [],
                'exports': [],
                'jsx_elements': [],
                'hooks_used': [],
                'estimated_complexity': 'low'
            }
            
            # Detect JSX
            if '<' in source_code and '>' in source_code:
                analysis['has_jsx'] = True
            
            # Detect component type
            if 'function ' in source_code and analysis['has_jsx']:
                analysis['component_type'] = 'functional'
            elif 'class ' in source_code and 'extends' in source_code:
                analysis['component_type'] = 'class'
            elif '=>' in source_code and analysis['has_jsx']:
                analysis['component_type'] = 'arrow_function'
            
            # Detect hooks
            hooks = ['useState', 'useEffect', 'useContext', 'useReducer', 'useMemo', 'useCallback', 'useRef']
            for hook in hooks:
                if hook in source_code:
                    analysis['has_hooks'] = True
                    analysis['hooks_used'].append(hook)
                    if hook == 'useState':
                        analysis['has_state'] = True
                    elif hook == 'useEffect':
                        analysis['has_effects'] = True
            
            # Detect TypeScript interfaces for props
            if 'interface' in source_code and 'Props' in source_code:
                analysis['has_props_interface'] = True
            
            # Extract imports
            import_lines = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', source_code)
            analysis['imports'] = import_lines
            
            # Extract JSX elements
            jsx_elements = re.findall(r'<(\w+)', source_code)
            analysis['jsx_elements'] = list(set(jsx_elements))
            
            # Estimate complexity
            complexity_score = len(analysis['hooks_used']) * 2 + len(analysis['jsx_elements'])
            if complexity_score > 20:
                analysis['estimated_complexity'] = 'high'
            elif complexity_score > 10:
                analysis['estimated_complexity'] = 'medium'
            
            return analysis
        
        except Exception as e:
            logger.error(f"React structure analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _analyze_typescript_structure(self, source_code: str, file_path: str) -> Dict[str, Any]:
        """Perform basic TypeScript structure analysis."""
        try:
            analysis = {
                'has_types': False,
                'has_interfaces': False,
                'has_generics': False,
                'has_enums': False,
                'has_decorators': False,
                'imports': [],
                'exports': [],
                'type_annotations': [],
                'estimated_type_coverage': 'unknown'
            }
            
            # Detect TypeScript features
            if ':' in source_code and ('string' in source_code or 'number' in source_code or 'boolean' in source_code):
                analysis['has_types'] = True
            if 'interface ' in source_code:
                analysis['has_interfaces'] = True
            if '<T>' in source_code or '<T,' in source_code:
                analysis['has_generics'] = True
            if 'enum ' in source_code:
                analysis['has_enums'] = True
            if '@' in source_code:
                analysis['has_decorators'] = True
            
            # Extract imports
            import_lines = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', source_code)
            analysis['imports'] = import_lines
            
            # Estimate type coverage
            total_lines = len([line for line in source_code.split('\n') if line.strip() and not line.strip().startswith('//')])
            type_annotations = len(re.findall(r':\s*\w+', source_code))
            
            if total_lines > 0:
                coverage_ratio = type_annotations / total_lines
                if coverage_ratio > 0.3:
                    analysis['estimated_type_coverage'] = 'high'
                elif coverage_ratio > 0.1:
                    analysis['estimated_type_coverage'] = 'medium'
                else:
                    analysis['estimated_type_coverage'] = 'low'
            
            return analysis
        
        except Exception as e:
            logger.error(f"TypeScript structure analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _create_package_content_text(self, package_data: Dict[str, Any], basic_analysis: Dict[str, Any], 
                                   build_analysis: Dict[str, Any]) -> str:
        """Create comprehensive text content for package.json."""
        content_parts = []
        
        content_parts.append("PACKAGE.JSON ANALYSIS")
        content_parts.append("=" * 50)
        
        # Project overview
        content_parts.append("PROJECT OVERVIEW:")
        content_parts.append(f"  Name: {basic_analysis.get('name', 'N/A')}")
        content_parts.append(f"  Version: {basic_analysis.get('version', 'N/A')}")
        content_parts.append(f"  Framework: {basic_analysis.get('framework_type', 'N/A')}")
        content_parts.append(f"  Build Tool: {basic_analysis.get('build_tool', 'N/A')}")
        content_parts.append(f"  Has React: {'✓' if basic_analysis.get('has_react') else '✗'}")
        content_parts.append(f"  Has TypeScript: {'✓' if basic_analysis.get('has_typescript') else '✗'}")
        content_parts.append("")
        
        # Dependencies
        deps = basic_analysis.get('dependencies', {})
        content_parts.append("DEPENDENCIES:")
        content_parts.append(f"  Production: {len(deps.get('production', []))}")
        content_parts.append(f"  Development: {len(deps.get('development', []))}")
        content_parts.append(f"  Total: {deps.get('total_count', 0)}")
        content_parts.append("")
        
        # Scripts
        scripts = basic_analysis.get('scripts', [])
        if scripts:
            content_parts.append("SCRIPTS:")
            for script in scripts[:10]:  # Show first 10 scripts
                content_parts.append(f"  - {script}")
            content_parts.append("")
        
        # Quality indicators
        quality = basic_analysis.get('quality_indicators', {})
        if quality:
            content_parts.append("QUALITY INDICATORS:")
            content_parts.append(f"  Testing: {'✓' if quality.get('has_testing') else '✗'}")
            content_parts.append(f"  Linting: {'✓' if quality.get('has_linting') else '✗'}")
            content_parts.append(f"  Formatting: {'✓' if quality.get('has_formatting') else '✗'}")
            content_parts.append(f"  Build Scripts: {'✓' if quality.get('has_build_scripts') else '✗'}")
            content_parts.append("")
        
        # Raw package.json
        content_parts.append("PACKAGE.JSON CONTENT:")
        content_parts.append("-" * 30)
        content_parts.append(json.dumps(package_data, indent=2))
        
        return "\n".join(content_parts)
    
    def _create_config_content_text(self, content: str, basic_analysis: Dict[str, Any], 
                                  config_analysis: Dict[str, Any], filename: str) -> str:
        """Create comprehensive text content for build config files."""
        content_parts = []
        
        content_parts.append(f"{filename.upper()} ANALYSIS")
        content_parts.append("=" * 50)
        
        # Configuration overview
        content_parts.append("CONFIGURATION OVERVIEW:")
        content_parts.append(f"  File: {filename}")
        content_parts.append(f"  Complexity: {basic_analysis.get('estimated_complexity', 'unknown')}")
        content_parts.append(f"  Has Plugins: {'✓' if basic_analysis.get('contains_plugins') else '✗'}")
        content_parts.append(f"  Has Loaders: {'✓' if basic_analysis.get('contains_loaders') else '✗'}")
        content_parts.append(f"  TypeScript Config: {'✓' if basic_analysis.get('has_typescript_config') else '✗'}")
        content_parts.append(f"  Path Mapping: {'✓' if basic_analysis.get('has_path_mapping') else '✗'}")
        content_parts.append("")
        
        # Configuration content
        content_parts.append("CONFIGURATION CONTENT:")
        content_parts.append("-" * 30)
        content_parts.append(content)
        
        return "\n".join(content_parts)
    
    def _create_react_content_text(self, source_code: str, basic_analysis: Dict[str, Any], 
                                 react_analysis: Dict[str, Any], typescript_analysis: Dict[str, Any]) -> str:
        """Create comprehensive text content for React components."""
        content_parts = []
        
        content_parts.append("REACT COMPONENT ANALYSIS")
        content_parts.append("=" * 50)
        
        if 'error' not in basic_analysis:
            # Component overview
            content_parts.append("COMPONENT OVERVIEW:")
            content_parts.append(f"  Type: {basic_analysis.get('component_type', 'unknown')}")
            content_parts.append(f"  Has JSX: {'✓' if basic_analysis.get('has_jsx') else '✗'}")
            content_parts.append(f"  Uses Hooks: {'✓' if basic_analysis.get('has_hooks') else '✗'}")
            content_parts.append(f"  Has State: {'✓' if basic_analysis.get('has_state') else '✗'}")
            content_parts.append(f"  Has Effects: {'✓' if basic_analysis.get('has_effects') else '✗'}")
            content_parts.append(f"  Complexity: {basic_analysis.get('estimated_complexity', 'unknown')}")
            content_parts.append("")
            
            # Hooks used
            hooks = basic_analysis.get('hooks_used', [])
            if hooks:
                content_parts.append("HOOKS USED:")
                for hook in hooks:
                    content_parts.append(f"  - {hook}")
                content_parts.append("")
            
            # JSX elements
            jsx_elements = basic_analysis.get('jsx_elements', [])
            if jsx_elements:
                content_parts.append("JSX ELEMENTS:")
                for element in jsx_elements[:10]:  # Show first 10 elements
                    content_parts.append(f"  - <{element}>")
                content_parts.append("")
            
            # TypeScript features (if applicable)
            if typescript_analysis and 'error' not in typescript_analysis:
                content_parts.append("TYPESCRIPT FEATURES:")
                content_parts.append(f"  Type Annotations: {'✓' if typescript_analysis.get('has_types') else '✗'}")
                content_parts.append(f"  Interfaces: {'✓' if typescript_analysis.get('has_interfaces') else '✗'}")
                content_parts.append(f"  Generics: {'✓' if typescript_analysis.get('has_generics') else '✗'}")
                content_parts.append(f"  Type Coverage: {typescript_analysis.get('estimated_type_coverage', 'unknown')}")
                content_parts.append("")
        
        # Source code
        content_parts.append("SOURCE CODE:")
        content_parts.append("-" * 30)
        content_parts.append(source_code)
        
        return "\n".join(content_parts)
    
    def _create_typescript_content_text(self, source_code: str, basic_analysis: Dict[str, Any], 
                                      typescript_analysis: Dict[str, Any]) -> str:
        """Create comprehensive text content for TypeScript files."""
        content_parts = []
        
        content_parts.append("TYPESCRIPT FILE ANALYSIS")
        content_parts.append("=" * 50)
        
        if 'error' not in basic_analysis:
            # TypeScript features
            content_parts.append("TYPESCRIPT FEATURES:")
            content_parts.append(f"  Type Annotations: {'✓' if basic_analysis.get('has_types') else '✗'}")
            content_parts.append(f"  Interfaces: {'✓' if basic_analysis.get('has_interfaces') else '✗'}")
            content_parts.append(f"  Generics: {'✓' if basic_analysis.get('has_generics') else '✗'}")
            content_parts.append(f"  Enums: {'✓' if basic_analysis.get('has_enums') else '✗'}")
            content_parts.append(f"  Decorators: {'✓' if basic_analysis.get('has_decorators') else '✗'}")
            content_parts.append(f"  Type Coverage: {basic_analysis.get('estimated_type_coverage', 'unknown')}")
            content_parts.append("")
            
            # Imports
            imports = basic_analysis.get('imports', [])
            if imports:
                content_parts.append("IMPORTS:")
                for imp in imports[:10]:  # Show first 10 imports
                    content_parts.append(f"  - {imp}")
                content_parts.append("")
        
        # Source code
        content_parts.append("SOURCE CODE:")
        content_parts.append("-" * 30)
        content_parts.append(source_code)
        
        return "\n".join(content_parts)
    
    def analyze_react_project(self, file_paths: List[str]) -> Dict[str, Any]:
        """Analyze multiple React/TypeScript files as a project."""
        project_analysis = {
            'total_files': len(file_paths),
            'files_analyzed': [],
            'project_structure': {
                'react_components': 0,
                'typescript_files': 0,
                'config_files': 0,
                'has_package_json': False,
                'build_tool': 'unknown',
                'framework_type': 'unknown'
            },
            'technology_stack': {
                'react': False,
                'typescript': False,
                'testing_framework': 'unknown',
                'build_tool': 'unknown'
            },
            'quality_summary': {
                'average_complexity': 'unknown',
                'type_coverage': 'unknown',
                'best_practices_score': 0
            }
        }
        
        for file_path in file_paths:
            if self.can_extract(file_path):
                try:
                    result = self.extract_content(file_path)
                    if result['success']:
                        project_analysis['files_analyzed'].append({
                            'file': os.path.basename(file_path),
                            'analysis': result.get('analysis', {})
                        })
                        
                        # Aggregate project metrics
                        analysis = result.get('analysis', {})
                        file_type = analysis.get('file_type', '')
                        
                        if file_type == 'react_component':
                            project_analysis['project_structure']['react_components'] += 1
                            project_analysis['technology_stack']['react'] = True
                            
                            if analysis.get('language') == 'typescript':
                                project_analysis['technology_stack']['typescript'] = True
                        
                        elif file_type == 'typescript':
                            project_analysis['project_structure']['typescript_files'] += 1
                            project_analysis['technology_stack']['typescript'] = True
                        
                        elif file_type == 'package_json':
                            project_analysis['project_structure']['has_package_json'] = True
                            basic = analysis.get('basic_structure', {})
                            project_analysis['project_structure']['build_tool'] = basic.get('build_tool', 'unknown')
                            project_analysis['project_structure']['framework_type'] = basic.get('framework_type', 'unknown')
                            project_analysis['technology_stack']['build_tool'] = basic.get('build_tool', 'unknown')
                        
                        elif file_type == 'build_config':
                            project_analysis['project_structure']['config_files'] += 1
                
                except Exception as e:
                    logger.error(f"Error analyzing {file_path} in project context: {e}")
        
        return project_analysis