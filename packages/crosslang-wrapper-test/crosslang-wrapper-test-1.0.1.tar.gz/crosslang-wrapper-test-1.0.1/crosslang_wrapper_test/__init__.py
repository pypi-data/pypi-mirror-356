import requests

class CrossLangWrapperTest:
    def __init__(self, api_key: str, base_url: str = "http://localhost:5000"):
        self.api_key = api_key
        self.base_url = base_url

    def is_server_alive(self) -> bool:
        try:
            res = requests.get(f"{self.base_url}/api/v1")
            return res.text == "Server Up & Running!"
        except requests.RequestException:
            return False

    def run_test(self) -> dict:
        try:
            res = requests.post(
                f"{self.base_url}/api/v1/test/test-route",
                json={"apiKey": self.api_key}
            )
            res.raise_for_status()
            return res.json()

        except requests.HTTPError as http_err:
            return {
                "error": True,
                "status": res.status_code,
                "data": res.json(),
                "message": res.json().get("error", "Something went wrong from backend.")
            }
        except requests.RequestException as net_err:
            return {
                "error": True,
                "message": "No response from server. Network issue?"
            }
        except Exception as e:
            return {
                "error": True,
                "message": "Unexpected error occurred.",
                "detail": str(e)
            }
