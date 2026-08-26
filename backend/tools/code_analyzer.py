from typing import Dict, Any


class CodeAnalyzer:
    """
    Deterministic code analysis tool.

    Performs static analysis on Git changes without using an LLM.
    """

    def analyze(
        self,
        changed_files: list[str],
        git_diff: str,
    ) -> Dict[str, Any]:

        findings = []

        added_lines = 0
        removed_lines = 0

        for line in git_diff.splitlines():

            if line.startswith("+++") or line.startswith("---"):
                continue

            if line.startswith("+"):
                added_lines += 1

            elif line.startswith("-"):
                removed_lines += 1

        # Large diff
        if len(git_diff) > 10000:
            findings.append({
                "type": "large_diff",
                "severity": "medium",
                "message": "Large Git diff detected."
            })

        # Large number of changed files
        if len(changed_files) > 20:
            findings.append({
                "type": "large_change_set",
                "severity": "medium",
                "message": "Large number of files changed."
            })

        # TODO / FIXME detection
        if "TODO" in git_diff or "FIXME" in git_diff:
            findings.append({
                "type": "todo_fixme",
                "severity": "low",
                "message": "TODO/FIXME marker detected in changes."
            })

        return {
            "changed_file_count": len(changed_files),
            "added_lines": added_lines,
            "removed_lines": removed_lines,
            "diff_size": len(git_diff),
            "findings": findings,
        }