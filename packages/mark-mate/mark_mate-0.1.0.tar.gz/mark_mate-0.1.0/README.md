# MarkMate
**Your AI Teaching Assistant for Assignments and Assessment**

[![PyPI version](https://badge.fury.io/py/mark-mate.svg)](https://badge.fury.io/py/mark-mate)
[![Python versions](https://img.shields.io/pypi/pyversions/mark-mate.svg)](https://pypi.org/project/mark-mate/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive system for processing, consolidating, and grading student submissions with support for multiple content types, GitHub repository analysis, WordPress assignments, and AI-powered assessment using Claude 3.5 Sonnet and GPT-4o.

## 🚀 Quick Start

### Installation

```bash
pip install mark-mate
```

### Basic Usage

```bash
# Consolidate submissions
mark-mate consolidate raw_submissions/

# Scan for GitHub URLs
mark-mate scan processed_submissions/ --output github_urls.txt

# Extract content with analysis
mark-mate extract processed_submissions/ --github-urls github_urls.txt --output extracted.json

# Grade submissions
mark-mate grade extracted.json assignment_spec.txt --output results.json
```

### API Keys Setup

```bash
export ANTHROPIC_API_KEY="your_anthropic_key"
export OPENAI_API_KEY="your_openai_key"
```

## 📋 System Overview

MarkMate consists of four main components accessible via CLI or Python API:

### 1. **Consolidate** - File organization and filtering
- Groups files by student ID with intelligent pattern matching
- Extracts zip archives with conflict resolution
- Filters Mac system files (.DS_Store, resource forks, __MACOSX)
- WordPress mode for UpdraftPlus backup organization

### 2. **Scan** - GitHub repository detection
- Comprehensive URL detection with regex patterns
- Scans text files within zip archives
- Enhanced encoding support for international students
- Creates editable student_id:repo_url mapping files

### 3. **Extract** - Multi-format content processing
- **Document Processing**: PDF, DOCX, TXT, MD, Jupyter notebooks
- **Code Analysis**: Python, HTML, CSS, JavaScript, React/TypeScript
- **GitHub Analysis**: Commit history, development patterns, repository quality
- **WordPress Processing**: Themes, plugins, database, AI detection
- **Enhanced Encoding**: 18+ encodings for international students

### 4. **Grade** - AI-powered assessment
- **Dual-LLM Grading**: Claude 3.5 Sonnet + GPT-4o
- **Automatic Rubric Extraction**: From assignment specifications
- **Confidence Scoring**: Based on provider agreement
- **Comprehensive Feedback**: Incorporating all analysis types

## 🌟 Key Features

- **Multi-Format Support**: PDF, DOCX, TXT, MD, Jupyter notebooks, Python code, web files (HTML/CSS/JS), React/TypeScript projects
- **GitHub Repository Analysis**: Commit history, development patterns, repository quality assessment
- **Enhanced Encoding Support**: Optimized for ESL students with automatic encoding detection (UTF-8, UTF-16, CP1252, Latin-1, and more)
- **WordPress Assignment Processing**: Complete backup analysis with theme, plugin, and database evaluation
- **Dual-LLM Grading**: Claude 3.5 Sonnet + GPT-4o with confidence scoring and mark aggregation
- **Mac System File Filtering**: Automatic removal of .DS_Store, resource forks, and __MACOSX directories

## 🖥️ CLI Interface

### Consolidate Command
```bash
mark-mate consolidate [OPTIONS] FOLDER_PATH

Options:
  --no-zip              Discard zip files instead of extracting
  --wordpress           Enable WordPress-specific processing
  --keep-mac-files      Preserve Mac system files
  --output-dir TEXT     Output directory (default: processed_submissions)
```

### Scan Command
```bash
mark-mate scan [OPTIONS] SUBMISSIONS_FOLDER

Options:
  --output TEXT         Output file for URL mappings (default: github_urls.txt)
  --encoding TEXT       Text encoding (default: utf-8)
```

### Extract Command
```bash
mark-mate extract [OPTIONS] SUBMISSIONS_FOLDER

Options:
  --output TEXT         Output JSON file (default: extracted_content.json)
  --wordpress           Enable WordPress processing
  --github-urls TEXT    GitHub URL mapping file
  --dry-run             Preview processing without extraction
  --max-students INT    Limit number of students (for testing)
```

### Grade Command
```bash
mark-mate grade [OPTIONS] EXTRACTED_CONTENT ASSIGNMENT_SPEC

Options:
  --output TEXT         Output JSON file (default: grading_results.json)
  --rubric TEXT         Separate rubric file
  --max-students INT    Limit number of students
  --dry-run             Preview grading without API calls
  --providers TEXT      LLM providers: claude, openai, both (default: both)
```

## 🐍 Python API

### Library Usage

```python
from mark_mate import GradingSystem, AssignmentProcessor, ContentAnalyzer

# Process submissions
processor = AssignmentProcessor()
result = processor.process_submission(
    "/path/to/submission", 
    "123", 
    wordpress=True,
    github_url="https://github.com/user/repo"
)

# Grade with AI
grader = GradingSystem()
grade_result = grader.grade_submission(
    student_data=result,
    assignment_spec="Assignment requirements...",
    providers=["claude", "openai"]
)

# Analyze content
analyzer = ContentAnalyzer()
summary = analyzer.generate_submission_summary(
    result["content"], 
    result["metadata"]
)
```

## 🔄 Complete Workflows

### Programming Assignment with GitHub
```bash
# 1. Consolidate submissions
mark-mate consolidate programming_submissions/

# 2. Scan for GitHub URLs
mark-mate scan processed_submissions/ --output github_urls.txt

# 3. Extract with comprehensive analysis
mark-mate extract processed_submissions/ --github-urls github_urls.txt

# 4. Grade with repository analysis
mark-mate grade extracted_content.json programming_assignment.txt
```

### WordPress Assignment
```bash
# 1. Consolidate WordPress backups
mark-mate consolidate wordpress_submissions/ --wordpress

# 2. Extract WordPress content
mark-mate extract processed_submissions/ --wordpress

# 3. Grade with WordPress criteria
mark-mate grade extracted_content.json wordpress_assignment.txt
```

### International Student Support
```bash
# Enhanced encoding detection handles international submissions automatically
mark-mate consolidate international_submissions/
mark-mate extract processed_submissions/  # Auto-detects 18+ encodings
mark-mate grade extracted_content.json assignment.txt
```

## 🌍 Enhanced Support for International Students

### Advanced Encoding Detection
Comprehensive support for ESL (English as a Second Language) students:

**Supported Encodings:**
- **UTF-16**: Windows systems with non-English locales
- **CP1252**: Windows-1252 (Western European, legacy systems)
- **Latin-1**: ISO-8859-1 (European systems, older editors)
- **Regional**: Cyrillic (CP1251), Turkish (CP1254), Chinese (GB2312, Big5), Japanese (Shift_JIS), Korean (EUC-KR)

**Intelligent Fallback Strategy:**
1. Try optimal encoding based on content type
2. Graceful fallback with error handling
3. Preserve international characters and symbols
4. Detailed logging of encoding attempts

## 🐙 GitHub Repository Analysis

### Comprehensive Development Assessment
Analyzes student GitHub repositories to evaluate development processes:

**Repository Analysis Features:**
- **Commit History**: Development timeline, frequency patterns, consistency
- **Message Quality**: Scoring based on descriptiveness and professionalism
- **Development Patterns**: Steady development vs. last-minute work detection
- **Collaboration**: Multi-author analysis, teamwork evaluation
- **Repository Quality**: README, documentation, directory structure
- **Code Organization**: File management, naming conventions, best practices

**Analysis Output Example:**
```json
{
  "github_metrics": {
    "total_commits": 15,
    "development_span_days": 14,
    "commit_message_quality": {
      "score": 89,
      "quality_level": "excellent"
    },
    "consistency_score": 0.86,
    "collaboration_level": "collaborative"
  }
}
```

## 🎯 WordPress Assignment Support

### Static Assessment Capabilities
Assess WordPress assignments without requiring site restoration:

**Technical Implementation:**
- Theme analysis and customization assessment
- Plugin inventory and functionality review
- Database content extraction and analysis
- Security configuration evaluation

**Content Quality Assessment:**
- Blog post count and word count analysis
- Media usage and organization
- User account configuration
- Comment analysis

**AI Integration Detection:**
- Automatic detection of AI-related plugins
- AI keyword analysis in plugin descriptions
- Assessment of AI integration documentation

## 📊 Output and Results

### Extraction Output
```json
{
  "extraction_session": {
    "timestamp": "2025-06-19T10:30:00",
    "total_students": 24,
    "wordpress_mode": true,
    "github_analysis": true
  },
  "students": {
    "123": {
      "content": {...},
      "metadata": {...}
    }
  }
}
```

### Grading Output
```json
{
  "grading_session": {
    "timestamp": "2025-06-19T11:00:00",
    "total_students": 24,
    "providers": ["claude", "openai"]
  },
  "results": {
    "123": {
      "aggregate": {
        "mark": 85,
        "feedback": "Comprehensive feedback...",
        "confidence": 0.95,
        "max_mark": 100
      },
      "providers": {
        "claude": {"mark": 83, "feedback": "..."},
        "openai": {"mark": 87, "feedback": "..."}
      }
    }
  }
}
```

## 🛠️ Development

### Setup Development Environment
```bash
git clone https://github.com/markmate-ai/mark-mate.git
cd mark-mate
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
black src/
flake8 src/
mypy src/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Adding New Features
1. **Content Extractors**: Follow the `BaseExtractor` pattern in `src/mark_mate/extractors/`
2. **Analysis Capabilities**: Extend existing analyzers or create new ones
3. **LLM Providers**: Add new providers in `src/mark_mate/core/grader.py`
4. **CLI Commands**: Add new commands in `src/mark_mate/cli/`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Documentation**: [https://mark-mate.readthedocs.io](https://mark-mate.readthedocs.io)
- **GitHub**: [https://github.com/markmate-ai/mark-mate](https://github.com/markmate-ai/mark-mate)
- **PyPI**: [https://pypi.org/project/mark-mate/](https://pypi.org/project/mark-mate/)
- **Issues**: [https://github.com/markmate-ai/mark-mate/issues](https://github.com/markmate-ai/mark-mate/issues)

## 🙏 Acknowledgments

MarkMate is designed for educational assessment purposes. Please ensure compliance with your institution's policies regarding automated grading and student data processing.

---

**MarkMate: Your AI Teaching Assistant for Assignments and Assessment**