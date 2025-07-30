"""
MarkMate Default Configuration Values

Default templates and configuration values used throughout MarkMate.
"""

# Default grading prompt template
DEFAULT_GRADING_PROMPT = """
You are an expert academic grader evaluating a student submission. Please provide a detailed assessment.

ASSIGNMENT SPECIFICATION:
{assignment_spec}

GRADING RUBRIC:
{rubric}

STUDENT SUBMISSION (Student ID: {student_id}):
{content_summary}

Please provide your assessment in the following format:

MARK: [numerical mark out of total possible marks]
FEEDBACK: [detailed constructive feedback explaining the mark, highlighting strengths and areas for improvement]

Be fair, consistent, and constructive in your evaluation. Consider all aspects of the submission including technical implementation, documentation quality, and adherence to requirements.
"""

# Default file type mappings
FILE_TYPE_MAPPINGS = {
    # Document types
    ".pdf": "pdf",
    ".docx": "docx", 
    ".doc": "docx",
    ".txt": "txt",
    ".md": "md",
    ".markdown": "md",
    ".rtf": "txt",
    
    # Code types
    ".py": "py",
    ".ipynb": "ipynb",
    ".js": "js",
    ".ts": "ts",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".json": "json",
    ".xml": "xml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "cfg",
    ".conf": "conf",
    
    # Web types
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "css",
    ".sass": "css",
    ".less": "css",
    
    # Office types
    ".xlsx": "xlsx",
    ".xls": "xlsx",
    ".pptx": "pptx",
    ".ppt": "pptx",
    
    # Archive types
    ".zip": "zip",
    ".tar": "tar",
    ".gz": "gz",
    ".rar": "rar",
    ".7z": "7z",
    
    # Image types
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".gif": "image",
    ".bmp": "image",
    ".svg": "image",
    ".webp": "image",
    
    # Video types
    ".mp4": "video",
    ".avi": "video",
    ".mov": "video",
    ".wmv": "video",
    ".flv": "video",
    ".webm": "video"
}

# WordPress backup file patterns
WORDPRESS_PATTERNS = {
    "themes": ["-themes.zip", "_themes.zip"],
    "plugins": ["-plugins.zip", "_plugins.zip"],
    "uploads": ["-uploads.zip", "_uploads.zip"],
    "database": ["-db.gz", "_db.gz", "-database.sql", "_database.sql"],
    "others": ["-others.zip", "_others.zip"],
    "backup": ["backup_", "backup-", "updraft"]
}

# GitHub URL patterns for detection
GITHUB_URL_PATTERNS = [
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
    r"'https://github\.com/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+/?(?:\.git)?'"
]

# Code analysis patterns
CODE_ANALYSIS_PATTERNS = {
    "python": {
        "function": [r"def\s+\w+\s*\(", r"async\s+def\s+\w+\s*\("],
        "class": [r"class\s+\w+\s*[\(:]"],
        "import": [r"^import\s+", r"^from\s+\w+\s+import"],
        "comment": [r"^\s*#", r'^\s*"""', r"^\s*'''"],
        "docstring": [r'""".+?"""', r"'''.+?'''"]
    },
    "javascript": {
        "function": [r"function\s+\w+\s*\(", r"\w+\s*=\s*function\s*\(", r"\w+\s*=>\s*"],
        "class": [r"class\s+\w+\s*\{"],
        "import": [r"^import\s+", r"^const\s+.+\s*=\s*require\("],
        "comment": [r"^\s*//", r"/\*.*?\*/"],
        "export": [r"^export\s+", r"module\.exports\s*="]
    },
    "html": {
        "tag": [r"<\w+.*?>"],
        "comment": [r"<!--.*?-->"],
        "doctype": [r"<!DOCTYPE"],
        "script": [r"<script.*?>"],
        "style": [r"<style.*?>"]
    },
    "css": {
        "selector": [r"[\w\.-]+\s*\{"],
        "property": [r"\w+\s*:"],
        "comment": [r"/\*.*?\*/"],
        "media": [r"@media\s+"],
        "import": [r"@import\s+"]
    }
}

# AI-related keywords for plugin detection
AI_KEYWORDS = [
    "ai", "artificial", "intelligence", "gpt", "chatbot", "assistant",
    "machine learning", "ml", "neural", "deep learning", "openai",
    "claude", "anthropic", "hugging face", "tensorflow", "pytorch",
    "nlp", "natural language", "computer vision", "speech", "voice",
    "automation", "smart", "cognitive", "recommendation", "prediction"
]

# Default rubric extraction patterns
RUBRIC_PATTERNS = [
    r"(?i)rubric[:\s]*(.*?)(?=\n\n|\Z)",
    r"(?i)assessment criteria[:\s]*(.*?)(?=\n\n|\Z)",
    r"(?i)marking scheme[:\s]*(.*?)(?=\n\n|\Z)",
    r"(?i)grading[:\s]*(.*?)(?=\n\n|\Z)",
    r"(?i)evaluation[:\s]*(.*?)(?=\n\n|\Z)"
]

# Mark extraction patterns
MARK_PATTERNS = [
    r"(?i)total[:\s]*(\d+)",
    r"(?i)out of[:\s]*(\d+)",
    r"(?i)marks?[:\s]*(\d+)",
    r"(?i)points?[:\s]*(\d+)",
    r"(?i)maximum[:\s]*(\d+)",
    r"(?i)max[:\s]*(\d+)"
]

# Default encoding detection order
ENCODING_DETECTION_ORDER = [
    "utf-8",
    "utf-16",
    "utf-16-le", 
    "utf-16-be",
    "cp1252",
    "latin-1",
    "ascii",
    "cp1251",  # Cyrillic
    "cp1254",  # Turkish
    "iso-8859-1",  # Western European
    "iso-8859-2",  # Central European
    "gb2312",  # Simplified Chinese
    "big5",    # Traditional Chinese
    "shift_jis",  # Japanese
    "euc-kr"   # Korean
]

# CLI help messages
CLI_HELP = {
    "consolidate": "Consolidate and organize student submission files with intelligent filtering",
    "scan": "Scan submissions for GitHub repository URLs and create mapping files",
    "extract": "Extract and analyze content from student submissions with comprehensive multi-format support",
    "grade": "Grade student submissions using AI with multiple LLM providers"
}

# Default output templates
OUTPUT_TEMPLATES = {
    "extraction_session": {
        "timestamp": None,
        "total_students": 0,
        "wordpress_mode": False,
        "github_analysis": False,
        "submissions_folder": None
    },
    "grading_session": {
        "timestamp": None,
        "total_students": 0,
        "providers": [],
        "assignment_spec_file": None,
        "rubric_file": None,
        "source_content_file": None
    }
}