import requests

class LNSClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.base_url = "http://localhost:4000/api/v1"  

    def resolve(self, name: str) -> str:
        if not name:
            raise ValueError("Name is required")

        url = f"{self.base_url}/resolve/{name}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            raise ValueError("Name not registered or expired")
        elif response.status_code != 200:
            raise RuntimeError("Failed to resolve name")

        return response.json()["address"]
