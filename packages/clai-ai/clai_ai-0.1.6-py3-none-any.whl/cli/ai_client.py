from google import genai
from typing import Dict, List, Optional
from cli.config import ConfigManager
import re

class AIClient:
    """Handles communication with Gemini AI API with enhanced commit message generation"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.client = None
        self._initialize_client()
        
        # Files/extensions to exclude from diff analysis
        self.EXCLUDED_FILES = {
            'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            'package.json', 'go.sum', 'Gemfile.lock',
            '*.log', '*.min.js', '*.min.css',
            '*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg',
            '*.pdf', '*.ico', '*.woff', '*.woff2', '*.ttf',
            '*.env', '*.example', '*.sample'
        }

    def _initialize_client(self):
        """Initialize Gemini client with API key"""
        api_key = self.config_manager.get_api_key()
        if not api_key:
            raise Exception(
                "No API key configured. Run 'clay config --api-key YOUR_KEY' first."
            )
        self.client = genai.Client(api_key=api_key)

    def _should_exclude_file(self, filename: str) -> bool:
        """Check if file should be excluded from analysis"""
        return any(
            filename == pattern or 
            filename.endswith(pattern.lstrip('*')) 
            for pattern in self.EXCLUDED_FILES
        )

    def _filter_diff(self, git_diff: str, staged_files: List[Dict]) -> tuple[str, List[Dict]]:
        """Filter out irrelevant files and their diffs"""
        filtered_files = []
        filtered_diff = []
        
        # Split diff into per-file sections
        diff_sections = re.split(r'diff --git a/.+ b/.+', git_diff)
        if not diff_sections:
            return git_diff, staged_files
            
        # First section is usually empty or metadata
        diff_sections = diff_sections[1:]  
        
        for file_info, diff_section in zip(staged_files, diff_sections):
            if not self._should_exclude_file(file_info['file']):
                filtered_files.append(file_info)
                filtered_diff.append(diff_section)
        
        return '\n'.join(filtered_diff), filtered_files

    def generate_commit_message(self, git_diff: str, staged_files: List[Dict]) -> str:
        """Generate a high-quality commit message with subject and body"""
        # Filter out irrelevant files first
        filtered_diff, filtered_files = self._filter_diff(git_diff, staged_files)
        
        if not filtered_files:
            return self._generate_fallback_commit_message(staged_files)

        # Create categorized file summary
        file_summary = []
        for file_info in filtered_files:
            file_summary.append(f"- {file_info['file']} ({file_info['status']})")
        
        files_text = "\n".join(file_summary)
        
        prompt = f"""You are an expert software engineer writing excellent Git commit messages. 
Analyze the following changes and generate a professional commit message.

**Changed Files:**
{files_text}

**Code Changes:**
{filtered_diff}

**Commit Message Guidelines:**
1. Follow Conventional Commits specification (feat|fix|docs|style|refactor|test|chore|perf|build|ci|revert)
2. Structure your response with:
   - First line: Subject (max 50 chars)
   - Blank line
   - Then: Body (wrap at 72 chars, explain WHY not WHAT)
3. Focus on the impact and reasoning
4. Use imperative mood ("Add" not "Added")
5. For multiple changes, group logically

**Example Format:**
feat: add user authentication middleware

Add JWT-based authentication middleware to handle API requests.
Includes token validation and error handling for:
- Missing tokens
- Invalid signatures
- Expired tokens

**Generate the commit message now:**"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-001", contents=prompt
            )
            commit_message = response.text
            
            # Clean and validate the response
            return self._format_commit_message(commit_message, filtered_files)
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_commit_message(filtered_files)

    def _format_commit_message(self, raw_message: str, files: List[Dict]) -> str:
        """Validate and format the AI-generated commit message"""
        # Remove any markdown formatting or quotes
        clean_message = re.sub(r'^["`]|["`]$', '', raw_message.strip())
        
        # Ensure proper subject/body separation
        if '\n\n' not in clean_message:
            if len(clean_message) <= 72:
                return clean_message
            # Split long single-line messages
            parts = clean_message.split('. ')
            if len(parts) > 1:
                clean_message = f"{parts[0]}\n\n{' '.join(parts[1:])}"
            else:
                clean_message = f"{clean_message[:50]}\n\n{clean_message[50:]}"
        
        # Ensure subject line isn't too long
        subject, *body = clean_message.split('\n\n')
        if len(subject) > 50:
            subject = subject[:47] + "..."
        
        return f"{subject}\n\n{' '.join(body)}".strip()

    def _generate_fallback_commit_message(self, staged_files: List[Dict]) -> str:
        """Generate a simple but useful fallback message"""
        if not staged_files:
            return "Update files"
            
        if len(staged_files) == 1:
            file_info = staged_files[0]
            action = {
                'modified': 'Update',
                'added': 'Add',
                'deleted': 'Remove',
                'renamed': 'Rename'
            }.get(file_info['status'], 'Update')
            
            return f"{action} {file_info['file']}"
        
        # Group by change type
        changes = {}
        for file_info in staged_files:
            changes.setdefault(file_info['status'], []).append(file_info['file'])
        
        parts = []
        for status, files in changes.items():
            action = {
                'modified': 'Update',
                'added': 'Add',
                'deleted': 'Remove',
                'renamed': 'Rename'
            }.get(status, 'Update')
            
            if len(files) == 1:
                parts.append(f"{action} {files[0]}")
            else:
                parts.append(f"{action} {len(files)} {status} files")
        
        return "\n\n".join(parts)
