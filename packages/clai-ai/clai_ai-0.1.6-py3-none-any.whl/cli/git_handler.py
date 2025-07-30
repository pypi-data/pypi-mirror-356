import git
from git import Repo, InvalidGitRepositoryError
from pathlib import Path
from typing import List, Dict, Optional

import os


class GitHandler:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.repo = None
        self._initialize_repo()

    def _initialize_repo(self):
        try:
            self.repo = Repo(self.repo_path)
        except InvalidGitRepositoryError:
            self.repo = None

    def get_repo_info(self) -> dict:
        if not self.repo:
            return {}
        try:
            return {
                "repo_path": str(self.repo_path),
                "repo": self.repo,
                "remote_url": self.repo.remote().url if self.repo.remotes else None,
                "branch": self.get_current_branch(),
                "has_staged": self.has_staged_changes(),
            }
        except:
            return {}

    def is_git_repo(self) -> bool:
        """Check if current directory is a Git repository"""
        return self.repo is not None

    def get_current_branch(self) -> str:
        """Get current branch name"""
        if not self.repo:
            raise Exception("Not a git repository")
        return self.repo.active_branch.name

    def has_staged_changes(self) -> bool:
        """Check if there are staged changes"""
        if not self.repo:
            raise Exception("Not a git repository")
        return len(self.repo.index.diff("HEAD")) > 0

    def get_staged_changes(self) -> List[Dict]:
        """Get list of staged changes with details"""
        if not self.repo:
            raise Exception("Not a git repository")

        changes = []
        for item in self.repo.index.diff("HEAD"):
            changes.append(
                {
                    "file": item.a_path,
                    "change_type": item.change_type,
                    "status": self._get_change_status(item.change_type),
                }
            )
        return changes

    def get_staged_diff(self) -> str:
        """Get diff of staged changes"""
        if not self.repo:
            raise Exception("Not a git repository")

        # Get staged changes diff
        staged_diff = self.repo.git.diff("--cached")
        return staged_diff

    def _get_change_status(self, change_type) -> str:
        """Convert GitPython change type to readable status"""
        status_map = {
            "A": "added",
            "D": "deleted",
            "M": "modified",
            "R": "renamed",
            "C": "copied",
            "T": "type_changed",
        }
        return status_map.get(change_type, "unknown")

    def get_recent_files(self, days: int = 7) -> List[str]:
        """Get files modified in the last N days"""
        if not self.repo:
            return []

        try:
            # Get commits from last N days
            since = f"--since='{days} days ago'"
            commits = list(self.repo.iter_commits(since))

            modified_files = set()
            for commit in commits:
                for item in commit.stats.files:
                    modified_files.add(item)

            return list(modified_files)
        except:
            return []

    def get_tracked_files(self) -> List[str]:
        """Get all Git-tracked files"""
        if not self.repo:
            return []

        try:
            tracked_files = []
            for item in self.repo.git.ls_files().split("\n"):
                if item.strip():
                    tracked_files.append(item.strip())
            return tracked_files
        except:
            return []

    def commit(self, message: str):
        """Commit staged changes with given message"""
        if not self.repo:
            raise Exception("Not a git repository")

        if not self.has_staged_changes():
            raise Exception("No staged changes to commit")

        # Commit the staged changes
        self.repo.index.commit(message)

    def push(self, remote: str = "origin", branch: Optional[str] = None):
        """Push changes to remote repository"""
        if not self.repo:
            raise Exception("Not a git repository")

        if branch is None:
            branch = self.get_current_branch()

        # Push to remote
        origin = self.repo.remote(remote)
        origin.push(branch)
