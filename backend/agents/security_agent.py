from backend.tools.security_scanner import SecurityScanner


class SecurityAgent:
    """
    Agent responsible for deterministic security analysis.
    """

    def __init__(self):
        self.scanner = SecurityScanner()

    def analyze(self, state):

        result = self.scanner.scan(
            state.get("git_diff", "")
        )

        return {
    "security_analysis": result
                } 