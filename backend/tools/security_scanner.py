import re
from typing import Dict, Any


class SecurityScanner:
    """
    Deterministic security scanner for Git diffs.

    Detects common hard-coded secrets and sensitive
    credential patterns without using an LLM.
    """

    PATTERNS = {
        "password": r"password\s*=\s*['\"]?[^'\"]+['\"]?",
        "api_key": r"api[_-]?key\s*=\s*['\"]?[^'\"]+['\"]?",
        "secret": r"secret\s*=\s*['\"]?[^'\"]+['\"]?",
        "token": r"token\s*=\s*['\"]?[^'\"]+['\"]?",
        "private_key": r"-----BEGIN .*PRIVATE KEY-----",
    }

    def scan(self, git_diff: str) -> Dict[str, Any]:
        """
        Scan Git diff for potential security issues.
        """

        findings = []

        for name, pattern in self.PATTERNS.items():

            matches = re.findall(
                pattern,
                git_diff,
                flags=re.IGNORECASE,
            )

            if matches:
                findings.append({
                    "type": name,
                    "severity": "high",
                    "count": len(matches),
                    "message": f"Potential {name} detected.",
                })

        return {
            "findings": findings,
            "finding_count": len(findings),
        }