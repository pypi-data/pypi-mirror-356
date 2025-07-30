#!/usr/bin/env python3
"""
MarkMate Extract Command

Extracts and analyzes content from student submissions with comprehensive multi-format support.
"""

import argparse
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def add_parser(subparsers) -> argparse.ArgumentParser:
    """Add extract command parser."""
    parser = subparsers.add_parser(
        "extract",
        help="Extract and analyze content from student submissions",
        description="Processes submissions with multi-format support, GitHub analysis, and WordPress processing"
    )
    
    parser.add_argument(
        "submissions_folder",
        help="Path to processed submissions folder"
    )
    
    parser.add_argument(
        "--output",
        default="extracted_content.json",
        help="Output JSON file for extracted content (default: extracted_content.json)"
    )
    
    parser.add_argument(
        "--wordpress",
        action="store_true",
        help="Enable WordPress-specific processing"
    )
    
    parser.add_argument(
        "--github-urls",
        help="Path to GitHub URL mapping file (from scan command)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without actually extracting content"
    )
    
    parser.add_argument(
        "--max-students",
        type=int,
        help="Maximum number of students to process (for testing)"
    )
    
    return parser


def load_github_urls(github_urls_file):
    """
    Load GitHub URL mappings from file.
    
    Args:
        github_urls_file: Path to the GitHub URLs mapping file
        
    Returns:
        Dictionary mapping student IDs to GitHub URLs
    """
    github_urls = {}
    
    if not github_urls_file or not os.path.exists(github_urls_file):
        return github_urls
    
    try:
        with open(github_urls_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if ':' in line:
                        student_id, url = line.split(':', 1)
                        github_urls[student_id.strip()] = url.strip()
        
        logger.info(f"Loaded GitHub URLs for {len(github_urls)} students")
    except Exception as e:
        logger.error(f"Error loading GitHub URLs file: {e}")
    
    return github_urls


def extract_student_id_from_path(file_path):
    """Extract student ID from file path."""
    import re
    path_parts = Path(file_path).parts
    
    # Look for 3-digit patterns in path components
    for part in reversed(path_parts):
        # Pattern: _123_ or just 123
        match = re.search(r'_?(\d{3})_?', part)
        if match:
            return match.group(1)
    
    return None


def find_student_submissions(submissions_folder, max_students=None):
    """
    Find all student submission files/folders.
    
    Args:
        submissions_folder: Path to submissions folder
        max_students: Maximum number of students to process
        
    Returns:
        Dictionary mapping student IDs to submission paths
    """
    submissions = {}
    
    if not os.path.exists(submissions_folder):
        logger.error(f"Submissions folder does not exist: {submissions_folder}")
        return submissions
    
    # Find all student files/folders
    for item in os.listdir(submissions_folder):
        item_path = os.path.join(submissions_folder, item)
        student_id = extract_student_id_from_path(item)
        
        if student_id and (os.path.isfile(item_path) or os.path.isdir(item_path)):
            submissions[student_id] = item_path
            
            if max_students and len(submissions) >= max_students:
                break
    
    return submissions


def extract_submission_content(submission_path, student_id, wordpress=False, github_url=None):
    """
    Extract content from a single student submission.
    
    Args:
        submission_path: Path to the student's submission
        student_id: Student ID
        wordpress: Whether to enable WordPress processing
        github_url: GitHub repository URL for the student
        
    Returns:
        Dictionary containing extracted content and metadata
    """
    from ..core.processor import AssignmentProcessor
    
    try:
        processor = AssignmentProcessor()
        result = processor.process_submission(
            submission_path, 
            student_id,
            wordpress=wordpress,
            github_url=github_url
        )
        
        logger.info(f"Successfully processed student {student_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing student {student_id}: {e}")
        return {
            "student_id": student_id,
            "error": str(e),
            "processed": False,
            "timestamp": datetime.now().isoformat()
        }


def main(args) -> int:
    """Main extraction logic."""
    submissions_folder = args.submissions_folder
    output_file = args.output
    wordpress = args.wordpress
    github_urls_file = args.github_urls
    dry_run = args.dry_run
    max_students = args.max_students
    
    logger.info(f"Processing submissions from: {submissions_folder}")
    if wordpress:
        logger.info("WordPress processing enabled")
    if github_urls_file:
        logger.info(f"GitHub URLs file: {github_urls_file}")
    if dry_run:
        logger.info("DRY RUN MODE - No content will be extracted")
    
    # Load GitHub URLs
    github_urls = load_github_urls(github_urls_file)
    
    # Find student submissions
    submissions = find_student_submissions(submissions_folder, max_students)
    
    if not submissions:
        logger.error("No student submissions found")
        return 1
    
    logger.info(f"Found {len(submissions)} student submissions")
    
    if dry_run:
        logger.info("DRY RUN - Would process the following students:")
        for student_id, path in sorted(submissions.items()):
            github_info = f" (GitHub: {github_urls.get(student_id, 'None')})" if github_urls_file else ""
            logger.info(f"  {student_id}: {path}{github_info}")
        return 0
    
    # Process each submission
    extracted_content = {
        "extraction_session": {
            "timestamp": datetime.now().isoformat(),
            "total_students": len(submissions),
            "wordpress_mode": wordpress,
            "github_analysis": bool(github_urls_file),
            "submissions_folder": submissions_folder
        },
        "students": {}
    }
    
    processed_count = 0
    for student_id, submission_path in sorted(submissions.items()):
        logger.info(f"Processing student {student_id} ({processed_count + 1}/{len(submissions)})")
        
        github_url = github_urls.get(student_id)
        
        result = extract_submission_content(
            submission_path, 
            student_id, 
            wordpress=wordpress, 
            github_url=github_url
        )
        
        extracted_content["students"][student_id] = result
        processed_count += 1
    
    # Save results
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_content, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Content extraction complete!")
        logger.info(f"Processed {processed_count} students")
        logger.info(f"Results saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        return 1