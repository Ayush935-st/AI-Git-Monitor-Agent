from unittest.mock import MagicMock

from backend.agents.review_agent import ReviewAgent


def test_review():

    agent = ReviewAgent()

    agent.llm_service.generate_response = MagicMock(
        return_value="Review Generated Successfully"
    )

    review = agent.review_code(
        repository="test/repository",
        commit="abc123",
        changed_files=[
            "app.py",
            "config.py"
        ],
        git_diff="+ password=admin123\n+ print('test')",
        code_analysis={
            "changed_file_count": 2,
            "findings": []
        },
        security_analysis={
            "findings": [
                {
                    "type": "password",
                    "severity": "high",
                    "message": "Potential password detected."
                }
            ]
        },
        risk_score=5
    )

    assert review == "Review Generated Successfully"

    agent.llm_service.generate_response.assert_called_once()