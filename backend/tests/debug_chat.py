import requests
from backend.config import settings

url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {settings.nvidia_api_key}",
    "Content-Type": "application/json",
}

payload = {
    "model": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "messages": [
        {
            "role": "user",
            "content": "Hello"
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)

print("Status:", response.status_code)
print(response.text)
