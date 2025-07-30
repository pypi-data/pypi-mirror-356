#!/usr/bin/env python3
"""
MarkMate Consolidate Command

Consolidates and organizes student submission files with intelligent filtering.
"""

import argparse
import os
import re
import zipfile
import shutil
import tempfile
from pathlib import Path
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def add_parser(subparsers) -> argparse.ArgumentParser:
    """Add consolidate command parser."""
    parser = subparsers.add_parser(
        "consolidate",
        help="Consolidate and organize student submission files",
        description="Groups files by student ID, extracts archives, and filters Mac system files"
    )
    
    parser.add_argument(
        "folder_path",
        help="Path to folder containing student submissions"
    )
    
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="Discard zip files instead of extracting them"
    )
    
    parser.add_argument(
        "--wordpress",
        action="store_true",
        help="Enable WordPress-specific processing for UpdraftPlus backups"
    )
    
    parser.add_argument(
        "--keep-mac-files",
        action="store_true",
        help="Preserve Mac system files (default: filter them out)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="processed_submissions",
        help="Output directory for processed submissions (default: processed_submissions)"
    )
    
    return parser


def extract_student_id(filename):
    """Extract student ID from filename using regex pattern."""
    # Pattern matches: _<STUDENT_ID>_ where STUDENT_ID is the first 3 digits surrounded by underscores
    pattern = r'_(\d{3})_'
    match = re.search(pattern, filename)
    return match.group(1) if match else None


def get_file_extension(filename):
    """Get the file extension, handling special cases."""
    # Handle files without extensions
    if '.' not in filename:
        return ''
    
    # Get the last part after the last dot
    ext = filename.split('.')[-1].lower()
    
    # Handle double extensions like .zip.zip
    if filename.lower().endswith('.zip.zip'):
        return 'zip'
    
    return ext


def is_mac_system_file(filename):
    """Check if file is a Mac system file that should be filtered."""
    mac_system_patterns = [
        '.DS_Store',
        '._',  # Resource fork files
        '__MACOSX',
        '.Spotlight-V100',
        '.Trashes',
        '.TemporaryItems',
        '.fseventsd',
    ]
    
    # Check if filename starts with any Mac system pattern
    for pattern in mac_system_patterns:
        if filename.startswith(pattern) or pattern in filename:
            return True
    
    return False


def is_wordpress_backup_file(filename):
    """Check if file is a WordPress UpdraftPlus backup file."""
    wordpress_patterns = [
        '-themes.zip',
        '-plugins.zip', 
        '-uploads.zip',
        '-db.gz',
        '-others.zip',
        'backup_'
    ]
    
    return any(pattern in filename.lower() for pattern in wordpress_patterns)


def organize_wordpress_files(files, student_id, output_dir):
    """Organize WordPress backup files into structured directories."""
    student_dir = os.path.join(output_dir, f"{student_id}")
    wordpress_dir = os.path.join(student_dir, "wordpress_backup")
    
    # Create directory structure
    subdirs = {
        'themes': os.path.join(wordpress_dir, 'themes'),
        'plugins': os.path.join(wordpress_dir, 'plugins'),
        'uploads': os.path.join(wordpress_dir, 'uploads'),
        'database': os.path.join(wordpress_dir, 'database'),
        'others': os.path.join(wordpress_dir, 'others'),
        'originals': os.path.join(student_dir, 'original_backups')
    }
    
    for subdir in subdirs.values():
        os.makedirs(subdir, exist_ok=True)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        # Copy original backup files
        shutil.copy2(file_path, subdirs['originals'])
        
        # Organize by type
        if '-themes.zip' in filename:
            extract_wordpress_backup(file_path, subdirs['themes'])
        elif '-plugins.zip' in filename:
            extract_wordpress_backup(file_path, subdirs['plugins'])
        elif '-uploads.zip' in filename:
            extract_wordpress_backup(file_path, subdirs['uploads'])
        elif '-db.gz' in filename or 'database' in filename.lower():
            shutil.copy2(file_path, subdirs['database'])
        elif '-others.zip' in filename:
            extract_wordpress_backup(file_path, subdirs['others'])
        else:
            # Documentation or other files
            dest_path = os.path.join(student_dir, f"{student_id}_{filename}")
            shutil.copy2(file_path, dest_path)


