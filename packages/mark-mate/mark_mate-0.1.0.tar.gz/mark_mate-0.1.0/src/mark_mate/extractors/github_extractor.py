"""
GitHub repository extractor for analyzing student GitHub repositories.

This module handles extraction and analysis of GitHub repositories,
providing detailed repository quality assessment, commit analysis, and
development pattern evaluation.
"""

import logging
import os
import re
import tempfile
import shutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict
from .base_extractor import BaseExtractor

logger = logging.getLogger(__name__)


class GitHubExtractor(BaseExtractor):
    """Extractor for GitHub repository analysis."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.extractor_name = "github_extractor"
        self.supported_protocols = ['https', 'http', 'git']
        
        # Check if git is available
        self.git_available = self._check_git_availability()
        if not self.git_available:
            logger.warning("Git is not available - GitHub analysis will be limited")
    
    def _check_git_availability(self) -> bool:
        """Check if git command is available."""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def can_extract(self, repo_url: str) -> bool:
        """Check if this extractor can handle the given repository URL."""
        if not self.git_available:
            return False
        
        # Basic GitHub URL validation
        github_patterns = [
            r'https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+',
            r'http://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+',
            r'git@github\.com:[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+\.git'
        ]
        
        return any(re.match(pattern, repo_url) for pattern in github_patterns)
    
    def extract_content(self, repo_url: str) -> Dict[str, Any]:
        """Extract content and perform analysis on GitHub repository."""
        if not self.can_extract(repo_url):
            return self.create_error_result(repo_url, ValueError("Invalid GitHub repository URL"))
        
        if not self.git_available:
            return self.create_error_result(repo_url, RuntimeError("Git is not available"))
        
        try:
            # Analyze repository
            analysis_result = self._analyze_repository(repo_url)
            
            if analysis_result['success']:
                # Create comprehensive content text
                content_text = self._create_content_text(repo_url, analysis_result['analysis'])
                
                return self.create_success_result(
                    repo_url, 
                    content_text, 
                    analysis_result['analysis']
                )
            else:
                return self.create_error_result(
                    repo_url, 
                    Exception(analysis_result.get('error', 'Unknown error'))
                )
        
        except Exception as e:
            logger.error(f"GitHub extraction failed for {repo_url}: {e}")
            return self.create_error_result(repo_url, e)
    
    def _analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Analyze GitHub repository."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                repo_path = os.path.join(temp_dir, 'repo')
                
                # Clone repository (shallow clone for efficiency)
                clone_success = self._clone_repository(repo_url, repo_path)
                
                if not clone_success:
                    return {
                        'success': False,
                        'error': 'Failed to clone repository'
                    }
                
                # Perform various analyses
                analysis = {
                    'repository_url': repo_url,
                    'clone_success': True,
                    'commit_analysis': self._analyze_commits(repo_path),
                    'repository_quality': self._analyze_repository_quality(repo_path),
                    'development_patterns': self._analyze_development_patterns(repo_path),
                    'file_analysis': self._analyze_files(repo_path),
                    'branch_analysis': self._analyze_branches(repo_path)
                }
                
                return {
                    'success': True,
                    'analysis': analysis
                }
        
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _clone_repository(self, repo_url: str, clone_path: str) -> bool:
        """Clone repository with shallow clone for efficiency."""
        try:
            # Use shallow clone with depth 50 to get recent history
            cmd = [
                'git', 'clone', 
                '--depth', '50',  # Get last 50 commits
                '--single-branch',  # Only default branch
                repo_url, 
                clone_path
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                logger.info(f"Successfully cloned repository: {repo_url}")
                return True
            else:
                logger.error(f"Git clone failed: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error(f"Repository clone timed out: {repo_url}")
            return False
        except Exception as e:
            logger.error(f"Clone error: {e}")
            return False
    
    def _analyze_commits(self, repo_path: str) -> Dict[str, Any]:
        """Analyze commit history and patterns."""
        try:
            # Get commit information
            cmd = [
                'git', '-C', repo_path, 'log',
                '--pretty=format:%H|%an|%ae|%ad|%s',
                '--date=iso'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return {'error': 'Failed to get commit history'}
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|', 4)
                    if len(parts) == 5:
                        commits.append({
                            'hash': parts[0],
                            'author_name': parts[1],
                            'author_email': parts[2],
                            'date': parts[3],
                            'message': parts[4]
                        })
            
            if not commits:
                return {'error': 'No commits found'}
            
            # Analyze commit patterns
            return self._analyze_commit_patterns(commits)
        
        except Exception as e:
            logger.error(f"Commit analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_commit_patterns(self, commits: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in commit history."""
        if not commits:
            return {'error': 'No commits to analyze'}
        
        # Parse commit dates
        commit_dates = []
        for commit in commits:
            try:
                # Parse ISO date format
                date_str = commit['date'].split(' ')[0]  # Get date part only
                date_obj = datetime.fromisoformat(date_str)
                commit_dates.append(date_obj)
            except Exception as e:
                logger.warning(f"Could not parse date: {commit['date']}")
        
        if not commit_dates:
            return {'error': 'Could not parse commit dates'}
        
        # Sort dates
        commit_dates.sort()
        
        # Calculate metrics
        first_commit = commit_dates[0]
        last_commit = commit_dates[-1]
        total_commits = len(commits)
        development_span = (last_commit - first_commit).days
        
        # Commit frequency analysis
        if development_span > 0:
            commits_per_day = total_commits / development_span
        else:
            commits_per_day = total_commits  # All commits in one day
        
        # Analyze commit timing patterns
        commit_hours = []
        for commit in commits:
            try:
                time_part = commit['date'].split(' ')[1]
                hour = int(time_part.split(':')[0])
                commit_hours.append(hour)
            except:
                pass
        
        # Analyze commit message quality
        message_quality = self._analyze_commit_message_quality(commits)
        
        # Detect development patterns
        consistency_score = self._calculate_consistency_score(commit_dates)
        
        return {
            'total_commits': total_commits,
            'first_commit': first_commit.isoformat(),
            'last_commit': last_commit.isoformat(),
            'development_span_days': development_span,
            'commits_per_day': round(commits_per_day, 2),
            'commit_message_quality': message_quality,
            'consistency_score': consistency_score,
            'peak_commit_hours': self._find_peak_hours(commit_hours),
            'authors': self._analyze_authors(commits)
        }
    
    def _analyze_commit_message_quality(self, commits: List[Dict]) -> Dict[str, Any]:
        """Analyze quality of commit messages."""
        messages = [commit['message'] for commit in commits]
        
        if not messages:
            return {'score': 0, 'analysis': 'No commit messages'}
        
        # Quality metrics
        total_messages = len(messages)
        
        # Length analysis
        lengths = [len(msg) for msg in messages]
        avg_length = sum(lengths) / len(lengths)
        
        # Quality indicators
        descriptive_count = sum(1 for msg in messages if len(msg) >= 10)
        capitalized_count = sum(1 for msg in messages if msg and msg[0].isupper())
        
        # Common poor practices
        generic_patterns = [
            r'^(update|fix|change|modify|add)$',
            r'^(wip|work in progress|temp|temporary)$',
            r'^(asdf|test|testing|\.\.\.)$',
            r'^[0-9]+$'  # Just numbers
        ]
        
        poor_quality_count = 0
        for msg in messages:
            if any(re.match(pattern, msg.lower().strip()) for pattern in generic_patterns):
                poor_quality_count += 1
        
        # Calculate score (0-100)
        descriptive_ratio = descriptive_count / total_messages
        capitalized_ratio = capitalized_count / total_messages
        poor_quality_ratio = poor_quality_count / total_messages
        
        score = int(100 * (
            descriptive_ratio * 0.4 + 
            capitalized_ratio * 0.3 + 
            (1 - poor_quality_ratio) * 0.3
        ))
        
        # Quality assessment
        if score >= 80:
            quality_level = 'excellent'
        elif score >= 60:
            quality_level = 'good'
        elif score >= 40:
            quality_level = 'fair'
        else:
            quality_level = 'poor'
        
        return {
            'score': score,
            'quality_level': quality_level,
            'average_length': round(avg_length, 1),
            'descriptive_ratio': round(descriptive_ratio, 2),
            'poor_quality_ratio': round(poor_quality_ratio, 2),
            'total_messages': total_messages
        }
    
    def _calculate_consistency_score(self, commit_dates: List[datetime]) -> float:
        """Calculate development consistency score (0-1)."""
        if len(commit_dates) < 2:
            return 1.0
        
        # Calculate gaps between commits
        gaps = []
        for i in range(1, len(commit_dates)):
            gap = (commit_dates[i] - commit_dates[i-1]).days
            gaps.append(gap)
        
        if not gaps:
            return 1.0
        
        # Lower variance in gaps = higher consistency
        avg_gap = sum(gaps) / len(gaps)
        if avg_gap == 0:
            return 1.0
        
        variance = sum((gap - avg_gap) ** 2 for gap in gaps) / len(gaps)
        std_dev = variance ** 0.5
        
        # Normalize to 0-1 scale (lower coefficient of variation = higher consistency)
        coefficient_of_variation = std_dev / avg_gap if avg_gap > 0 else 0
        consistency = max(0, 1 - min(1, coefficient_of_variation))
        
        return round(consistency, 2)
    
    def _find_peak_hours(self, commit_hours: List[int]) -> List[int]:
        """Find the most common hours for commits."""
        if not commit_hours:
            return []
        
        hour_counts = defaultdict(int)
        for hour in commit_hours:
            hour_counts[hour] += 1
        
        if not hour_counts:
            return []
        
        max_count = max(hour_counts.values())
        peak_hours = [hour for hour, count in hour_counts.items() if count == max_count]
        
        return sorted(peak_hours)
    
    def _analyze_authors(self, commits: List[Dict]) -> Dict[str, Any]:
        """Analyze commit authors."""
        authors = defaultdict(int)
        emails = set()
        
        for commit in commits:
            authors[commit['author_name']] += 1
            emails.add(commit['author_email'])
        
        return {
            'unique_authors': len(authors),
            'unique_emails': len(emails),
            'primary_author': max(authors.keys(), key=authors.get) if authors else None,
            'collaboration_level': 'solo' if len(authors) == 1 else 'collaborative'
        }
    
    def _analyze_repository_quality(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository structure and quality indicators."""
        try:
            quality_metrics = {
                'has_readme': False,
                'has_license': False,
                'has_gitignore': False,
                'directory_structure': 'unorganized',
                'documentation_quality': 'minimal'
            }
            
            # Check for important files
            for root, dirs, files in os.walk(repo_path):
                # Skip .git directory
                if '.git' in dirs:
                    dirs.remove('.git')
                
                for file in files:
                    filename_lower = file.lower()
                    
                    if filename_lower.startswith('readme'):
                        quality_metrics['has_readme'] = True
                    elif filename_lower.startswith('license'):
                        quality_metrics['has_license'] = True
                    elif filename_lower == '.gitignore':
                        quality_metrics['has_gitignore'] = True
            
            # Analyze directory structure
            quality_metrics['directory_structure'] = self._assess_directory_structure(repo_path)
            
            # Assess documentation quality
            quality_metrics['documentation_quality'] = self._assess_documentation_quality(repo_path)
            
            return quality_metrics
        
        except Exception as e:
            logger.error(f"Repository quality analysis failed: {e}")
            return {'error': str(e)}
    
    def _assess_directory_structure(self, repo_path: str) -> str:
        """Assess the organization of the repository directory structure."""
        try:
            # Common good practices
            good_indicators = 0
            total_checks = 0
            
            # Check for organized structure
            common_dirs = {'src', 'lib', 'docs', 'test', 'tests', 'examples', 'assets', 'public', 'static'}
            
            dirs_found = set()
            for root, dirs, files in os.walk(repo_path):
                if root == repo_path:  # Only check top level
                    dirs_found.update(d.lower() for d in dirs if not d.startswith('.'))
            
            # Points for having organized directories
            if dirs_found & common_dirs:
                good_indicators += 1
            total_checks += 1
            
            # Points for not having everything in root
            if len(dirs_found) > 0:
                good_indicators += 1
            total_checks += 1
            
            # Assessment
            if total_checks == 0:
                return 'minimal'
            
            organization_ratio = good_indicators / total_checks
            
            if organization_ratio >= 0.8:
                return 'well_organized'
            elif organization_ratio >= 0.5:
                return 'organized'
            else:
                return 'unorganized'
        
        except Exception as e:
            logger.error(f"Directory structure assessment failed: {e}")
            return 'unknown'
    
    def _assess_documentation_quality(self, repo_path: str) -> str:
        """Assess the quality of repository documentation."""
        try:
            readme_content = ""
            
            # Find and read README
            for root, dirs, files in os.walk(repo_path):
                if root == repo_path:  # Only check root
                    for file in files:
                        if file.lower().startswith('readme'):
                            readme_path = os.path.join(root, file)
                            try:
                                with open(readme_path, 'r', encoding='utf-8') as f:
                                    readme_content = f.read()
                                break
                            except:
                                try:
                                    with open(readme_path, 'r', encoding='latin-1') as f:
                                        readme_content = f.read()
                                    break
                                except:
                                    pass
            
            if not readme_content:
                return 'minimal'
            
            # Analyze README quality
            lines = readme_content.split('\n')
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            
            quality_score = 0
            
            # Length check
            if len(non_empty_lines) >= 10:
                quality_score += 1
            
            # Structure check (headers)
            has_headers = any(line.startswith('#') for line in non_empty_lines)
            if has_headers:
                quality_score += 1
            
            # Content quality indicators
            content_lower = readme_content.lower()
            quality_keywords = ['installation', 'usage', 'example', 'description', 'how to', 'getting started']
            keyword_matches = sum(1 for keyword in quality_keywords if keyword in content_lower)
            
            if keyword_matches >= 2:
                quality_score += 1
            
            # Assessment
            if quality_score >= 3:
                return 'comprehensive'
            elif quality_score >= 2:
                return 'good'
            elif quality_score >= 1:
                return 'basic'
            else:
                return 'minimal'
        
        except Exception as e:
            logger.error(f"Documentation quality assessment failed: {e}")
            return 'unknown'
    
    def _analyze_development_patterns(self, repo_path: str) -> Dict[str, Any]:
        """Analyze development patterns and behaviors."""
        try:
            # Get file change statistics
            cmd = ['git', '-C', repo_path, 'diff', '--stat', 'HEAD~1', 'HEAD']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            patterns = {
                'last_commit_changes': 'minimal',
                'development_activity': 'steady'
            }
            
            if result.returncode == 0 and result.stdout:
                # Parse diff stats
                lines = result.stdout.strip().split('\n')
                if lines:
                    last_line = lines[-1]
                    if 'files changed' in last_line:
                        # Extract numbers
                        import re
                        numbers = re.findall(r'\d+', last_line)
                        if numbers:
                            files_changed = int(numbers[0])
                            if files_changed > 10:
                                patterns['last_commit_changes'] = 'extensive'
                            elif files_changed > 3:
                                patterns['last_commit_changes'] = 'moderate'
                            else:
                                patterns['last_commit_changes'] = 'minimal'
            
            return patterns
        
        except Exception as e:
            logger.error(f"Development pattern analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_files(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository files and content."""
        try:
            file_stats = {
                'total_files': 0,
                'code_files': 0,
                'documentation_files': 0,
                'config_files': 0,
                'file_types': defaultdict(int)
            }
            
            code_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs', '.swift', '.kt'}
            doc_extensions = {'.md', '.txt', '.rst', '.pdf', '.doc', '.docx'}
            config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'}
            
            for root, dirs, files in os.walk(repo_path):
                # Skip .git directory
                if '.git' in dirs:
                    dirs.remove('.git')
                
                for file in files:
                    file_stats['total_files'] += 1
                    
                    ext = os.path.splitext(file)[1].lower()
                    file_stats['file_types'][ext] += 1
                    
                    if ext in code_extensions:
                        file_stats['code_files'] += 1
                    elif ext in doc_extensions:
                        file_stats['documentation_files'] += 1
                    elif ext in config_extensions:
                        file_stats['config_files'] += 1
            
            # Convert defaultdict to regular dict for JSON serialization
            file_stats['file_types'] = dict(file_stats['file_types'])
            
            return file_stats
        
        except Exception as e:
            logger.error(f"File analysis failed: {e}")
            return {'error': str(e)}
    
    def _analyze_branches(self, repo_path: str) -> Dict[str, Any]:
        """Analyze repository branching structure."""
        try:
            # Get branch information
            cmd = ['git', '-C', repo_path, 'branch', '-a']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            branch_info = {
                'total_branches': 0,
                'current_branch': 'unknown',
                'branching_strategy': 'simple'
            }
            
            if result.returncode == 0:
                branches = []
                current_branch = None
                
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line:
                        if line.startswith('* '):
                            current_branch = line[2:]
                            branches.append(current_branch)
                        elif not line.startswith('remotes/'):
                            branches.append(line)
                
                branch_info['total_branches'] = len(branches)
                branch_info['current_branch'] = current_branch or 'unknown'
                
                # Assess branching strategy
                if len(branches) > 3:
                    branch_info['branching_strategy'] = 'complex'
                elif len(branches) > 1:
                    branch_info['branching_strategy'] = 'moderate'
                else:
                    branch_info['branching_strategy'] = 'simple'
            
            return branch_info
        
        except Exception as e:
            logger.error(f"Branch analysis failed: {e}")
            return {'error': str(e)}
    
    def _create_content_text(self, repo_url: str, analysis: Dict[str, Any]) -> str:
        """Create comprehensive content text for GitHub repository analysis."""
        content_parts = [
            f"GITHUB REPOSITORY ANALYSIS",
            f"Repository URL: {repo_url}",
            "",
            "COMMIT ANALYSIS:"
        ]
        
        commit_analysis = analysis.get('commit_analysis', {})
        if 'error' not in commit_analysis:
            content_parts.extend([
                f"Total commits: {commit_analysis.get('total_commits', 0)}",
                f"Development span: {commit_analysis.get('development_span_days', 0)} days",
                f"Commits per day: {commit_analysis.get('commits_per_day', 0)}",
                f"First commit: {commit_analysis.get('first_commit', 'Unknown')}",
                f"Last commit: {commit_analysis.get('last_commit', 'Unknown')}",
                ""
            ])
            
            # Commit message quality
            msg_quality = commit_analysis.get('commit_message_quality', {})
            if msg_quality:
                content_parts.extend([
                    "COMMIT MESSAGE QUALITY:",
                    f"Quality level: {msg_quality.get('quality_level', 'unknown')}",
                    f"Quality score: {msg_quality.get('score', 0)}/100",
                    f"Average message length: {msg_quality.get('average_length', 0)} characters",
                    ""
                ])
        
        # Repository quality
        repo_quality = analysis.get('repository_quality', {})
        if 'error' not in repo_quality:
            content_parts.extend([
                "REPOSITORY QUALITY:",
                f"Has README: {repo_quality.get('has_readme', False)}",
                f"Has LICENSE: {repo_quality.get('has_license', False)}",
                f"Has .gitignore: {repo_quality.get('has_gitignore', False)}",
                f"Directory structure: {repo_quality.get('directory_structure', 'unknown')}",
                f"Documentation quality: {repo_quality.get('documentation_quality', 'unknown')}",
                ""
            ])
        
        # File analysis
        file_analysis = analysis.get('file_analysis', {})
        if 'error' not in file_analysis:
            content_parts.extend([
                "FILE ANALYSIS:",
                f"Total files: {file_analysis.get('total_files', 0)}",
                f"Code files: {file_analysis.get('code_files', 0)}",
                f"Documentation files: {file_analysis.get('documentation_files', 0)}",
                f"Configuration files: {file_analysis.get('config_files', 0)}",
                ""
            ])
        
        return "\n".join(content_parts)