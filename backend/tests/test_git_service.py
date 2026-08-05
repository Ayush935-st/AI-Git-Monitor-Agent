from backend.services.git_service import GitService


def test_latest_commit():
    service = GitService("repositories/sample_repo")
    service.load_repository()

    assert service.get_latest_commit() is not None

    print("Branches:", service.get_branches())

    print("Latest Commit:", service.get_latest_commit().hexsha)

    print("Changed Files:", service.get_changed_files())

    print("Git Diff:\n")
    print(service.get_commit_diff()[:1000])  # Print first 1000 chars