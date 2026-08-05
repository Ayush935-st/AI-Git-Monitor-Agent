from unittest.mock import MagicMock

from backend.agents.review_agent import ReviewAgent


def test_review():

    agent = ReviewAgent()

    agent.llm_service.generate_response = MagicMock(
        return_value="Review Generated Successfully"
    )

    review = agent.review_code("sample git diff")

    assert review == "Review Generated Successfully"