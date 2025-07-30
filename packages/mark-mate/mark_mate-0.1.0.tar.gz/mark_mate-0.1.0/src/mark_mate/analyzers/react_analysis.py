"""
React/TypeScript analysis module for modern frontend development.

This module provides comprehensive analysis of React components, TypeScript code,
and build configurations for modern frontend projects.
"""

import logging
import re
import json
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class ReactAnalyzer:
    """React component analysis with JSX parsing and best practices."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the React analyzer."""
        self.config = config or {}
        logger.info("React analyzer initialized")
    
    def analyze_component(self, file_path: str, source_code: str) -> Dict[str, Any]:
        """
        Analyze React component for structure, patterns, and best practices.
        
        Args:
            file_path: Path to the React component file
            source_code: Component source code
            
        Returns:
            Dictionary containing React analysis results
        """
        analysis_results = {
            'file_path': file_path,
            'analysis_timestamp': str(datetime.now()),
            'component_analysis': {},
            'jsx_analysis': {},
            'hooks_analysis': {},
            'props_analysis': {},
            'best_practices': {},
            'summary': {}
        }
        
        try:
            # Component structure analysis
            analysis_results['component_analysis'] = self._analyze_component_structure(source_code)
            
            # JSX analysis
            analysis_results['jsx_analysis'] = self._analyze_jsx_patterns(source_code)
            
            # Hooks analysis
            analysis_results['hooks_analysis'] = self._analyze_hooks_usage(source_code)
            
            # Props analysis
            analysis_results['props_analysis'] = self._analyze_props_patterns(source_code)
            
            # Best practices check
            analysis_results['best_practices'] = self._check_react_best_practices(source_code)
            
            # Generate summary
            analysis_results['summary'] = self._generate_react_summary(analysis_results)
            
            return analysis_results
        
        except Exception as e:
            logger.error(f"React analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _analyze_component_structure(self, source_code: str) -> Dict[str, Any]:
        """Analyze React component structure and patterns."""
        try:
            structure = {
                'component_type': 'unknown',
                'component_name': 'unknown',
                'is_default_export': False,
                'is_named_export': False,
                'has_display_name': False,
                'component_patterns': [],
                'lifecycle_methods': [],
                'render_complexity': 'low'
            }
            
            # Detect component type and name
            # Function component
            func_match = re.search(r'(?:function|const)\s+(\w+)', source_code)
            if func_match and ('return' in source_code and '<' in source_code):
                structure['component_type'] = 'functional'
                structure['component_name'] = func_match.group(1)
            
            # Arrow function component
            arrow_match = re.search(r'const\s+(\w+)\s*=\s*\(.*?\)\s*=>', source_code)
            if arrow_match and ('<' in source_code):
                structure['component_type'] = 'arrow_functional'
                structure['component_name'] = arrow_match.group(1)
            
            # Class component
            class_match = re.search(r'class\s+(\w+)\s+extends\s+(?:React\.)?Component', source_code)
            if class_match:
                structure['component_type'] = 'class'
                structure['component_name'] = class_match.group(1)
            
            # Export patterns
            if 'export default' in source_code:
                structure['is_default_export'] = True
            if re.search(r'export\s+(?:const|function|class)', source_code):
                structure['is_named_export'] = True
            
            # Display name
            if f"{structure['component_name']}.displayName" in source_code:
                structure['has_display_name'] = True
            
            # Component patterns
            patterns = []
            if 'memo(' in source_code or 'React.memo' in source_code:
                patterns.append('memoized')
            if 'forwardRef(' in source_code or 'React.forwardRef' in source_code:
                patterns.append('forward_ref')
            if 'lazy(' in source_code or 'React.lazy' in source_code:
                patterns.append('lazy_loading')
            if 'Suspense' in source_code:
                patterns.append('suspense')
            structure['component_patterns'] = patterns
            
            # Lifecycle methods (class components)
            lifecycle_methods = [
                'componentDidMount', 'componentDidUpdate', 'componentWillUnmount',
                'shouldComponentUpdate', 'getSnapshotBeforeUpdate',
                'componentDidCatch', 'getDerivedStateFromError'
            ]
            found_methods = [method for method in lifecycle_methods if method in source_code]
            structure['lifecycle_methods'] = found_methods
            
            # Render complexity estimation
            jsx_lines = len([line for line in source_code.split('\n') if '<' in line and '>' in line])
            if jsx_lines > 20:
                structure['render_complexity'] = 'high'
            elif jsx_lines > 10:
                structure['render_complexity'] = 'medium'
            
            return structure
        
        except Exception as e:
            logger.error(f"Component structure analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_jsx_patterns(self, source_code: str) -> Dict[str, Any]:
        """Analyze JSX patterns and usage."""
        try:
            jsx_analysis = {
                'jsx_elements': [],
                'custom_components': [],
                'html_elements': [],
                'conditional_rendering': [],
                'list_rendering': False,
                'inline_styles': False,
                'css_classes': False,
                'event_handlers': [],
                'jsx_complexity': 'low'
            }
            
            # Extract JSX elements
            jsx_elements = re.findall(r'<(\w+)', source_code)
            jsx_analysis['jsx_elements'] = list(set(jsx_elements))
            
            # Separate custom components from HTML elements
            html_elements = ['div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                           'button', 'input', 'form', 'img', 'a', 'ul', 'li', 'table', 
                           'tr', 'td', 'th', 'section', 'article', 'nav', 'header', 'footer']
            
            for element in jsx_analysis['jsx_elements']:
                if element.lower() in html_elements:
                    jsx_analysis['html_elements'].append(element)
                elif element[0].isupper():  # Custom components start with uppercase
                    jsx_analysis['custom_components'].append(element)
            
            # Conditional rendering patterns
            conditional_patterns = []
            if '&&' in source_code and '{' in source_code:
                conditional_patterns.append('logical_and')
            if '?' in source_code and ':' in source_code and '{' in source_code:
                conditional_patterns.append('ternary_operator')
            if 'if(' in source_code or 'if (' in source_code:
                conditional_patterns.append('if_statement')
            jsx_analysis['conditional_rendering'] = conditional_patterns
            
            # List rendering
            if '.map(' in source_code and '{' in source_code:
                jsx_analysis['list_rendering'] = True
            
            # Styling patterns
            if 'style={{' in source_code:
                jsx_analysis['inline_styles'] = True
            if 'className=' in source_code or 'class=' in source_code:
                jsx_analysis['css_classes'] = True
            
            # Event handlers
            event_handlers = re.findall(r'on(\w+)=', source_code)
            jsx_analysis['event_handlers'] = list(set(event_handlers))
            
            # JSX complexity
            total_jsx_features = (
                len(jsx_analysis['jsx_elements']) +
                len(jsx_analysis['conditional_rendering']) +
                len(jsx_analysis['event_handlers']) +
                (1 if jsx_analysis['list_rendering'] else 0)
            )
            
            if total_jsx_features > 15:
                jsx_analysis['jsx_complexity'] = 'high'
            elif total_jsx_features > 8:
                jsx_analysis['jsx_complexity'] = 'medium'
            
            return jsx_analysis
        
        except Exception as e:
            logger.error(f"JSX analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_hooks_usage(self, source_code: str) -> Dict[str, Any]:
        """Analyze React hooks usage and patterns."""
        try:
            hooks_analysis = {
                'hooks_used': [],
                'custom_hooks': [],
                'hooks_count': {},
                'dependency_arrays': [],
                'hooks_best_practices': {
                    'proper_dependency_arrays': True,
                    'hooks_at_top_level': True,
                    'custom_hooks_naming': True
                }
            }
            
            # Standard React hooks
            standard_hooks = [
                'useState', 'useEffect', 'useContext', 'useReducer',
                'useMemo', 'useCallback', 'useRef', 'useImperativeHandle',
                'useLayoutEffect', 'useDebugValue'
            ]
            
            for hook in standard_hooks:
                matches = re.findall(f'{hook}\\(', source_code)
                if matches:
                    hooks_analysis['hooks_used'].append(hook)
                    hooks_analysis['hooks_count'][hook] = len(matches)
            
            # Custom hooks (functions starting with 'use')
            custom_hook_matches = re.findall(r'(?:const|let|var)\s+(\w*use\w+)\s*=', source_code)
            hooks_analysis['custom_hooks'] = list(set(custom_hook_matches))
            
            # Dependency arrays analysis
            dependency_arrays = re.findall(r'useEffect\([^,]+,\s*\[([^\]]*)\]', source_code)
            hooks_analysis['dependency_arrays'] = dependency_arrays
            
            # Best practices checks
            # Check for empty dependency arrays (potential issues)
            if 'useEffect(' in source_code:
                empty_deps = source_code.count('useEffect(') > source_code.count(', [')
                hooks_analysis['hooks_best_practices']['proper_dependency_arrays'] = not empty_deps
            
            # Check if hooks are at top level (not in loops/conditions)
            for hook in hooks_analysis['hooks_used']:
                # Simple check: if hook is inside if/for/while
                hook_lines = [line for line in source_code.split('\n') if hook in line]
                for line in hook_lines:
                    stripped = line.strip()
                    if stripped.startswith('if') or stripped.startswith('for') or stripped.startswith('while'):
                        hooks_analysis['hooks_best_practices']['hooks_at_top_level'] = False
                        break
            
            # Check custom hooks naming
            for custom_hook in hooks_analysis['custom_hooks']:
                if not custom_hook.startswith('use'):
                    hooks_analysis['hooks_best_practices']['custom_hooks_naming'] = False
                    break
            
            return hooks_analysis
        
        except Exception as e:
            logger.error(f"Hooks analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_props_patterns(self, source_code: str) -> Dict[str, Any]:
        """Analyze props patterns and TypeScript interfaces."""
        try:
            props_analysis = {
                'has_props_interface': False,
                'props_interface_name': None,
                'destructured_props': [],
                'default_props': False,
                'prop_types': False,
                'props_spreading': False,
                'props_drilling_risk': 'low'
            }
            
            # TypeScript props interface
            interface_match = re.search(r'interface\s+(\w*Props?\w*)', source_code)
            if interface_match:
                props_analysis['has_props_interface'] = True
                props_analysis['props_interface_name'] = interface_match.group(1)
            
            # Destructured props
            destructure_match = re.search(r'{\s*([^}]+)\s*}\s*[:=].*props', source_code, re.IGNORECASE)
            if destructure_match:
                props_list = [prop.strip() for prop in destructure_match.group(1).split(',')]
                props_analysis['destructured_props'] = props_list
            
            # Default props
            if 'defaultProps' in source_code:
                props_analysis['default_props'] = True
            
            # PropTypes
            if 'PropTypes' in source_code or 'propTypes' in source_code:
                props_analysis['prop_types'] = True
            
            # Props spreading
            if '...props' in source_code or '{...props}' in source_code:
                props_analysis['props_spreading'] = True
            
            # Props drilling risk (simple heuristic)
            props_count = len(props_analysis['destructured_props'])
            if props_count > 10:
                props_analysis['props_drilling_risk'] = 'high'
            elif props_count > 5:
                props_analysis['props_drilling_risk'] = 'medium'
            
            return props_analysis
        
        except Exception as e:
            logger.error(f"Props analysis failed: {e}")
            return {'error': str(e)}
    
    def _check_react_best_practices(self, source_code: str) -> Dict[str, Any]:
        """Check React best practices and patterns."""
        try:
            best_practices = {
                'issues': [],
                'warnings': [],
                'good_practices': [],
                'score': 0
            }
            
            # Key extraction for lists
            if '.map(' in source_code and 'key=' not in source_code:
                best_practices['issues'].append('Missing key prop in list rendering')
            elif '.map(' in source_code and 'key=' in source_code:
                best_practices['good_practices'].append('Proper key usage in list rendering')
            
            # Event handler binding (class components)
            if 'class ' in source_code and 'this.handleClick' in source_code:
                if '.bind(this)' in source_code:
                    best_practices['warnings'].append('Using .bind() in render method (performance issue)')
                elif 'handleClick = (' in source_code:
                    best_practices['good_practices'].append('Using arrow functions for event handlers')
            
            # Direct state mutation
            if 'this.state.' in source_code and '=' in source_code:
                # Simple check for direct assignment to state
                state_assignments = re.findall(r'this\.state\.\w+\s*=', source_code)
                if state_assignments:
                    best_practices['issues'].append('Direct state mutation detected')
            
            # Inline function definitions in JSX
            inline_functions = len(re.findall(r'{\s*\([^)]*\)\s*=>', source_code))
            if inline_functions > 3:
                best_practices['warnings'].append(f'Many inline functions in JSX ({inline_functions}) - consider useCallback')
            
            # Component naming
            component_names = re.findall(r'(?:function|const|class)\s+(\w+)', source_code)
            for name in component_names:
                if name[0].islower() and 'component' in name.lower():
                    best_practices['warnings'].append(f'Component name should start with uppercase: {name}')
                elif name[0].isupper():
                    best_practices['good_practices'].append('Proper component naming convention')
                    break
            
            # Fragment usage
            if '<React.Fragment>' in source_code or '<>' in source_code:
                best_practices['good_practices'].append('Using React Fragments to avoid wrapper divs')
            
            # Conditional rendering patterns
            if ' && ' in source_code and '{' in source_code:
                best_practices['good_practices'].append('Using logical AND for conditional rendering')
            
            # Performance optimizations
            if 'memo(' in source_code or 'React.memo' in source_code:
                best_practices['good_practices'].append('Using React.memo for performance optimization')
            
            if 'useMemo(' in source_code or 'useCallback(' in source_code:
                best_practices['good_practices'].append('Using performance hooks (useMemo/useCallback)')
            
            # Calculate score
            total_checks = 8  # Number of best practice checks
            issues_weight = 3
            warnings_weight = 1
            good_practices_weight = 1
            
            penalty = len(best_practices['issues']) * issues_weight + len(best_practices['warnings']) * warnings_weight
            bonus = len(best_practices['good_practices']) * good_practices_weight
            
            best_practices['score'] = max(0, min(100, 100 - penalty + bonus))
            
            return best_practices
        
        except Exception as e:
            logger.error(f"Best practices check failed: {e}")
            return {'error': str(e)}
    
    def _generate_react_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate React analysis summary."""
        summary = {
            'component_quality': 'unknown',
            'complexity_level': 'unknown',
            'modern_patterns_usage': 'unknown',
            'total_issues': 0,
            'recommendations': []
        }
        
        try:
            # Count issues
            if 'best_practices' in analysis_results:
                bp = analysis_results['best_practices']
                summary['total_issues'] = len(bp.get('issues', [])) + len(bp.get('warnings', []))
            
            # Component quality assessment
            if 'best_practices' in analysis_results:
                score = analysis_results['best_practices'].get('score', 0)
                if score >= 80:
                    summary['component_quality'] = 'excellent'
                elif score >= 60:
                    summary['component_quality'] = 'good'
                elif score >= 40:
                    summary['component_quality'] = 'fair'
                else:
                    summary['component_quality'] = 'needs_improvement'
            
            # Complexity level
            component_complexity = 'low'
            jsx_complexity = 'low'
            
            if 'component_analysis' in analysis_results:
                component_complexity = analysis_results['component_analysis'].get('render_complexity', 'low')
            
            if 'jsx_analysis' in analysis_results:
                jsx_complexity = analysis_results['jsx_analysis'].get('jsx_complexity', 'low')
            
            if component_complexity == 'high' or jsx_complexity == 'high':
                summary['complexity_level'] = 'high'
            elif component_complexity == 'medium' or jsx_complexity == 'medium':
                summary['complexity_level'] = 'medium'
            else:
                summary['complexity_level'] = 'low'
            
            # Modern patterns usage
            modern_score = 0
            if 'hooks_analysis' in analysis_results:
                hooks = analysis_results['hooks_analysis'].get('hooks_used', [])
                if 'useState' in hooks or 'useEffect' in hooks:
                    modern_score += 2
                if any(hook in hooks for hook in ['useMemo', 'useCallback', 'useContext']):
                    modern_score += 1
            
            if 'component_analysis' in analysis_results:
                patterns = analysis_results['component_analysis'].get('component_patterns', [])
                if 'memoized' in patterns:
                    modern_score += 1
                if 'lazy_loading' in patterns or 'suspense' in patterns:
                    modern_score += 1
            
            if modern_score >= 4:
                summary['modern_patterns_usage'] = 'excellent'
            elif modern_score >= 2:
                summary['modern_patterns_usage'] = 'good'
            elif modern_score >= 1:
                summary['modern_patterns_usage'] = 'basic'
            else:
                summary['modern_patterns_usage'] = 'minimal'
            
            # Generate recommendations
            if summary['total_issues'] > 3:
                summary['recommendations'].append('Address React best practices violations')
            
            if summary['complexity_level'] == 'high':
                summary['recommendations'].append('Consider breaking down complex components')
            
            if summary['modern_patterns_usage'] == 'minimal':
                summary['recommendations'].append('Consider using modern React patterns (hooks, memoization)')
            
            if 'hooks_analysis' in analysis_results:
                hooks_bp = analysis_results['hooks_analysis'].get('hooks_best_practices', {})
                if not hooks_bp.get('proper_dependency_arrays', True):
                    summary['recommendations'].append('Review useEffect dependency arrays')
            
            return summary
        
        except Exception as e:
            logger.error(f"React summary generation failed: {e}")
            return {'error': str(e)}


class TypeScriptAnalyzer:
    """TypeScript analysis with type checking and modern features."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the TypeScript analyzer."""
        self.config = config or {}
        logger.info("TypeScript analyzer initialized")
    
    def analyze_typescript(self, file_path: str, source_code: str) -> Dict[str, Any]:
        """
        Analyze TypeScript code for types, patterns, and best practices.
        
        Args:
            file_path: Path to the TypeScript file
            source_code: TypeScript source code
            
        Returns:
            Dictionary containing TypeScript analysis results
        """
        analysis_results = {
            'file_path': file_path,
            'analysis_timestamp': str(datetime.now()),
            'type_analysis': {},
            'interface_analysis': {},
            'generic_analysis': {},
            'import_analysis': {},
            'best_practices': {},
            'summary': {}
        }
        
        try:
            # Type analysis
            analysis_results['type_analysis'] = self._analyze_types(source_code)
            
            # Interface analysis
            analysis_results['interface_analysis'] = self._analyze_interfaces(source_code)
            
            # Generic analysis
            analysis_results['generic_analysis'] = self._analyze_generics(source_code)
            
            # Import/export analysis
            analysis_results['import_analysis'] = self._analyze_imports_exports(source_code)
            
            # Best practices check
            analysis_results['best_practices'] = self._check_typescript_best_practices(source_code)
            
            # Generate summary
            analysis_results['summary'] = self._generate_typescript_summary(analysis_results)
            
            return analysis_results
        
        except Exception as e:
            logger.error(f"TypeScript analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _analyze_types(self, source_code: str) -> Dict[str, Any]:
        """Analyze TypeScript type usage."""
        try:
            type_analysis = {
                'primitive_types': [],
                'complex_types': [],
                'type_aliases': [],
                'union_types': [],
                'intersection_types': [],
                'type_annotations_count': 0,
                'type_coverage_estimate': 'unknown'
            }
            
            # Primitive types
            primitives = ['string', 'number', 'boolean', 'null', 'undefined', 'void', 'any', 'unknown', 'never']
            for primitive in primitives:
                if f': {primitive}' in source_code or f'<{primitive}>' in source_code:
                    type_analysis['primitive_types'].append(primitive)
            
            # Type aliases
            type_aliases = re.findall(r'type\s+(\w+)\s*=', source_code)
            type_analysis['type_aliases'] = type_aliases
            
            # Union types
            union_count = source_code.count(' | ')
            if union_count > 0:
                type_analysis['union_types'] = [f'union_type_{i}' for i in range(union_count)]
            
            # Intersection types
            intersection_count = source_code.count(' & ')
            if intersection_count > 0:
                type_analysis['intersection_types'] = [f'intersection_type_{i}' for i in range(intersection_count)]
            
            # Type annotations count
            type_annotations = len(re.findall(r':\s*\w+', source_code))
            type_analysis['type_annotations_count'] = type_annotations
            
            # Type coverage estimate
            total_declarations = len(re.findall(r'(?:const|let|var|function)\s+\w+', source_code))
            if total_declarations > 0:
                coverage_ratio = type_annotations / total_declarations
                if coverage_ratio > 0.8:
                    type_analysis['type_coverage_estimate'] = 'high'
                elif coverage_ratio > 0.5:
                    type_analysis['type_coverage_estimate'] = 'medium'
                else:
                    type_analysis['type_coverage_estimate'] = 'low'
            
            return type_analysis
        
        except Exception as e:
            logger.error(f"Type analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_interfaces(self, source_code: str) -> Dict[str, Any]:
        """Analyze TypeScript interfaces."""
        try:
            interface_analysis = {
                'interfaces': [],
                'interface_extensions': [],
                'interface_properties': {},
                'optional_properties': {}
            }
            
            # Find interfaces
            interface_matches = re.findall(r'interface\s+(\w+)(?:\s+extends\s+(\w+))?\s*{([^}]*)}', source_code, re.DOTALL)
            
            for match in interface_matches:
                interface_name = match[0]
                extends_interface = match[1] if match[1] else None
                interface_body = match[2]
                
                interface_analysis['interfaces'].append(interface_name)
                
                if extends_interface:
                    interface_analysis['interface_extensions'].append({
                        'interface': interface_name,
                        'extends': extends_interface
                    })
                
                # Analyze properties
                properties = re.findall(r'(\w+)(\??):\s*([^;]+)', interface_body)
                interface_analysis['interface_properties'][interface_name] = []
                interface_analysis['optional_properties'][interface_name] = []
                
                for prop_match in properties:
                    prop_name = prop_match[0]
                    is_optional = prop_match[1] == '?'
                    prop_type = prop_match[2].strip()
                    
                    interface_analysis['interface_properties'][interface_name].append({
                        'name': prop_name,
                        'type': prop_type,
                        'optional': is_optional
                    })
                    
                    if is_optional:
                        interface_analysis['optional_properties'][interface_name].append(prop_name)
            
            return interface_analysis
        
        except Exception as e:
            logger.error(f"Interface analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_generics(self, source_code: str) -> Dict[str, Any]:
        """Analyze TypeScript generics usage."""
        try:
            generic_analysis = {
                'generic_functions': [],
                'generic_interfaces': [],
                'generic_classes': [],
                'type_parameters': [],
                'constraints': []
            }
            
            # Generic functions
            generic_funcs = re.findall(r'function\s+(\w+)<([^>]+)>', source_code)
            for func_match in generic_funcs:
                func_name = func_match[0]
                type_params = func_match[1]
                generic_analysis['generic_functions'].append({
                    'name': func_name,
                    'type_parameters': type_params
                })
            
            # Generic interfaces
            generic_interfaces = re.findall(r'interface\s+(\w+)<([^>]+)>', source_code)
            for interface_match in generic_interfaces:
                interface_name = interface_match[0]
                type_params = interface_match[1]
                generic_analysis['generic_interfaces'].append({
                    'name': interface_name,
                    'type_parameters': type_params
                })
            
            # Type parameters
            type_params = re.findall(r'<([T-Z]\w*)(?:\s+extends\s+(\w+))?>', source_code)
            for param_match in type_params:
                param_name = param_match[0]
                constraint = param_match[1] if param_match[1] else None
                generic_analysis['type_parameters'].append(param_name)
                if constraint:
                    generic_analysis['constraints'].append({
                        'parameter': param_name,
                        'constraint': constraint
                    })
            
            return generic_analysis
        
        except Exception as e:
            logger.error(f"Generic analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_imports_exports(self, source_code: str) -> Dict[str, Any]:
        """Analyze import/export patterns."""
        try:
            import_analysis = {
                'imports': [],
                'exports': [],
                'dynamic_imports': False,
                'default_export': None,
                'named_exports': [],
                'import_types': []
            }
            
            # Regular imports
            imports = re.findall(r'import\s+(?:{([^}]+)}|(\w+)|\*\s+as\s+(\w+))\s+from\s+[\'"]([^\'"]+)[\'"]', source_code)
            for import_match in imports:
                named_imports = import_match[0] if import_match[0] else None
                default_import = import_match[1] if import_match[1] else None
                namespace_import = import_match[2] if import_match[2] else None
                module_path = import_match[3]
                
                import_analysis['imports'].append({
                    'module': module_path,
                    'named': named_imports.split(',') if named_imports else [],
                    'default': default_import,
                    'namespace': namespace_import
                })
            
            # Type imports
            type_imports = re.findall(r'import\s+type\s+{([^}]+)}\s+from\s+[\'"]([^\'"]+)[\'"]', source_code)
            for type_import in type_imports:
                import_analysis['import_types'].append({
                    'types': type_import[0].split(','),
                    'module': type_import[1]
                })
            
            # Dynamic imports
            if 'import(' in source_code:
                import_analysis['dynamic_imports'] = True
            
            # Exports
            if 'export default' in source_code:
                default_match = re.search(r'export\s+default\s+(\w+)', source_code)
                if default_match:
                    import_analysis['default_export'] = default_match.group(1)
            
            named_exports = re.findall(r'export\s+(?:const|function|class|interface|type)\s+(\w+)', source_code)
            import_analysis['named_exports'] = named_exports
            
            return import_analysis
        
        except Exception as e:
            logger.error(f"Import/export analysis failed: {e}")
            return {'error': str(e)}
    
    def _check_typescript_best_practices(self, source_code: str) -> Dict[str, Any]:
        """Check TypeScript best practices."""
        try:
            best_practices = {
                'issues': [],
                'warnings': [],
                'good_practices': [],
                'score': 0
            }
            
            # Avoid 'any' type
            any_count = source_code.count(': any')
            if any_count > 0:
                best_practices['warnings'].append(f'Using "any" type {any_count} times - consider more specific types')
            else:
                best_practices['good_practices'].append('Avoiding "any" type')
            
            # Use 'unknown' instead of 'any' for unknown types
            if ': unknown' in source_code:
                best_practices['good_practices'].append('Using "unknown" type for type safety')
            
            # Interface naming convention (PascalCase)
            interfaces = re.findall(r'interface\s+(\w+)', source_code)
            for interface in interfaces:
                if not interface[0].isupper():
                    best_practices['warnings'].append(f'Interface "{interface}" should use PascalCase')
                else:
                    best_practices['good_practices'].append('Proper interface naming convention')
                    break
            
            # Type assertions (should be minimal)
            type_assertions = source_code.count(' as ') + source_code.count('<')
            if type_assertions > 3:
                best_practices['warnings'].append('Many type assertions - consider improving type inference')
            
            # Optional chaining
            if '?.' in source_code:
                best_practices['good_practices'].append('Using optional chaining')
            
            # Nullish coalescing
            if '??' in source_code:
                best_practices['good_practices'].append('Using nullish coalescing operator')
            
            # Strict type checking patterns
            if 'strictNullChecks' in source_code or '| null' in source_code or '| undefined' in source_code:
                best_practices['good_practices'].append('Using strict null checking patterns')
            
            # Generic constraints
            if 'extends' in source_code and '<' in source_code:
                best_practices['good_practices'].append('Using generic constraints')
            
            # Calculate score
            total_checks = 7
            issues_weight = 3
            warnings_weight = 1
            good_practices_weight = 1
            
            penalty = len(best_practices['issues']) * issues_weight + len(best_practices['warnings']) * warnings_weight
            bonus = len(best_practices['good_practices']) * good_practices_weight
            
            best_practices['score'] = max(0, min(100, 100 - penalty + bonus))
            
            return best_practices
        
        except Exception as e:
            logger.error(f"TypeScript best practices check failed: {e}")
            return {'error': str(e)}
    
    def _generate_typescript_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate TypeScript analysis summary."""
        summary = {
            'type_safety_level': 'unknown',
            'modern_features_usage': 'unknown',
            'code_quality': 'unknown',
            'total_issues': 0,
            'recommendations': []
        }
        
        try:
            # Count issues
            if 'best_practices' in analysis_results:
                bp = analysis_results['best_practices']
                summary['total_issues'] = len(bp.get('issues', [])) + len(bp.get('warnings', []))
            
            # Type safety level
            if 'type_analysis' in analysis_results:
                coverage = analysis_results['type_analysis'].get('type_coverage_estimate', 'unknown')
                any_usage = 'any' in analysis_results['type_analysis'].get('primitive_types', [])
                
                if coverage == 'high' and not any_usage:
                    summary['type_safety_level'] = 'excellent'
                elif coverage == 'high' or (coverage == 'medium' and not any_usage):
                    summary['type_safety_level'] = 'good'
                elif coverage == 'medium':
                    summary['type_safety_level'] = 'fair'
                else:
                    summary['type_safety_level'] = 'poor'
            
            # Modern features usage
            modern_score = 0
            if 'generic_analysis' in analysis_results:
                generics = analysis_results['generic_analysis']
                if generics.get('generic_functions') or generics.get('generic_interfaces'):
                    modern_score += 2
            
            if 'interface_analysis' in analysis_results:
                interfaces = analysis_results['interface_analysis'].get('interfaces', [])
                if interfaces:
                    modern_score += 1
            
            if 'type_analysis' in analysis_results:
                types = analysis_results['type_analysis']
                if types.get('union_types') or types.get('intersection_types'):
                    modern_score += 1
                if types.get('type_aliases'):
                    modern_score += 1
            
            if modern_score >= 4:
                summary['modern_features_usage'] = 'excellent'
            elif modern_score >= 2:
                summary['modern_features_usage'] = 'good'
            elif modern_score >= 1:
                summary['modern_features_usage'] = 'basic'
            else:
                summary['modern_features_usage'] = 'minimal'
            
            # Code quality
            if 'best_practices' in analysis_results:
                score = analysis_results['best_practices'].get('score', 0)
                if score >= 80:
                    summary['code_quality'] = 'excellent'
                elif score >= 60:
                    summary['code_quality'] = 'good'
                elif score >= 40:
                    summary['code_quality'] = 'fair'
                else:
                    summary['code_quality'] = 'needs_improvement'
            
            # Generate recommendations
            if summary['type_safety_level'] in ['poor', 'fair']:
                summary['recommendations'].append('Improve type annotations and avoid "any" type')
            
            if summary['modern_features_usage'] == 'minimal':
                summary['recommendations'].append('Consider using more TypeScript features (generics, unions, interfaces)')
            
            if summary['total_issues'] > 2:
                summary['recommendations'].append('Address TypeScript best practices violations')
            
            return summary
        
        except Exception as e:
            logger.error(f"TypeScript summary generation failed: {e}")
            return {'error': str(e)}


class BuildConfigAnalyzer:
    """Build configuration analysis for modern frontend tools."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the build config analyzer."""
        self.config = config or {}
        logger.info("Build config analyzer initialized")
    
    def analyze_package_json(self, file_path: str, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze package.json for build configuration and dependencies."""
        try:
            analysis = {
                'build_analysis': {},
                'dependency_analysis': {},
                'script_analysis': {},
                'quality_tools': {},
                'recommendations': []
            }
            
            # Build tool detection and analysis
            analysis['build_analysis'] = self._analyze_build_tools(package_data)
            
            # Dependency analysis
            analysis['dependency_analysis'] = self._analyze_dependencies(package_data)
            
            # Scripts analysis
            analysis['script_analysis'] = self._analyze_scripts(package_data)
            
            # Quality tools analysis
            analysis['quality_tools'] = self._analyze_quality_tools(package_data)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_package_recommendations(analysis)
            
            return analysis
        
        except Exception as e:
            logger.error(f"Package.json analysis failed: {e}")
            return {'error': str(e)}
    
    def analyze_build_config(self, file_path: str, config_content: str) -> Dict[str, Any]:
        """Analyze build configuration files."""
        try:
            filename = os.path.basename(file_path).lower()
            
            if filename == 'tsconfig.json':
                return self._analyze_tsconfig(config_content)
            elif 'vite.config' in filename:
                return self._analyze_vite_config(config_content)
            elif 'webpack.config' in filename:
                return self._analyze_webpack_config(config_content)
            else:
                return self._analyze_generic_config(config_content, filename)
        
        except Exception as e:
            logger.error(f"Build config analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_build_tools(self, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze build tools and configuration."""
        all_deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
        
        build_analysis = {
            'primary_build_tool': 'unknown',
            'bundler': 'unknown',
            'typescript_support': False,
            'css_preprocessing': [],
            'testing_framework': 'unknown',
            'linting_tools': [],
            'build_optimizations': []
        }
        
        # Detect primary build tool
        if 'vite' in all_deps:
            build_analysis['primary_build_tool'] = 'vite'
            build_analysis['bundler'] = 'rollup'
        elif 'webpack' in all_deps:
            build_analysis['primary_build_tool'] = 'webpack'
            build_analysis['bundler'] = 'webpack'
        elif 'react-scripts' in all_deps:
            build_analysis['primary_build_tool'] = 'create-react-app'
            build_analysis['bundler'] = 'webpack'
        elif 'next' in all_deps:
            build_analysis['primary_build_tool'] = 'next.js'
            build_analysis['bundler'] = 'webpack'
        elif 'parcel' in all_deps:
            build_analysis['primary_build_tool'] = 'parcel'
            build_analysis['bundler'] = 'parcel'
        
        # TypeScript support
        if 'typescript' in all_deps or '@types/node' in all_deps:
            build_analysis['typescript_support'] = True
        
        # CSS preprocessing
        css_tools = []
        if 'sass' in all_deps or 'node-sass' in all_deps:
            css_tools.append('sass')
        if 'less' in all_deps:
            css_tools.append('less')
        if 'stylus' in all_deps:
            css_tools.append('stylus')
        if 'postcss' in all_deps:
            css_tools.append('postcss')
        build_analysis['css_preprocessing'] = css_tools
        
        # Testing framework
        if 'jest' in all_deps:
            build_analysis['testing_framework'] = 'jest'
        elif 'vitest' in all_deps:
            build_analysis['testing_framework'] = 'vitest'
        elif 'mocha' in all_deps:
            build_analysis['testing_framework'] = 'mocha'
        elif '@testing-library/react' in all_deps:
            build_analysis['testing_framework'] = 'react-testing-library'
        
        # Linting tools
        linting = []
        if 'eslint' in all_deps:
            linting.append('eslint')
        if 'prettier' in all_deps:
            linting.append('prettier')
        if 'stylelint' in all_deps:
            linting.append('stylelint')
        build_analysis['linting_tools'] = linting
        
        return build_analysis
    
    def _analyze_dependencies(self, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dependency patterns and health."""
        deps = package_data.get('dependencies', {})
        dev_deps = package_data.get('devDependencies', {})
        
        dependency_analysis = {
            'total_dependencies': len(deps) + len(dev_deps),
            'production_count': len(deps),
            'development_count': len(dev_deps),
            'framework_dependencies': [],
            'utility_libraries': [],
            'potential_issues': []
        }
        
        all_deps = {**deps, **dev_deps}
        
        # Framework dependencies
        frameworks = []
        if 'react' in all_deps:
            frameworks.append('react')
        if 'vue' in all_deps:
            frameworks.append('vue')
        if 'angular' in all_deps:
            frameworks.append('angular')
        if 'svelte' in all_deps:
            frameworks.append('svelte')
        dependency_analysis['framework_dependencies'] = frameworks
        
        # Utility libraries
        utilities = []
        if 'lodash' in all_deps:
            utilities.append('lodash')
        if 'axios' in all_deps:
            utilities.append('axios')
        if 'moment' in all_deps:
            utilities.append('moment')
        if 'date-fns' in all_deps:
            utilities.append('date-fns')
        dependency_analysis['utility_libraries'] = utilities
        
        # Potential issues
        issues = []
        if dependency_analysis['total_dependencies'] > 100:
            issues.append('High number of dependencies - consider reducing bundle size')
        
        if 'moment' in all_deps:
            issues.append('Consider replacing moment.js with lighter alternatives like date-fns')
        
        if len(frameworks) > 1:
            issues.append('Multiple frontend frameworks detected - potential conflicts')
        
        dependency_analysis['potential_issues'] = issues
        
        return dependency_analysis
    
    def _analyze_scripts(self, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze npm scripts configuration."""
        scripts = package_data.get('scripts', {})
        
        script_analysis = {
            'available_scripts': list(scripts.keys()),
            'build_scripts': [],
            'dev_scripts': [],
            'test_scripts': [],
            'linting_scripts': [],
            'script_quality': 'unknown'
        }
        
        for script_name, script_command in scripts.items():
            if 'build' in script_name.lower():
                script_analysis['build_scripts'].append(script_name)
            elif any(word in script_name.lower() for word in ['dev', 'start', 'serve']):
                script_analysis['dev_scripts'].append(script_name)
            elif 'test' in script_name.lower():
                script_analysis['test_scripts'].append(script_name)
            elif any(word in script_name.lower() for word in ['lint', 'format', 'check']):
                script_analysis['linting_scripts'].append(script_name)
        
        # Script quality assessment
        essential_scripts = ['build', 'dev', 'test']
        available_essential = 0
        for essential in essential_scripts:
            if any(essential in script.lower() for script in script_analysis['available_scripts']):
                available_essential += 1
        
        if available_essential == 3:
            script_analysis['script_quality'] = 'excellent'
        elif available_essential == 2:
            script_analysis['script_quality'] = 'good'
        elif available_essential == 1:
            script_analysis['script_quality'] = 'basic'
        else:
            script_analysis['script_quality'] = 'minimal'
        
        return script_analysis
    
    def _analyze_quality_tools(self, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code quality and development tools."""
        all_deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
        
        quality_analysis = {
            'linting': False,
            'formatting': False,
            'type_checking': False,
            'testing': False,
            'pre_commit_hooks': False,
            'bundler_analysis': False,
            'quality_score': 0
        }
        
        # Linting
        if 'eslint' in all_deps:
            quality_analysis['linting'] = True
            quality_analysis['quality_score'] += 1
        
        # Formatting
        if 'prettier' in all_deps:
            quality_analysis['formatting'] = True
            quality_analysis['quality_score'] += 1
        
        # Type checking
        if 'typescript' in all_deps or '@types/node' in all_deps:
            quality_analysis['type_checking'] = True
            quality_analysis['quality_score'] += 1
        
        # Testing
        if any(tool in all_deps for tool in ['jest', 'vitest', '@testing-library/react', 'cypress', 'playwright']):
            quality_analysis['testing'] = True
            quality_analysis['quality_score'] += 1
        
        # Pre-commit hooks
        if 'husky' in all_deps or 'lint-staged' in all_deps:
            quality_analysis['pre_commit_hooks'] = True
            quality_analysis['quality_score'] += 1
        
        # Bundle analysis
        if any(tool in all_deps for tool in ['webpack-bundle-analyzer', 'rollup-plugin-analyzer']):
            quality_analysis['bundler_analysis'] = True
            quality_analysis['quality_score'] += 1
        
        return quality_analysis
    
    def _analyze_tsconfig(self, config_content: str) -> Dict[str, Any]:
        """Analyze tsconfig.json configuration."""
        try:
            # Simple text-based analysis since we can't guarantee JSON parsing
            analysis = {
                'strict_mode': False,
                'target': 'unknown',
                'module_system': 'unknown',
                'jsx_support': False,
                'path_mapping': False,
                'source_maps': False,
                'recommendations': []
            }
            
            if 'strict' in config_content and 'true' in config_content:
                analysis['strict_mode'] = True
            else:
                analysis['recommendations'].append('Enable strict mode for better type safety')
            
            target_match = re.search(r'"target":\s*"([^"]+)"', config_content)
            if target_match:
                analysis['target'] = target_match.group(1)
            
            if 'jsx' in config_content.lower():
                analysis['jsx_support'] = True
            
            if 'paths' in config_content:
                analysis['path_mapping'] = True
            
            if 'sourceMap' in config_content and 'true' in config_content:
                analysis['source_maps'] = True
            
            return analysis
        
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_vite_config(self, config_content: str) -> Dict[str, Any]:
        """Analyze Vite configuration."""
        analysis = {
            'plugins': [],
            'optimizations': [],
            'dev_server_config': False,
            'build_config': False
        }
        
        if 'plugins' in config_content:
            if 'react()' in config_content:
                analysis['plugins'].append('react')
            if 'vue()' in config_content:
                analysis['plugins'].append('vue')
        
        if 'server:' in config_content:
            analysis['dev_server_config'] = True
        
        if 'build:' in config_content:
            analysis['build_config'] = True
        
        return analysis
    
    def _analyze_webpack_config(self, config_content: str) -> Dict[str, Any]:
        """Analyze Webpack configuration."""
        analysis = {
            'entry_points': [],
            'loaders': [],
            'plugins': [],
            'optimization_config': False,
            'dev_server_config': False
        }
        
        if 'entry:' in config_content:
            analysis['entry_points'] = ['detected']
        
        if 'module:' in config_content and 'rules:' in config_content:
            if 'babel-loader' in config_content:
                analysis['loaders'].append('babel')
            if 'ts-loader' in config_content:
                analysis['loaders'].append('typescript')
            if 'css-loader' in config_content:
                analysis['loaders'].append('css')
        
        if 'optimization:' in config_content:
            analysis['optimization_config'] = True
        
        if 'devServer:' in config_content:
            analysis['dev_server_config'] = True
        
        return analysis
    
    def _analyze_generic_config(self, config_content: str, filename: str) -> Dict[str, Any]:
        """Analyze generic configuration files."""
        return {
            'config_type': filename,
            'size': len(config_content),
            'complexity': 'high' if len(config_content) > 1000 else 'medium' if len(config_content) > 500 else 'low'
        }
    
    def _generate_package_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on package.json analysis."""
        recommendations = []
        
        # Build tools recommendations
        build_analysis = analysis.get('build_analysis', {})
        if build_analysis.get('primary_build_tool') == 'unknown':
            recommendations.append('Consider adding a modern build tool like Vite or Webpack')
        
        # Quality tools recommendations
        quality_tools = analysis.get('quality_tools', {})
        if not quality_tools.get('linting'):
            recommendations.append('Add ESLint for code linting')
        if not quality_tools.get('formatting'):
            recommendations.append('Add Prettier for code formatting')
        if not quality_tools.get('testing'):
            recommendations.append('Add a testing framework like Jest or Vitest')
        
        # Scripts recommendations
        script_analysis = analysis.get('script_analysis', {})
        if script_analysis.get('script_quality') in ['basic', 'minimal']:
            recommendations.append('Add comprehensive npm scripts for build, dev, and test')
        
        # Dependency recommendations
        dependency_analysis = analysis.get('dependency_analysis', {})
        if dependency_analysis.get('potential_issues'):
            recommendations.extend(dependency_analysis['potential_issues'])
        
        return recommendations