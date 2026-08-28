from backend.tools.code_analyzer import CodeAnalyzer


class CodeAnalysisAgent:
    """
    Agent responsible for deterministic code analysis.
    """

    def __init__(self):
        self.analyzer = CodeAnalyzer()

    def analyze(self, state):

        result = self.analyzer.analyze(
            changed_files=state.get("changed_files", []),
            git_diff=state.get("git_diff", ""),
        )

        return {
    "code_analysis": result
                }