from backend.services.llm_services import LLMService
from backend.utils.logger import logger


class ReviewAgent:
    """
    AI Agent responsible for generating an engineering assessment
    from Git changes and deterministic analysis results.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def build_prompt(
        self,
        repository: str,
        commit: str,
        changed_files: list[str],
        git_diff: str,
        code_analysis: dict,
        security_analysis: dict,
        risk_score: int,
    ) -> str:

        return f"""
You are an experienced Senior Software Engineer performing an
automated Git code review.

Your task is to independently assess the change and provide a
practical engineering opinion.

Do NOT simply repeat the supplied analysis.
Use the evidence below, interpret it, and explain WHY the change
is safe, risky, or requires review.

Repository:
{repository}

Commit:
{commit}

Changed Files:
{changed_files}

Deterministic Code Analysis:
{code_analysis}

Deterministic Security Analysis:
{security_analysis}

Calculated Risk Score:
{risk_score}/10

Git Diff:
{git_diff}

Provide the review using the following structure:

## Engineering Assessment

Explain what the change appears to do and whether it introduces
meaningful engineering risk.

## Code Quality

Discuss the quality of the actual change. Do not invent issues
that are not supported by the diff.

## Security Assessment

Interpret the security findings. Explain the practical impact
of any detected issue.

## Performance

Discuss performance implications only if the change provides
evidence for them. Otherwise state that no significant
performance concern is evident.

## Maintainability

Assess how the change affects maintainability and future
development.

## Risk Assessment

Explain the calculated risk score and whether you agree with
the resulting risk level.

## Recommendations

Provide specific, actionable recommendations. Prioritize the
most important fixes first.

## Final Decision

Choose exactly one:

APPROVE
REVIEW
BLOCK

Then explain the decision briefly.

Important rules:

- Base your reasoning on the supplied Git diff and analysis.
- Do not invent files, functions, vulnerabilities, or behavior.
- Distinguish confirmed findings from potential concerns.
- If a security finding is confirmed by the deterministic scanner,
  do not dismiss it.
- Give your own engineering judgment rather than using generic
  checklist language.
"""

    def review_code(
        self,
        repository: str,
        commit: str,
        changed_files: list[str],
        git_diff: str,
        code_analysis: dict,
        security_analysis: dict,
        risk_score: int,
    ) -> str:

        logger.info("Generating AI engineering assessment...")

        prompt = self.build_prompt(
            repository=repository,
            commit=commit,
            changed_files=changed_files,
            git_diff=git_diff,
            code_analysis=code_analysis,
            security_analysis=security_analysis,
            risk_score=risk_score,
        )

        response = self.llm_service.generate_response(prompt)

        logger.info("AI engineering assessment completed.")

        return response