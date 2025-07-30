from google import genai
from typing import Dict, List, Optional
from cli.config import ConfigManager


class AIClient:
    """Handles communication with Gemini AI API"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.client = None
        self._initialize_client()
      

    def _initialize_client(self):
        """Initialize Gemini client with API key"""
        api_key = self.config_manager.get_api_key()
        if not api_key:
            raise Exception(
                "No API key configured. Run 'clay config --api-key YOUR_KEY' first."
            )

        self.client = genai.Client(api_key=api_key)

    def generate_commit_message(self, git_diff: str, staged_files: List[Dict]) -> str:
        """Generate a meaningful commit message from git diff"""

        # Create file summary
        file_summary = []
        for file_info in staged_files:
            file_summary.append(f"- {file_info['file']} ({file_info['status']})")

        files_text = "\n".join(file_summary)

        prompt = f"""You are a senior developer helping to write meaningful Git commit messages.

STAGED FILES:
{files_text}

GIT DIFF:
{git_diff}

Please generate a concise, meaningful commit message following these guidelines:
1. Use conventional commit format if appropriate (feat:, fix:, docs:, style:, refactor:, test:, chore:)
2. Keep it under 50 characters for the title
3. Be specific about what changed, not just "update files"
4. Focus on the WHY and WHAT, not the HOW
5. Use imperative mood (e.g., "Add feature" not "Added feature")

Examples of good commit messages:
- "feat: add user authentication system"
- "fix: resolve memory leak in data processing"
- "docs: update API documentation for v2"
- "refactor: simplify database connection logic"

Return ONLY the commit message, nothing else."""

        print(prompt)
        try:
            print("ETHERE")
            if not self.client:
                return ""  # FIXME:

            response = self.client.models.generate_content(
                model="gemini-2.0-flash-001", contents=prompt
            )

            commit_message = response.text

            # Clean up the response (remove quotes, extra whitespace)
            commit_message = commit_message
            print(commit_message)
            print("AI_CLIENT::COMMIT_MSG")
            # Fallback if response is too long or empty
            if not commit_message or len(commit_message) > 1172:
                return self._generate_fallback_commit_message(staged_files)

            return commit_message

        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_commit_message(staged_files)

    def _generate_fallback_commit_message(self, staged_files: List[Dict]) -> str:
        """Generate a simple fallback commit message"""
        if len(staged_files) == 1:
            file_info = staged_files[0]
            action = (
                "Update"
                if file_info["status"] == "modified"
                else file_info["status"].title()
            )
            return f"{action} {file_info['file']}"
        else:
            return f"Update {len(staged_files)} files"
