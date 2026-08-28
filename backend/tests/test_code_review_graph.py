from unittest.mock import patch

from backend.agents.code_review_graph import code_review_graph


def test_code_review_graph():

    test_state = {
        "repository": "test/repository",
        "commit": "abc123",
        "changed_files": [
            "app.py",
            "config.py"
        ],
        "git_diff": """
+ password=admin123
+ print("test")
"""
    }

    mock_review = """
The code contains a hard-coded password.
This is a high-severity security issue.
The credential should be moved to a secure environment variable or secret manager.
"""

    with patch(
        "backend.agents.review_agent.ReviewAgent.review_code",
        return_value=mock_review
    ):
        result = code_review_graph.invoke(test_state)

    print("\n===== CODE REVIEW RESULT =====")
    print(result)

    # Deterministic analysis
    assert result["risk_score"] == 5
    assert result["code_analysis"]["risk_level"] == "MEDIUM"

    # Security detection
    assert len(result["security_analysis"]["findings"]) > 0

    finding = result["security_analysis"]["findings"][0]

    assert finding["type"] == "password"
    assert finding["severity"] == "high"

    # Mocked LLM review
    assert result["llm_review"] is not None
    assert len(result["llm_review"]) > 0

    print("\n===== AI ENGINEERING REVIEW =====")
    print(result["llm_review"])