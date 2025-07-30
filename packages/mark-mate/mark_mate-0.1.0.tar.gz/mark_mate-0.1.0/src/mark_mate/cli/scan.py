#!/usr/bin/env python3
"""
MarkMate Scan Command

Scans processed submissions for GitHub repository URLs and creates mapping files.
"""

import argparse
import os
import re
import logging
from pathlib import Path
from collections import defaultdict
import zipfile
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def add_parser(subparsers) -> argparse.ArgumentParser:
    """Add scan command parser."""
    parser = subparsers.add_parser(
        "scan",
        help="Scan submissions for GitHub repository URLs",
        description="Detects GitHub repository URLs in student submissions and creates mapping files"
    )
    
    parser.add_argument(
        "submissions_folder",
        help="Path to processed submissions folder"
    )
    
    parser.add_argument(
        "--output",
        default="github_urls.txt",
        help="Output file for GitHub URL mappings (default: github_urls.txt)"
    )
    
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Text encoding to use when reading files (default: utf-8)"
    )
    
    return parser


def extract_github_urls_from_text(text):
    """
    Extract GitHub repository URLs from text using comprehensive regex patterns.
    
    Args:
        text: Text content to scan for URLs
        
    Returns:
        List of unique GitHub repository URLs found
    """
    github_patterns = [
        # Standard GitHub repository URLs
        r'https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?(?:\.git)?',
        r'http://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?(?:\.git)?',
        
        # GitHub URLs without protocol
        r'github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?(?:\.git)?',
        
        # Git clone URLs
        r'git@github\.com:[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+(?:\.git)?',
        
        # Markdown link format
        r'\[.*?\]\(https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?(?:\.git)?\)',
        
        # URLs in quotes
        r'"https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?(?:\.git)?"',
        r"'https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?(?:\.git)?'",
    ]
    
    urls = set()
    
    for pattern in github_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # Clean up the URL
            url = clean_github_url(match)
            if url:
                urls.add(url)
    
    return list(urls)


def clean_github_url(url):
    """
    Clean and normalize a GitHub URL.
    
    Args:
        url: Raw GitHub URL string
        
    Returns:
        Cleaned GitHub repository URL
    """
    # Remove markdown formatting
    if url.startswith('[') and '](' in url:
        url = url.split('](')[1].rstrip(')')
    
    # Remove quotes
    url = url.strip('"\'')
    
    # Convert SSH to HTTPS
    if url.startswith('git@github.com:'):
        url = url.replace('git@github.com:', 'https://github.com/')
    
    # Add protocol if missing
    if url.startswith('github.com'):
        url = 'https://' + url
    
    # Remove .git suffix
    if url.endswith('.git'):
        url = url[:-4]
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    # Validate URL format
    if not re.match(r'https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$', url):
        return None
    
    return url


def extract_student_id_from_path(file_path):
    """Extract student ID from file path."""
    # Try to extract from filename or parent directory
    path_parts = Path(file_path).parts
    
    # Look for 3-digit patterns in path components
    for part in reversed(path_parts):
        # Pattern: _123_ or just 123
        match = re.search(r'_?(\d{3})_?', part)
        if match:
            return match.group(1)
    
    return None


def scan_text_file(file_path, encoding='utf-8'):
    """
    Scan a text file for GitHub URLs.
    
    Args:
        file_path: Path to the file to scan
        encoding: Text encoding to use
        
    Returns:
        List of GitHub URLs found in the file
    """
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
            return extract_github_urls_from_text(content)
    except Exception as e:
        logger.debug(f"Could not read file {file_path}: {e}")
        return []


def scan_zip_file(zip_path, encoding='utf-8'):
    """
    Scan files within a zip archive for GitHub URLs.
    
    Args:
        zip_path: Path to the zip file
        encoding: Text encoding to use
        
    Returns:
        List of GitHub URLs found in the zip file
    """
    urls = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.filelist:
                if file_info.is_dir():
                    continue
                
                # Only scan text-based files
                if is_text_file(file_info.filename):
                    try:
                        with zip_ref.open(file_info) as f:
                            content = f.read().decode(encoding, errors='ignore')
                            file_urls = extract_github_urls_from_text(content)
                            urls.extend(file_urls)
                    except Exception as e:
                        logger.debug(f"Could not read {file_info.filename} from {zip_path}: {e}")
    
    except zipfile.BadZipFile:
        logger.debug(f"Could not read zip file: {zip_path}")
    
    return urls


def is_text_file(filename):
    """Check if a file is likely to contain text."""
    text_extensions = {
        '.txt', '.md', '.readme', '.doc', '.docx', '.pdf',
        '.py', '.js', '.html', '.css', '.json', '.xml',
        '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf'
    }
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in text_extensions or not file_ext  # Include files without extensions


def scan_submissions_folder(folder_path, encoding='utf-8'):
    """
    Scan a folder of student submissions for GitHub URLs.
    
    Args:
        folder_path: Path to the submissions folder
        encoding: Text encoding to use
        
    Returns:
        Dictionary mapping student IDs to lists of GitHub URLs
    """
    student_urls = defaultdict(list)
    
    if not os.path.exists(folder_path):
        logger.error(f"Submissions folder does not exist: {folder_path}")
        return student_urls
    
    # Scan all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Extract student ID from file path
            student_id = extract_student_id_from_path(file_path)
            if not student_id:
                continue
            
            urls = []
            
            # Handle different file types
            if filename.lower().endswith('.zip'):
                urls = scan_zip_file(file_path, encoding)
            elif is_text_file(filename):
                urls = scan_text_file(file_path, encoding)
            
            # Add URLs to student's list
            for url in urls:
                if url not in student_urls[student_id]:
                    student_urls[student_id].append(url)
                    logger.info(f"Found GitHub URL for student {student_id}: {url}")
    
    return student_urls


def write_url_mapping(student_urls, output_file):
    """
    Write student ID to GitHub URL mappings to a file.
    
    Args:
        student_urls: Dictionary mapping student IDs to lists of URLs
        output_file: Output file path
    """
    with open(output_file, 'w') as f:
        f.write("# MarkMate GitHub URL Mappings\n")
        f.write("# Format: student_id:github_url\n")
        f.write("# You can edit this file to add or correct URLs\n\n")
        
        for student_id, urls in sorted(student_urls.items()):
            if urls:
                # Use the first URL found, or user can edit manually
                primary_url = urls[0]
                f.write(f"{student_id}:{primary_url}\n")
                
                # Add other URLs as comments
                for url in urls[1:]:
                    f.write(f"# {student_id}:{url}\n")
            else:
                f.write(f"# {student_id}:NO_URL_FOUND\n")
        
        f.write("\n# End of mappings\n")


def main(args) -> int:
    """Main scanning logic."""
    folder_path = args.submissions_folder
    output_file = args.output
    encoding = args.encoding
    
    logger.info(f"Scanning submissions folder: {folder_path}")
    logger.info(f"Using encoding: {encoding}")
    
    # Scan for GitHub URLs
    student_urls = scan_submissions_folder(folder_path, encoding)
    
    if not student_urls:
        logger.warning("No GitHub URLs found in any submissions")
        return 1
    
    # Write mapping file
    write_url_mapping(student_urls, output_file)
    
    logger.info(f"GitHub URL scanning complete!")
    logger.info(f"Found URLs for {len([s for s, urls in student_urls.items() if urls])} students")
    logger.info(f"Total students processed: {len(student_urls)}")
    logger.info(f"URL mappings saved to: {output_file}")
    logger.info("You can edit the mapping file to add or correct URLs before extraction.")
    
    return 0