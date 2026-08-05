import requests
from backend.config import settings

headers = {
    "Authorization": f"Bearer {settings.nvidia_api_key}"
}

response = requests.get(
    "https://integrate.api.nvidia.com/v1/models",
    headers=headers
)

data = response.json()

for model in data["data"]:
    print(model["id"])