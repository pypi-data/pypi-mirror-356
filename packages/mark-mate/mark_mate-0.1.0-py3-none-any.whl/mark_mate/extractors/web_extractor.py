"""
Web content extractor for HTML, CSS, and JavaScript files with validation.

This module handles extraction and analysis of web development files,
providing HTML validation, CSS analysis, and basic JavaScript checking.
"""

import logging
import os
import re
from typing import Dict, Any, List, Optional
from .base_extractor import BaseExtractor

# Web validation imports
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

try:
    import html5lib
    HTML5LIB_AVAILABLE = True
except ImportError:
    HTML5LIB_AVAILABLE = False

try:
    import cssutils
    CSSUTILS_AVAILABLE = True
except ImportError:
    CSSUTILS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

WEB_VALIDATION_AVAILABLE = BEAUTIFULSOUP_AVAILABLE

# Import validators if available
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from analyzers.web_validation import HTMLValidator, CSSAnalyzer, JSAnalyzer
    WEB_ANALYZERS_AVAILABLE = True
except ImportError:
    WEB_ANALYZERS_AVAILABLE = False

logger = logging.getLogger(__name__)


class WebExtractor(BaseExtractor):
    """Extractor for web development files with validation and analysis."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.extractor_name = "web_extractor"
        self.supported_extensions = ['.html', '.htm', '.css', '.js', '.jsx']
        
        # Initialize validators if available
        self.html_validator = None
        self.css_analyzer = None
        self.js_analyzer = None
        self.web_validation_available = WEB_VALIDATION_AVAILABLE
        self.web_analyzers_available = WEB_ANALYZERS_AVAILABLE
        
        if self.web_validation_available and self.web_analyzers_available:
            try:
                self.html_validator = HTMLValidator(config)
                self.css_analyzer = CSSAnalyzer(config)
                self.js_analyzer = JSAnalyzer(config)
                logger.info("Web analyzers initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize web analyzers: {e}")
                self.web_analyzers_available = False
    
    def can_extract(self, file_path: str) -> bool:
        """Check if this extractor can handle the given file."""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_extensions
    
    def extract_content(self, file_path: str) -> Dict[str, Any]:
        """Extract content and perform validation on web files."""
        if not self.can_extract(file_path):
            return self.create_error_result(file_path, ValueError("Not a web development file"))
        
        try:
            # Read source code
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source_code = f.read()
            
            if not source_code.strip():
                logger.warning(f"Empty web file: {file_path}")
                return self.create_success_result(
                    file_path, 
                    "[EMPTY FILE] Web file contains no content",
                    {'analysis_type': 'empty_file'}
                )
            
            # Determine file type and analyze accordingly
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ['.html', '.htm']:
                return self._analyze_html_file(file_path, source_code)
            elif ext == '.css':
                return self._analyze_css_file(file_path, source_code)
            elif ext in ['.js', '.jsx']:
                return self._analyze_js_file(file_path, source_code)
            else:
                return self.create_error_result(file_path, ValueError(f"Unsupported web file type: {ext}"))
        
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error reading {file_path}: {e}")
            return self.create_error_result(file_path, e)
        except Exception as e:
            logger.error(f"Error extracting web content from {file_path}: {e}")
            return self.create_error_result(file_path, e)
    
    def _analyze_html_file(self, file_path: str, source_code: str) -> Dict[str, Any]:
        """Analyze HTML file with validation and accessibility checks."""
        basic_analysis = self._analyze_html_structure(source_code, file_path)
        
        # Full validation if available
        validation_results = {}
        if self.html_validator and self.web_analyzers_available:
            try:
                validation_results = self.html_validator.validate_html(file_path, source_code)
                logger.info(f"HTML validation completed for {os.path.basename(file_path)}")
            except Exception as e:
                logger.warning(f"HTML validation failed for {file_path}: {e}")
                validation_results = {'error': str(e)}
        else:
            validation_results = {'warning': 'HTML validation tools not available'}
        
        # Create comprehensive content text
        content_text = self._create_html_content_text(source_code, basic_analysis, validation_results)
        
        # Combine all analysis results
        comprehensive_analysis = {
            'file_type': 'html',
            'basic_structure': basic_analysis,
            'validation_results': validation_results,
            'content_metrics': {
                'source_lines': len(source_code.split('\n')),
                'source_size': len(source_code),
                'non_empty_lines': len([line for line in source_code.split('\n') if line.strip()]),
                'comment_lines': len([line for line in source_code.split('\n') if '<!--' in line])
            }
        }
        
        return self.create_success_result(file_path, content_text, comprehensive_analysis)
    
    def _analyze_css_file(self, file_path: str, source_code: str) -> Dict[str, Any]:
        """Analyze CSS file with validation and best practices."""
        basic_analysis = self._analyze_css_structure(source_code, file_path)
        
        # Full analysis if available
        analysis_results = {}
        if self.css_analyzer and self.web_analyzers_available:
            try:
                analysis_results = self.css_analyzer.analyze_css(file_path, source_code)
                logger.info(f"CSS analysis completed for {os.path.basename(file_path)}")
            except Exception as e:
                logger.warning(f"CSS analysis failed for {file_path}: {e}")
                analysis_results = {'error': str(e)}
        else:
            analysis_results = {'warning': 'CSS analysis tools not available'}
        
        # Create comprehensive content text
        content_text = self._create_css_content_text(source_code, basic_analysis, analysis_results)
        
        # Combine all analysis results
        comprehensive_analysis = {
            'file_type': 'css',
            'basic_structure': basic_analysis,
            'analysis_results': analysis_results,
            'content_metrics': {
                'source_lines': len(source_code.split('\n')),
                'source_size': len(source_code),
                'non_empty_lines': len([line for line in source_code.split('\n') if line.strip()]),
                'comment_lines': len([line for line in source_code.split('\n') if line.strip().startswith('/*')])
            }
        }
        
        return self.create_success_result(file_path, content_text, comprehensive_analysis)
    
    def _analyze_js_file(self, file_path: str, source_code: str) -> Dict[str, Any]:
        """Analyze JavaScript file with basic syntax and structure checking."""
        basic_analysis = self._analyze_js_structure(source_code, file_path)
        
        # Full analysis if available
        analysis_results = {}
        if self.js_analyzer and self.web_analyzers_available:
            try:
                analysis_results = self.js_analyzer.analyze_javascript(file_path, source_code)
                logger.info(f"JavaScript analysis completed for {os.path.basename(file_path)}")
            except Exception as e:
                logger.warning(f"JavaScript analysis failed for {file_path}: {e}")
                analysis_results = {'error': str(e)}
        else:
            analysis_results = {'warning': 'JavaScript analysis tools not available'}
        
        # Create comprehensive content text
        content_text = self._create_js_content_text(source_code, basic_analysis, analysis_results)
        
        # Combine all analysis results
        comprehensive_analysis = {
            'file_type': 'javascript',
            'basic_structure': basic_analysis,
            'analysis_results': analysis_results,
            'content_metrics': {
                'source_lines': len(source_code.split('\n')),
                'source_size': len(source_code),
                'non_empty_lines': len([line for line in source_code.split('\n') if line.strip()]),
                'comment_lines': len([line for line in source_code.split('\n') if line.strip().startswith('//')])
            }
        }
        
        return self.create_success_result(file_path, content_text, comprehensive_analysis)
    
    def _analyze_html_structure(self, source_code: str, file_path: str) -> Dict[str, Any]:
        """Perform basic HTML structure analysis."""
        try:
            if not BEAUTIFULSOUP_AVAILABLE:
                return {'error': 'BeautifulSoup not available for HTML parsing'}
            
            soup = BeautifulSoup(source_code, 'html.parser')
            
            analysis = {
                'has_doctype': source_code.strip().lower().startswith('<!doctype'),
                'has_html_tag': soup.find('html') is not None,
                'has_head_tag': soup.find('head') is not None,
                'has_body_tag': soup.find('body') is not None,
                'title': soup.find('title').get_text() if soup.find('title') else None,
                'meta_tags': len(soup.find_all('meta')),
                'headings': {
                    'h1': len(soup.find_all('h1')),
                    'h2': len(soup.find_all('h2')),
                    'h3': len(soup.find_all('h3')),
                    'h4': len(soup.find_all('h4')),
                    'h5': len(soup.find_all('h5')),
                    'h6': len(soup.find_all('h6'))
                },
                'links': len(soup.find_all('a')),
                'images': len(soup.find_all('img')),
                'forms': len(soup.find_all('form')),
                'scripts': len(soup.find_all('script')),
                'stylesheets': len(soup.find_all('link', {'rel': 'stylesheet'})),
                'semantic_elements': {
                    'header': len(soup.find_all('header')),
                    'nav': len(soup.find_all('nav')),
                    'main': len(soup.find_all('main')),
                    'section': len(soup.find_all('section')),
                    'article': len(soup.find_all('article')),
                    'aside': len(soup.find_all('aside')),
                    'footer': len(soup.find_all('footer'))
                }
            }
            
            # Accessibility checks
            analysis['accessibility'] = {
                'images_with_alt': len([img for img in soup.find_all('img') if img.get('alt') is not None]),
                'images_without_alt': len([img for img in soup.find_all('img') if img.get('alt') is None]),
                'has_lang_attribute': soup.find('html', attrs={'lang': True}) is not None,
                'has_viewport_meta': any('viewport' in str(meta) for meta in soup.find_all('meta'))
            }
            
            # Structure quality
            analysis['structure_quality'] = {
                'well_formed': all([
                    analysis['has_doctype'],
                    analysis['has_html_tag'],
                    analysis['has_head_tag'],
                    analysis['has_body_tag']
                ]),
                'has_title': analysis['title'] is not None,
                'heading_structure': sum(analysis['headings'].values()) > 0,
                'semantic_markup': sum(analysis['semantic_elements'].values()) > 0
            }
            
            return analysis
        
        except Exception as e:
            logger.error(f"HTML structure analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _analyze_css_structure(self, source_code: str, file_path: str) -> Dict[str, Any]:
        """Perform basic CSS structure analysis."""
        try:
            analysis = {
                'selectors': {
                    'id_selectors': len(re.findall(r'#[\w-]+', source_code)),
                    'class_selectors': len(re.findall(r'\.[\w-]+', source_code)),
                    'element_selectors': len(re.findall(r'^[a-zA-Z][a-zA-Z0-9]*\s*{', source_code, re.MULTILINE)),
                    'attribute_selectors': len(re.findall(r'\[[^\]]+\]', source_code)),
                    'pseudo_selectors': len(re.findall(r':[\w-]+', source_code))
                },
                'properties': {
                    'color_properties': len(re.findall(r'color\s*:', source_code, re.IGNORECASE)),
                    'font_properties': len(re.findall(r'font-?\w*\s*:', source_code, re.IGNORECASE)),
                    'layout_properties': len(re.findall(r'(margin|padding|width|height|display|position)\s*:', source_code, re.IGNORECASE)),
                    'background_properties': len(re.findall(r'background-?\w*\s*:', source_code, re.IGNORECASE))
                },
                'media_queries': len(re.findall(r'@media', source_code, re.IGNORECASE)),
                'imports': len(re.findall(r'@import', source_code, re.IGNORECASE)),
                'keyframes': len(re.findall(r'@keyframes', source_code, re.IGNORECASE)),
                'comments': len(re.findall(r'/\*.*?\*/', source_code, re.DOTALL)),
                'has_css_variables': '--' in source_code,
                'uses_flexbox': 'flex' in source_code.lower(),
                'uses_grid': 'grid' in source_code.lower()
            }
            
            # Calculate total rules (approximate)
            analysis['total_rules'] = len(re.findall(r'{[^}]*}', source_code))
            
            # Basic organization assessment
            analysis['organization'] = {
                'has_imports': analysis['imports'] > 0,
                'has_media_queries': analysis['media_queries'] > 0,
                'uses_modern_features': analysis['has_css_variables'] or analysis['uses_flexbox'] or analysis['uses_grid'],
                'is_commented': analysis['comments'] > 0
            }
            
            return analysis
        
        except Exception as e:
            logger.error(f"CSS structure analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _analyze_js_structure(self, source_code: str, file_path: str) -> Dict[str, Any]:
        """Perform basic JavaScript structure analysis."""
        try:
            analysis = {
                'functions': {
                    'function_declarations': len(re.findall(r'function\s+\w+', source_code)),
                    'arrow_functions': len(re.findall(r'=>', source_code)),
                    'anonymous_functions': len(re.findall(r'function\s*\(', source_code)),
                    'method_definitions': len(re.findall(r'\w+\s*:\s*function', source_code))
                },
                'variables': {
                    'var_declarations': len(re.findall(r'\bvar\s+', source_code)),
                    'let_declarations': len(re.findall(r'\blet\s+', source_code)),
                    'const_declarations': len(re.findall(r'\bconst\s+', source_code))
                },
                'classes': len(re.findall(r'\bclass\s+\w+', source_code)),
                'imports': {
                    'import_statements': len(re.findall(r'\bimport\s+', source_code)),
                    'require_statements': len(re.findall(r'\brequire\s*\(', source_code))
                },
                'control_structures': {
                    'if_statements': len(re.findall(r'\bif\s*\(', source_code)),
                    'for_loops': len(re.findall(r'\bfor\s*\(', source_code)),
                    'while_loops': len(re.findall(r'\bwhile\s*\(', source_code)),
                    'try_catch': len(re.findall(r'\btry\s*{', source_code))
                },
                'dom_interactions': {
                    'getelementbyid': len(re.findall(r'getElementById', source_code, re.IGNORECASE)),
                    'queryselector': len(re.findall(r'querySelector', source_code, re.IGNORECASE)),
                    'addeventlistener': len(re.findall(r'addEventListener', source_code, re.IGNORECASE)),
                    'jquery': '$(' in source_code or 'jQuery(' in source_code
                },
                'comments': {
                    'single_line': len(re.findall(r'//.*', source_code)),
                    'multi_line': len(re.findall(r'/\*.*?\*/', source_code, re.DOTALL))
                },
                'async_patterns': {
                    'promises': 'Promise' in source_code,
                    'async_await': 'async' in source_code and 'await' in source_code,
                    'callbacks': len(re.findall(r'callback|cb', source_code, re.IGNORECASE))
                }
            }
            
            # ES6+ features detection
            analysis['modern_features'] = {
                'arrow_functions': analysis['functions']['arrow_functions'] > 0,
                'destructuring': '{' in source_code and '}' in source_code and '=' in source_code,
                'template_literals': '`' in source_code,
                'spread_operator': '...' in source_code,
                'modules': analysis['imports']['import_statements'] > 0
            }
            
            # Code quality indicators
            analysis['quality_indicators'] = {
                'uses_strict_mode': "'use strict'" in source_code or '"use strict"' in source_code,
                'has_comments': (analysis['comments']['single_line'] + analysis['comments']['multi_line']) > 0,
                'uses_modern_syntax': any(analysis['modern_features'].values()),
                'error_handling': analysis['control_structures']['try_catch'] > 0
            }
            
            return analysis
        
        except Exception as e:
            logger.error(f"JavaScript structure analysis failed for {file_path}: {e}")
            return {'error': str(e)}
    
    def _create_html_content_text(self, source_code: str, basic_analysis: Dict[str, Any], 
                                validation_results: Dict[str, Any]) -> str:
        """Create comprehensive text content for HTML file."""
        content_parts = []
        
        content_parts.append("HTML DOCUMENT ANALYSIS")
        content_parts.append("=" * 50)
        
        if 'error' not in basic_analysis:
            # Document structure
            content_parts.append("DOCUMENT STRUCTURE:")
            content_parts.append(f"  Doctype: {'✓' if basic_analysis.get('has_doctype') else '✗'}")
            content_parts.append(f"  HTML tag: {'✓' if basic_analysis.get('has_html_tag') else '✗'}")
            content_parts.append(f"  Head section: {'✓' if basic_analysis.get('has_head_tag') else '✗'}")
            content_parts.append(f"  Body section: {'✓' if basic_analysis.get('has_body_tag') else '✗'}")
            content_parts.append(f"  Title: {basic_analysis.get('title', 'No title')}")
            content_parts.append("")
            
            # Content overview
            content_parts.append("CONTENT OVERVIEW:")
            content_parts.append(f"  Headings: {sum(basic_analysis.get('headings', {}).values())}")
            content_parts.append(f"  Links: {basic_analysis.get('links', 0)}")
            content_parts.append(f"  Images: {basic_analysis.get('images', 0)}")
            content_parts.append(f"  Forms: {basic_analysis.get('forms', 0)}")
            content_parts.append(f"  Scripts: {basic_analysis.get('scripts', 0)}")
            content_parts.append("")
            
            # Accessibility
            if 'accessibility' in basic_analysis:
                acc = basic_analysis['accessibility']
                content_parts.append("ACCESSIBILITY:")
                content_parts.append(f"  Images with alt text: {acc.get('images_with_alt', 0)}")
                content_parts.append(f"  Images without alt text: {acc.get('images_without_alt', 0)}")
                content_parts.append(f"  Language attribute: {'✓' if acc.get('has_lang_attribute') else '✗'}")
                content_parts.append(f"  Viewport meta tag: {'✓' if acc.get('has_viewport_meta') else '✗'}")
                content_parts.append("")
        
        # Validation results
        if validation_results and 'error' not in validation_results:
            content_parts.append("VALIDATION RESULTS:")
            if 'summary' in validation_results:
                summary = validation_results['summary']
                content_parts.append(f"  Overall Status: {summary.get('status', 'unknown')}")
                content_parts.append(f"  Errors: {summary.get('errors', 0)}")
                content_parts.append(f"  Warnings: {summary.get('warnings', 0)}")
                content_parts.append("")
        
        # Source code
        content_parts.append("SOURCE CODE:")
        content_parts.append("-" * 30)
        content_parts.append(source_code)
        
        return "\n".join(content_parts)
    
    def _create_css_content_text(self, source_code: str, basic_analysis: Dict[str, Any], 
                               analysis_results: Dict[str, Any]) -> str:
        """Create comprehensive text content for CSS file."""
        content_parts = []
        
        content_parts.append("CSS STYLESHEET ANALYSIS")
        content_parts.append("=" * 50)
        
        if 'error' not in basic_analysis:
            # Selectors overview
            content_parts.append("SELECTORS:")
            selectors = basic_analysis.get('selectors', {})
            content_parts.append(f"  ID selectors: {selectors.get('id_selectors', 0)}")
            content_parts.append(f"  Class selectors: {selectors.get('class_selectors', 0)}")
            content_parts.append(f"  Element selectors: {selectors.get('element_selectors', 0)}")
            content_parts.append(f"  Total rules: {basic_analysis.get('total_rules', 0)}")
            content_parts.append("")
            
            # Features
            content_parts.append("FEATURES:")
            content_parts.append(f"  Media queries: {basic_analysis.get('media_queries', 0)}")
            content_parts.append(f"  CSS variables: {'✓' if basic_analysis.get('has_css_variables') else '✗'}")
            content_parts.append(f"  Flexbox: {'✓' if basic_analysis.get('uses_flexbox') else '✗'}")
            content_parts.append(f"  Grid: {'✓' if basic_analysis.get('uses_grid') else '✗'}")
            content_parts.append("")
        
        # Analysis results
        if analysis_results and 'error' not in analysis_results:
            content_parts.append("VALIDATION RESULTS:")
            if 'summary' in analysis_results:
                summary = analysis_results['summary']
                content_parts.append(f"  Status: {summary.get('status', 'unknown')}")
                content_parts.append(f"  Issues: {summary.get('total_issues', 0)}")
                content_parts.append("")
        
        # Source code
        content_parts.append("SOURCE CODE:")
        content_parts.append("-" * 30)
        content_parts.append(source_code)
        
        return "\n".join(content_parts)
    
    def _create_js_content_text(self, source_code: str, basic_analysis: Dict[str, Any], 
                              analysis_results: Dict[str, Any]) -> str:
        """Create comprehensive text content for JavaScript file."""
        content_parts = []
        
        content_parts.append("JAVASCRIPT CODE ANALYSIS")
        content_parts.append("=" * 50)
        
        if 'error' not in basic_analysis:
            # Functions overview
            functions = basic_analysis.get('functions', {})
            total_functions = sum(functions.values())
            content_parts.append("FUNCTIONS:")
            content_parts.append(f"  Total functions: {total_functions}")
            content_parts.append(f"  Function declarations: {functions.get('function_declarations', 0)}")
            content_parts.append(f"  Arrow functions: {functions.get('arrow_functions', 0)}")
            content_parts.append("")
            
            # Variables
            variables = basic_analysis.get('variables', {})
            content_parts.append("VARIABLES:")
            content_parts.append(f"  var: {variables.get('var_declarations', 0)}")
            content_parts.append(f"  let: {variables.get('let_declarations', 0)}")
            content_parts.append(f"  const: {variables.get('const_declarations', 0)}")
            content_parts.append("")
            
            # Modern features
            if 'modern_features' in basic_analysis:
                modern = basic_analysis['modern_features']
                content_parts.append("MODERN FEATURES:")
                for feature, used in modern.items():
                    content_parts.append(f"  {feature.replace('_', ' ').title()}: {'✓' if used else '✗'}")
                content_parts.append("")
        
        # Analysis results
        if analysis_results and 'error' not in analysis_results:
            content_parts.append("CODE ANALYSIS:")
            if 'summary' in analysis_results:
                summary = analysis_results['summary']
                content_parts.append(f"  Quality: {summary.get('quality', 'unknown')}")
                content_parts.append(f"  Issues: {summary.get('total_issues', 0)}")
                content_parts.append("")
        
        # Source code
        content_parts.append("SOURCE CODE:")
        content_parts.append("-" * 30)
        content_parts.append(source_code)
        
        return "\n".join(content_parts)