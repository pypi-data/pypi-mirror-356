import requests

class NineBitCIQClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

    def get_status(self):
        response = self.session.get(f"{self.base_url}/status")
        response.raise_for_status()
        return response.json()

    def hello(self, name: str) -> None:
        """Prints a greeting to the CLI."""
        print(f"hello, {name}")