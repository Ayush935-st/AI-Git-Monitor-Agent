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
        Send prompt to NVIDIA NIM and return AI response.
        """
        print("Prompt:", prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        try:
            logger.info("Sending request to NVIDIA NIM...")

            print("Model:", self.model)
            print("URL:", f"{self.BASE_URL}/chat/completions")

            response = requests.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=100,
            )

            print("Status Code:", response.status_code)
            print("Response:")
            print(response.text)

            response.raise_for_status()

            result = response.json()

            logger.info("Response received successfully.")

            return result["choices"][0]["message"]["content"]

        except Timeout:
            logger.error("NVIDIA API request timed out.")
            raise

        except RequestException as e:
            logger.exception(e)
            raise