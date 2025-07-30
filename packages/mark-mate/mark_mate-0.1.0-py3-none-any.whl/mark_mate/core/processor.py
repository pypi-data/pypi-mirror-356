"""
MarkMate Core Processor

Handles the main content extraction and processing logic.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from ..extractors import (
    BaseExtractor, 
    OfficeExtractor, 
    CodeExtractor, 
    WebExtractor, 
    ReactExtractor,
    GitHubExtractor
)
from ..utils.file_detection import detect_file_type
from ..utils.encoding_utils import detect_encoding

logger = logging.getLogger(__name__)


class AssignmentProcessor:
    """Main processor for student assignment content extraction."""
    
    def __init__(self):
        """Initialize the processor with available extractors."""
        self.extractors = {
            'office': OfficeExtractor(),
            'code': CodeExtractor(),
            'web': WebExtractor(),
            'react': ReactExtractor(),
            'github': GitHubExtractor()
        }
    
    def process_submission(self, submission_path: str, student_id: str, 
                          wordpress: bool = False, github_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a single student submission.
        
        Args:
            submission_path: Path to the student's submission file/folder
            student_id: Student identifier
            wordpress: Enable WordPress-specific processing
            github_url: Optional GitHub repository URL for analysis
            
        Returns:
            Dictionary containing extracted content and metadata
        """
        result = {
            "student_id": student_id,
            "submission_path": submission_path,
            "processed": False,
            "timestamp": datetime.now().isoformat(),
            "content": {},
            "metadata": {
                "wordpress_mode": wordpress,
                "github_analysis": bool(github_url),
                "file_types_detected": [],
                "extractors_used": [],
                "errors": []
            }
        }
        
        try:
            if os.path.isfile(submission_path):
                # Single file submission
                result.update(self._process_file(submission_path, wordpress, github_url))
            elif os.path.isdir(submission_path):
                # Directory submission
                result.update(self._process_directory(submission_path, wordpress, github_url))
            else:
                raise FileNotFoundError(f"Submission path does not exist: {submission_path}")
            
            result["processed"] = True
            logger.info(f"Successfully processed submission for student {student_id}")
            
        except Exception as e:
            error_msg = f"Error processing submission for student {student_id}: {str(e)}"
            logger.error(error_msg)
            result["metadata"]["errors"].append(error_msg)
        
        return result
    
    def _process_file(self, file_path: str, wordpress: bool, github_url: Optional[str]) -> Dict[str, Any]:
        """Process a single file submission."""
        content = {}
        metadata = {"file_types_detected": [], "extractors_used": [], "errors": []}
        
        file_type = detect_file_type(file_path)
        metadata["file_types_detected"].append(file_type)
        
        # Select appropriate extractor
        extractor = self._get_extractor_for_file_type(file_type)
        if extractor:
            try:
                extracted = extractor.extract(file_path)
                content.update(extracted)
                metadata["extractors_used"].append(extractor.__class__.__name__)
            except Exception as e:
                error_msg = f"Extraction failed for {file_path}: {str(e)}"
                metadata["errors"].append(error_msg)
                logger.warning(error_msg)
        
        # GitHub analysis if URL provided
        if github_url:
            try:
                github_content = self.extractors['github'].extract(github_url)
                content["github_analysis"] = github_content
                metadata["extractors_used"].append("GitHubExtractor")
            except Exception as e:
                error_msg = f"GitHub analysis failed for {github_url}: {str(e)}"
                metadata["errors"].append(error_msg)
                logger.warning(error_msg)
        
        return {"content": content, "metadata": metadata}
    
    def _process_directory(self, dir_path: str, wordpress: bool, github_url: Optional[str]) -> Dict[str, Any]:
        """Process a directory submission."""
        content = {}
        metadata = {"file_types_detected": [], "extractors_used": [], "errors": []}
        
        # WordPress-specific processing
        if wordpress:
            content.update(self._process_wordpress_directory(dir_path, metadata))
        
        # Process all files in directory
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip hidden files and system files
                if file.startswith('.') or '__pycache__' in file_path:
                    continue
                
                file_type = detect_file_type(file_path)
                if file_type not in metadata["file_types_detected"]:
                    metadata["file_types_detected"].append(file_type)
                
                extractor = self._get_extractor_for_file_type(file_type)
                if extractor:
                    try:
                        extracted = extractor.extract(file_path)
                        # Organize by file type
                        if file_type not in content:
                            content[file_type] = []
                        content[file_type].append({
                            "file_path": os.path.relpath(file_path, dir_path),
                            "content": extracted
                        })
                        
                        if extractor.__class__.__name__ not in metadata["extractors_used"]:
                            metadata["extractors_used"].append(extractor.__class__.__name__)
                            
                    except Exception as e:
                        error_msg = f"Extraction failed for {file_path}: {str(e)}"
                        metadata["errors"].append(error_msg)
                        logger.debug(error_msg)
        
        # GitHub analysis if URL provided
        if github_url:
            try:
                github_content = self.extractors['github'].extract(github_url)
                content["github_analysis"] = github_content
                metadata["extractors_used"].append("GitHubExtractor")
            except Exception as e:
                error_msg = f"GitHub analysis failed for {github_url}: {str(e)}"
                metadata["errors"].append(error_msg)
                logger.warning(error_msg)
        
        return {"content": content, "metadata": metadata}
    
    def _process_wordpress_directory(self, dir_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Process WordPress-specific directory structure."""
        wordpress_content = {}
        
        # Look for WordPress-specific directories and files
        wordpress_dirs = ['themes', 'plugins', 'uploads', 'database']
        
        for wp_dir in wordpress_dirs:
            wp_path = os.path.join(dir_path, 'wordpress_backup', wp_dir)
            if os.path.exists(wp_path):
                try:
                    # Process WordPress directory
                    wp_content = self._analyze_wordpress_component(wp_path, wp_dir)
                    if wp_content:
                        wordpress_content[f"wordpress_{wp_dir}"] = wp_content
                except Exception as e:
                    error_msg = f"WordPress {wp_dir} processing failed: {str(e)}"
                    metadata["errors"].append(error_msg)
                    logger.warning(error_msg)
        
        return wordpress_content
    
    def _analyze_wordpress_component(self, component_path: str, component_type: str) -> Dict[str, Any]:
        """Analyze a specific WordPress component (themes, plugins, etc.)."""
        analysis = {
            "component_type": component_type,
            "path": component_path,
            "files_found": [],
            "analysis": {}
        }
        
        # Count files and analyze structure
        for root, dirs, files in os.walk(component_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, component_path)
                analysis["files_found"].append(rel_path)
        
        # Component-specific analysis
        if component_type == "themes":
            analysis["analysis"] = self._analyze_themes(component_path)
        elif component_type == "plugins":
            analysis["analysis"] = self._analyze_plugins(component_path)
        elif component_type == "uploads":
            analysis["analysis"] = self._analyze_uploads(component_path)
        elif component_type == "database":
            analysis["analysis"] = self._analyze_database(component_path)
        
        return analysis
    
    def _analyze_themes(self, themes_path: str) -> Dict[str, Any]:
        """Analyze WordPress themes."""
        return {
            "theme_count": len([d for d in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, d))]),
            "themes_found": [d for d in os.listdir(themes_path) if os.path.isdir(os.path.join(themes_path, d))]
        }
    
    def _analyze_plugins(self, plugins_path: str) -> Dict[str, Any]:
        """Analyze WordPress plugins."""
        plugins = [d for d in os.listdir(plugins_path) if os.path.isdir(os.path.join(plugins_path, d))]
        
        # Check for AI-related plugins
        ai_keywords = ['ai', 'artificial', 'intelligence', 'gpt', 'chatbot', 'assistant']
        ai_plugins = []
        
        for plugin in plugins:
            plugin_lower = plugin.lower()
            if any(keyword in plugin_lower for keyword in ai_keywords):
                ai_plugins.append(plugin)
        
        return {
            "plugin_count": len(plugins),
            "plugins_found": plugins,
            "ai_plugins": ai_plugins,
            "has_ai_plugins": len(ai_plugins) > 0
        }
    
    def _analyze_uploads(self, uploads_path: str) -> Dict[str, Any]:
        """Analyze WordPress uploads."""
        file_types = {}
        total_files = 0
        
        for root, dirs, files in os.walk(uploads_path):
            for file in files:
                total_files += 1
                ext = Path(file).suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            "total_files": total_files,
            "file_types": file_types,
            "has_media": total_files > 0
        }
    
    def _analyze_database(self, database_path: str) -> Dict[str, Any]:
        """Analyze WordPress database files."""
        db_files = [f for f in os.listdir(database_path) if f.endswith(('.sql', '.gz', '.zip'))]
        
        return {
            "database_files": db_files,
            "has_database": len(db_files) > 0
        }
    
    def _get_extractor_for_file_type(self, file_type: str) -> Optional[BaseExtractor]:
        """Get the appropriate extractor for a file type."""
        extractor_mapping = {
            'pdf': 'office',
            'docx': 'office',
            'txt': 'office',
            'md': 'office',
            'py': 'code',
            'js': 'web',
            'html': 'web',
            'css': 'web',
            'tsx': 'react',
            'ts': 'react',
            'jsx': 'react',
            'json': 'code',
            'ipynb': 'code'
        }
        
        extractor_name = extractor_mapping.get(file_type)
        return self.extractors.get(extractor_name) if extractor_name else None