def extract_wordpress_backup(zip_path, extract_dir):
    """Extract WordPress backup zip file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            logger.info(f"Extracted WordPress backup: {os.path.basename(zip_path)}")
    except zipfile.BadZipFile:
        logger.warning(f"Could not extract WordPress backup (bad zip): {zip_path}")
        # Copy as-is if extraction fails
        shutil.copy2(zip_path, extract_dir)


def process_regular_files(files, student_id, output_dir, no_zip=False, keep_mac_files=False):
    """Process regular (non-WordPress) student files."""
    student_dir = os.path.join(output_dir, f"{student_id}")
    os.makedirs(student_dir, exist_ok=True)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        # Filter Mac system files unless explicitly keeping them
        if not keep_mac_files and is_mac_system_file(filename):
            logger.debug(f"Filtering Mac system file: {filename}")
            continue
        
        file_ext = get_file_extension(filename)
        
        if file_ext == 'zip' and not no_zip:
            # Extract zip files
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(student_dir)
                    logger.info(f"Extracted zip for student {student_id}: {filename}")
            except zipfile.BadZipFile:
                logger.warning(f"Could not extract zip (bad file): {file_path}")
                # Copy as-is if extraction fails
                dest_path = os.path.join(student_dir, f"{student_id}_{filename}")
                shutil.copy2(file_path, dest_path)
        else:
            # Copy regular files with student ID prefix
            dest_path = os.path.join(student_dir, f"{student_id}_{filename}")
            shutil.copy2(file_path, dest_path)
    
    # Create final zip file
    zip_path = os.path.join(output_dir, f"{student_id}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(student_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, student_dir)
                zip_ref.write(file_path, arcname)
    
    # Remove temporary directory
    shutil.rmtree(student_dir)
    logger.info(f"Created consolidated zip: {zip_path}")


def main(args) -> int:
    """Main consolidation logic."""
    folder_path = args.folder_path
    output_dir = args.output_dir
    
    if not os.path.exists(folder_path):
        logger.error(f"Input folder does not exist: {folder_path}")
        return 1
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Processing files from: {folder_path}")
    logger.info(f"Output directory: {output_dir}")
    
    # Group files by student ID
    student_files = defaultdict(list)
    unmatched_files = []
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            student_id = extract_student_id(filename)
            if student_id:
                student_files[student_id].append(file_path)
            else:
                unmatched_files.append(filename)
    
    if unmatched_files:
        logger.warning(f"Files without student ID pattern: {len(unmatched_files)}")
        for filename in unmatched_files[:5]:  # Show first 5
            logger.warning(f"  - {filename}")
        if len(unmatched_files) > 5:
            logger.warning(f"  ... and {len(unmatched_files) - 5} more")
    
    # Process each student's files
    for student_id, files in student_files.items():
        logger.info(f"Processing student {student_id}: {len(files)} files")
        
        if args.wordpress:
            # Check if any files are WordPress backups
            wordpress_files = [f for f in files if is_wordpress_backup_file(os.path.basename(f))]
            if wordpress_files:
                organize_wordpress_files(files, student_id, output_dir)
            else:
                process_regular_files(files, student_id, output_dir, args.no_zip, args.keep_mac_files)
        else:
            process_regular_files(files, student_id, output_dir, args.no_zip, args.keep_mac_files)
    
    logger.info(f"Consolidation complete! Processed {len(student_files)} students")
    logger.info(f"Output saved to: {output_dir}/")
    
    return 0