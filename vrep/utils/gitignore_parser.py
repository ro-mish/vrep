import os
import fnmatch
from pathlib import Path
from typing import List, Set

class GitignoreParser:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.ignore_patterns: Set[str] = set()
        self._load_gitignore()

    def _load_gitignore(self):
        """Load patterns from .gitignore file"""
        gitignore_path = self.repo_path / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Convert pattern to work with fnmatch
                        pattern = line.rstrip('/')  # Remove trailing slashes
                        self.ignore_patterns.add(pattern)

    def should_ignore(self, path: str) -> bool:
        """Check if a path should be ignored based on gitignore patterns"""
        # Get relative path from repo root
        try:
            rel_path = str(Path(path).relative_to(self.repo_path))
        except ValueError:
            return False

        # Check each pattern
        for pattern in self.ignore_patterns:
            # Handle directory patterns
            if pattern.endswith('/'):
                if fnmatch.fnmatch(rel_path + '/', pattern):
                    return True
            # Handle file patterns
            if fnmatch.fnmatch(rel_path, pattern):
                return True
            # Handle patterns without leading slash
            if fnmatch.fnmatch(rel_path, f"**/{pattern}"):
                return True

        return False 