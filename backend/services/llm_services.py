import requests
from requests.exceptions import RequestException, Timeout

from backend.config import settings
from backend.utils.logger import logger


class LLMService:
    """
    Handles communication with NVIDIA NIM API.
    """

    BASE_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(self):
        self.api_key = settings.nvidia_api_key
        self.model = settings.nvidia_model

    def generate_response(self, prompt: str) -> str:
        """
        Send prompt to NVIDIA NIM and return the AI engineering review.
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.2,
            "max_tokens": 1024,
            "stream": False,
            "chat_template_kwargs": {
                "enable_thinking": False
            },
        }

        try:

            logger.info(
                "Sending request to NVIDIA NIM..."
            )

            logger.info(
                f"Model: {self.model}"
            )

            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )

            logger.info(
                f"NVIDIA response status: "
                f"{response.status_code}"
            )

            response.raise_for_status()

            result = response.json()

            content = (
                result["choices"][0]["message"]
                .get("content", "")
            )

            if not content:
                raise RuntimeError(
                    "NVIDIA returned an empty response."
                )

            logger.info(
                "Response received successfully."
            )

            return content

        except Timeout:

            logger.error(
                "NVIDIA API request timed out."
            )

            raise

        except RequestException:

            logger.exception(
                "NVIDIA API request failed."
            )

            raise