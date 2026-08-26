from pathlib import Path

from backend.agents.report_agent import ReportAgent


def test_report_agent():

    agent = ReportAgent()

    review = """
## Engineering Assessment

The change introduces a potential security concern that should
be reviewed before merging.

## Code Quality

The change is small and does not introduce significant structural
complexity.

## Security Assessment

A hard-coded credential was detected and should be removed.

## Performance

No significant performance concerns were identified.

## Maintainability

The change is relatively simple, but credential management
should be improved.

## Risk Assessment

The change requires review because of the security finding.

## Recommendations

Move credentials to a secure configuration or secret-management
system.

## Final Decision

REVIEW
"""

    commit_hash = "abc123"

    markdown_report = agent.generate_markdown(
        review=review,
        commit_hash=commit_hash,
        repository="test/repository",
        changed_files=[
            "app.py",
            "config.py",
        ],
        code_analysis={
            "changed_file_count": 2,
            "added_lines": 2,
            "removed_lines": 0,
            "diff_size": 37,
            "findings": [],
            "risk_level": "MEDIUM",
        },
        security_analysis={
            "findings": [
                {
                    "type": "password",
                    "severity": "high",
                    "count": 1,
                    "message": "Potential password detected.",
                }
            ],
            "finding_count": 1,
        },
        risk_score=5,
    )

    pdf_report = agent.generate_pdf(
        review=review,
        commit_hash=commit_hash,
        repository="test/repository",
        changed_files=[
            "app.py",
            "config.py",
        ],
        code_analysis={
            "changed_file_count": 2,
            "added_lines": 2,
            "removed_lines": 0,
            "diff_size": 37,
            "findings": [],
            "risk_level": "MEDIUM",
        },
        security_analysis={
            "findings": [
                {
                    "type": "password",
                    "severity": "high",
                    "count": 1,
                    "message": "Potential password detected.",
                }
            ],
            "finding_count": 1,
        },
        risk_score=5,
    )

    print("\n===== REPORT TEST =====")
    print("Markdown:", markdown_report)
    print("PDF:", pdf_report)

    assert Path(markdown_report).exists()
    assert Path(pdf_report).exists()

    assert Path(markdown_report).stat().st_size > 0
    assert Path(pdf_report).stat().st_size > 0