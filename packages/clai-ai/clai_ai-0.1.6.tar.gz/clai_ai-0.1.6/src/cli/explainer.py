
from typing import Optional

from cli.git_handler import GitHandler
from cli.ai_client import AIClient






class CodeExplainer:
    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        self.git_handler = GitHandler(root_path)
        self.ai_client = AIClient()

    def generate_commit_message(self) -> str:
        """Generate AI-powered commit message for staged changes"""
        
        if not self.git_handler.is_git_repo():
            raise Exception("Not a Git repository")
        
        if not self.git_handler.has_staged_changes():
            raise Exception("No staged changes to commit")
        
        # Get git diff and staged files
        git_diff = self.git_handler.get_staged_diff()
        staged_changes = self.git_handler.get_staged_changes()
        # Generate commit message using AI
        commit_message = self.ai_client.generate_commit_message(git_diff, staged_changes)
        
        return commit_message
