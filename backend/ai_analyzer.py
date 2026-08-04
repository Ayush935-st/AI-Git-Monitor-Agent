import json
import requests
from pathlib import Path

from backend.config import OLLAMA_MODEL, OLLAMA_URL


class AIAnalyzer:

    def __init__(self):

        prompt_file = Path("prompts/review_prompt.txt")

        with open(prompt_file, "r", encoding="utf-8") as file:
            self.prompt_template = file.read()

    def analyze(self, diff_text):

        prompt = self.prompt_template.replace("{diff}", diff_text)

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        try:

            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=300
            )

            response.raise_for_status()

            result = response.json()["response"]

            try:
                return json.loads(result)

            except Exception:

                return {
                    "summary": result,
                    "modified_functionality": "",
                    "bugs": [],
                    "security": [],
                    "performance": [],
                    "recommendations": [],
                    "risk": "Unknown"
                }

        except Exception as e:

            return {
                "error": str(e)
            }