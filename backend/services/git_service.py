from pathlib import Path
from typing import List, Optional

from git import Repo, GitCommandError

from backend.utils.logger import logger


class GitService:
    """
    Production Git Service.
    Handles all Git repository operations.
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo: Optional[Repo] = None

    def clone_repository(self, repo_url: str) -> None:
        """
        Clone a Git repository.
        """

        try:
            if self.repo_path.exists():
                logger.info("Repository already exists.")
                self.repo = Repo(self.repo_path)
                return

            logger.info(f"Cloning repository: {repo_url}")

            self.repo = Repo.clone_from(repo_url, self.repo_path)

            logger.info("Repository cloned successfully.")

        except GitCommandError as e:
            logger.exception(e)
            raise

    def load_repository(self):
        """
        Load an existing local repository.
        """

        self.repo = Repo(self.repo_path)

        logger.info("Repository loaded.")

    def pull_latest_changes(self):
        """
        Pull latest commits.
        """

        origin = self.repo.remotes.origin

        origin.pull()

        logger.info("Latest changes pulled.")

    def get_branches(self) -> List[str]:
        """
        Return all local branches.
        """

        return [branch.name for branch in self.repo.branches]

    def get_latest_commit(self):
        """
        Return latest commit object.
        """

        return self.repo.head.commit

    def get_changed_files(self):

        commit = self.get_latest_commit()

        if not commit.parents:
            return []

        previous = commit.parents[0]

        diff = previous.diff(commit)

        return [item.b_path for item in diff]

    def get_commit_diff(self):

        commit = self.get_latest_commit()

        if not commit.parents:
            return ""

        previous = commit.parents[0]

        return self.repo.git.diff(previous.hexsha, commit.hexsha)