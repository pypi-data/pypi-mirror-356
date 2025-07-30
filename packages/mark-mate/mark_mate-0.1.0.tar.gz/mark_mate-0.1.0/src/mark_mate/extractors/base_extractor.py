"""
Base extractor class for the content extraction system.

This module provides the abstract base class that all extractors should inherit from,
ensuring consistent interface and behavior across different file type extractors.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import os

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Abstract base class for all content extractors."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the extractor.
        
        Args:
            config: Optional configuration dictionary for extractor settings
        """
        self.config = config or {}
        self.supported_extensions: List[str] = []
        self.extractor_name: str = ""
    
    @abstractmethod
    def can_extract(self, file_path: str) -> bool:
        """
        Check if this extractor can handle the given file.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if this extractor can handle the file, False otherwise
        """
        pass
    
    @abstractmethod
    def extract_content(self, file_path: str) -> Dict[str, Any]:
        """
        Extract content from the specified file.
        
        Args:
            file_path: Path to the file to extract content from
            
        Returns:
            Dictionary containing extracted content and metadata
        """
        pass
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get basic file information.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file metadata
        """
        try:
            stat = os.stat(file_path)
            return {
                'filename': os.path.basename(file_path),
                'size': stat.st_size,
                'extension': os.path.splitext(file_path)[1].lower(),
                'extractor': self.extractor_name
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return {
                'filename': os.path.basename(file_path),
                'size': 0,
                'extension': os.path.splitext(file_path)[1].lower(),
                'extractor': self.extractor_name,
                'error': str(e)
            }
    
    def create_error_result(self, file_path: str, error: Exception) -> Dict[str, Any]:
        """
        Create a standardized error result.
        
        Args:
            file_path: Path to the file that caused the error
            error: The exception that occurred
            
        Returns:
            Standardized error result dictionary
        """
        return {
            'success': False,
            'error': str(error),
            'file_info': self.get_file_info(file_path),
            'extractor': self.extractor_name,
            'content': f"[EXTRACTION ERROR] Could not process {os.path.basename(file_path)}: {str(error)[:100]}"
        }
    
    def create_success_result(self, file_path: str, content: str, 
                            analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a standardized success result.
        
        Args:
            file_path: Path to the successfully processed file
            content: Extracted text content
            analysis: Optional analysis results
            
        Returns:
            Standardized success result dictionary
        """
        return {
            'success': True,
            'content': content,
            'file_info': self.get_file_info(file_path),
            'extractor': self.extractor_name,
            'analysis': analysis or {},
            'content_length': len(content) if content else 0
        }