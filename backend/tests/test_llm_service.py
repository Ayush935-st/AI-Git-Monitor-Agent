from unittest.mock import patch, Mock

from backend.services.llm_services import LLMService


def test_llm_service():
    service = LLMService()

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "SOLID principles promote maintainable and flexible software design."
                }
            }
        ]
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "backend.services.llm_services.requests.post",
        return_value=mock_response
    ) as mock_post:

        response = service.generate_response(
            "Explain SOLID principles in 50 words."
        )

    assert response == (
        "SOLID principles promote maintainable and flexible software design."
    )

    mock_post.assert_called_once()