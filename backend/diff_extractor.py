from git import Repo
from backend.config import REPO_PATH


class DiffExtractor:
    def __init__(self):
        self.repo = Repo(REPO_PATH)

    def extract_latest_commit(self):
        """
        Extract details of the latest commit.
        """

        commit = self.repo.head.commit

        commit_data = {
            "commit_id": commit.hexsha,
            "author": commit.author.name,
            "email": commit.author.email,
            "message": commit.message.strip(),
            "files": [],
            "diff": ""
        }

        # First commit has no parent
        if not commit.parents:
            return commit_data

        parent = commit.parents[0]

        # Generate diff between parent and current commit
        diff_index = parent.diff(commit, create_patch=True)

        for change in diff_index:

            filename = change.b_path if change.b_path else change.a_path

            commit_data["files"].append(filename)

            if change.diff:
                commit_data["diff"] += (
                    f"\n\n===== {filename} =====\n"
                    + change.diff.decode("utf-8", errors="ignore")
                )

        return commit_data