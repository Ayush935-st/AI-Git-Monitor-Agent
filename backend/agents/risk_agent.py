class RiskAgent:
    """Agent responsible for calculating overall risk."""

    def analyze(self, state):
        code_analysis = state.get("code_analysis", {})
        security_analysis = state.get("security_analysis", {})

        risk_score = 0

        for analysis in (code_analysis, security_analysis):
            for finding in analysis.get("findings", []):
                severity = finding.get("severity", "").lower()

                if severity == "high":
                    risk_score += 5
                elif severity == "medium":
                    risk_score += 2
                elif severity == "low":
                    risk_score += 1

        risk_score = min(risk_score, 10)

        if risk_score >= 7:
            risk_level = "HIGH"
        elif risk_score >= 4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "code_analysis": {
                **code_analysis,
                "risk_level": risk_level,
            },
            "current_agent": "risk",
        }