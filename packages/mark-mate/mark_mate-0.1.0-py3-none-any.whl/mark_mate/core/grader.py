"""
MarkMate Core Grader

Handles AI-powered grading using multiple LLM providers.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from statistics import mean, stdev
import re

# LLM imports
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class GradingSystem:
    """Main grading system using multiple LLM providers."""
    
    def __init__(self):
        """Initialize the grading system with available LLM clients."""
        self.anthropic_client = None
        self.openai_client = None
        self.token_usage = {
            'anthropic': {'input_tokens': 0, 'output_tokens': 0},
            'openai': {'input_tokens': 0, 'output_tokens': 0}
        }
        
        # Initialize clients if API keys are available
        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.anthropic_client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def grade_submission(self, student_data: Dict[str, Any], assignment_spec: str, 
                        providers: List[str], rubric: Optional[str] = None) -> Dict[str, Any]:
        """
        Grade a single student submission using specified providers.
        
        Args:
            student_data: Extracted content and metadata for the student
            assignment_spec: Assignment specification/requirements
            providers: List of LLM providers to use
            rubric: Optional separate rubric
            
        Returns:
            Dictionary containing grading results from all providers
        """
        result = {
            "student_id": student_data.get("student_id", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "providers": {},
            "aggregate": {},
            "metadata": {
                "providers_used": providers,
                "token_usage": {},
                "errors": []
            }
        }
        
        # Extract rubric from assignment spec if not provided separately
        if not rubric:
            rubric = self._extract_rubric(assignment_spec)
        
        # Grade with each provider
        provider_results = []
        
        for provider in providers:
            try:
                if provider == "claude" and self.anthropic_client:
                    provider_result = self._grade_with_claude(student_data, assignment_spec, rubric)
                    result["providers"]["claude"] = provider_result
                    provider_results.append(provider_result)
                    
                elif provider == "openai" and self.openai_client:
                    provider_result = self._grade_with_openai(student_data, assignment_spec, rubric)
                    result["providers"]["openai"] = provider_result
                    provider_results.append(provider_result)
                    
                else:
                    error_msg = f"Provider {provider} not available or not configured"
                    result["metadata"]["errors"].append(error_msg)
                    logger.warning(error_msg)
                    
            except Exception as e:
                error_msg = f"Error grading with {provider}: {str(e)}"
                result["metadata"]["errors"].append(error_msg)
                logger.error(error_msg)
        
        # Aggregate results if multiple providers were used
        if len(provider_results) > 1:
            result["aggregate"] = self._aggregate_results(provider_results)
        elif len(provider_results) == 1:
            # Single provider - use its result as aggregate
            result["aggregate"] = provider_results[0].copy()
            result["aggregate"]["confidence"] = 0.8  # Lower confidence for single provider
        else:
            result["aggregate"] = {
                "mark": 0,
                "feedback": "No grading providers were available",
                "confidence": 0.0,
                "max_mark": self._extract_max_mark(assignment_spec)
            }
        
        # Add token usage info
        result["metadata"]["token_usage"] = self.token_usage
        
        return result
    
    def _grade_with_claude(self, student_data: Dict[str, Any], assignment_spec: str, 
                          rubric: str) -> Dict[str, Any]:
        """Grade using Claude (Anthropic)."""
        if not self.anthropic_client:
            raise ValueError("Claude client not initialized")
        
        prompt = self._build_grading_prompt(student_data, assignment_spec, rubric)
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Track token usage
            self.token_usage['anthropic']['input_tokens'] += response.usage.input_tokens
            self.token_usage['anthropic']['output_tokens'] += response.usage.output_tokens
            
            # Parse response
            response_text = response.content[0].text
            return self._parse_grading_response(response_text, assignment_spec)
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def _grade_with_openai(self, student_data: Dict[str, Any], assignment_spec: str, 
                          rubric: str) -> Dict[str, Any]:
        """Grade using OpenAI GPT."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        prompt = self._build_grading_prompt(student_data, assignment_spec, rubric)
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert academic grader. Provide detailed, fair, and constructive feedback."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Track token usage
            self.token_usage['openai']['input_tokens'] += response.usage.prompt_tokens
            self.token_usage['openai']['output_tokens'] += response.usage.completion_tokens
            
            # Parse response
            response_text = response.choices[0].message.content
            return self._parse_grading_response(response_text, assignment_spec)
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _build_grading_prompt(self, student_data: Dict[str, Any], assignment_spec: str, 
                             rubric: str) -> str:
        """Build the grading prompt for LLM providers."""
        student_id = student_data.get("student_id", "unknown")
        content = student_data.get("content", {})
        
        # Serialize content for the prompt
        content_summary = self._summarize_content(content)
        
        prompt = f"""
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
        
        return prompt
    
    def _summarize_content(self, content: Dict[str, Any]) -> str:
        """Summarize extracted content for the grading prompt."""
        summary_parts = []
        
        # Document content
        if "documents" in content:
            summary_parts.append("DOCUMENTS:")
            for doc in content["documents"]:
                summary_parts.append(f"- {doc.get('filename', 'Unknown')}: {len(doc.get('text', ''))} characters")
        
        # Code content
        if "code" in content:
            summary_parts.append("CODE FILES:")
            for code_file in content["code"]:
                summary_parts.append(f"- {code_file.get('filename', 'Unknown')}: {len(code_file.get('content', ''))} lines")
        
        # Web content
        if "web" in content:
            summary_parts.append("WEB FILES:")
            for web_file in content["web"]:
                summary_parts.append(f"- {web_file.get('filename', 'Unknown')}: {web_file.get('file_type', 'unknown')} file")
        
        # GitHub analysis
        if "github_analysis" in content:
            github = content["github_analysis"]
            summary_parts.append("GITHUB REPOSITORY:")
            summary_parts.append(f"- Commits: {github.get('total_commits', 0)}")
            summary_parts.append(f"- Development span: {github.get('development_span_days', 0)} days")
        
        # WordPress analysis
        if any(key.startswith("wordpress_") for key in content.keys()):
            summary_parts.append("WORDPRESS ANALYSIS:")
            for key, value in content.items():
                if key.startswith("wordpress_"):
                    component = key.replace("wordpress_", "")
                    summary_parts.append(f"- {component}: {len(value.get('files_found', []))} files")
        
        return "\n".join(summary_parts) if summary_parts else "No content extracted"
    
    def _extract_rubric(self, assignment_spec: str) -> str:
        """Extract rubric information from assignment specification."""
        # Look for common rubric patterns
        rubric_patterns = [
            r"(?i)rubric[:\s]*(.*?)(?=\n\n|\Z)",
            r"(?i)assessment criteria[:\s]*(.*?)(?=\n\n|\Z)",
            r"(?i)marking scheme[:\s]*(.*?)(?=\n\n|\Z)",
            r"(?i)grading[:\s]*(.*?)(?=\n\n|\Z)"
        ]
        
        for pattern in rubric_patterns:
            match = re.search(pattern, assignment_spec, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # If no specific rubric found, return the whole assignment spec
        return assignment_spec
    
    def _extract_max_mark(self, assignment_spec: str) -> int:
        """Extract maximum mark from assignment specification."""
        # Look for patterns like "Total: 100", "out of 50", "marks: 30"
        mark_patterns = [
            r"(?i)total[:\s]*(\d+)",
            r"(?i)out of[:\s]*(\d+)",
            r"(?i)marks?[:\s]*(\d+)",
            r"(?i)points?[:\s]*(\d+)"
        ]
        
        for pattern in mark_patterns:
            match = re.search(pattern, assignment_spec)
            if match:
                return int(match.group(1))
        
        # Default to 100 if no max mark found
        return 100
    
    def _parse_grading_response(self, response_text: str, assignment_spec: str) -> Dict[str, Any]:
        """Parse LLM grading response into structured format."""
        result = {
            "mark": 0,
            "feedback": "",
            "max_mark": self._extract_max_mark(assignment_spec),
            "timestamp": datetime.now().isoformat()
        }
        
        # Extract mark
        mark_match = re.search(r"MARK[:\s]*(\d+(?:\.\d+)?)", response_text, re.IGNORECASE)
        if mark_match:
            result["mark"] = float(mark_match.group(1))
        
        # Extract feedback
        feedback_match = re.search(r"FEEDBACK[:\s]*(.*?)(?=\n\n|\Z)", response_text, re.IGNORECASE | re.DOTALL)
        if feedback_match:
            result["feedback"] = feedback_match.group(1).strip()
        else:
            # If no explicit feedback section, use the whole response
            result["feedback"] = response_text.strip()
        
        return result
    
    def _aggregate_results(self, provider_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from multiple providers."""
        marks = [r["mark"] for r in provider_results if "mark" in r]
        
        if not marks:
            return {
                "mark": 0,
                "feedback": "No valid marks from providers",
                "confidence": 0.0,
                "max_mark": provider_results[0].get("max_mark", 100)
            }
        
        # Calculate aggregated mark (weighted average)
        aggregated_mark = mean(marks)
        
        # Calculate confidence based on agreement between providers
        if len(marks) > 1:
            mark_std = stdev(marks) if len(marks) > 1 else 0
            max_mark = provider_results[0].get("max_mark", 100)
            # Higher confidence when providers agree (lower standard deviation)
            confidence = max(0.5, 1.0 - (mark_std / max_mark))
        else:
            confidence = 0.8
        
        # Combine feedback
        feedback_parts = []
        for i, result in enumerate(provider_results):
            provider_name = ["Claude", "OpenAI"][i] if i < 2 else f"Provider {i+1}"
            feedback_parts.append(f"{provider_name} Assessment: {result.get('feedback', 'No feedback')}")
        
        aggregated_feedback = "\n\n".join(feedback_parts)
        
        return {
            "mark": round(aggregated_mark, 1),
            "feedback": aggregated_feedback,
            "confidence": round(confidence, 2),
            "max_mark": provider_results[0].get("max_mark", 100),
            "provider_marks": marks,
            "mark_std_dev": round(stdev(marks), 2) if len(marks) > 1 else 0.0
        }