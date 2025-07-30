import requests
from .exceptions import AuthenticationError, APIRequestError

class SMSGatewayClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "api-key": api_key
        }

    def send_sms(self, recipient: str, message: str):
        url = f"{self.base_url}/sms"
        payload = {
            "recipient": recipient,
            "message": message
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError("Invalid or missing API key")
        if not response.ok:
            raise APIRequestError(f"Failed to send SMS: {response.text}")
        return response.json()

    def get_inbox(self):
        url = f"{self.base_url}/sms/inbox"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError("Invalid or missing API key")
        if not response.ok:
            raise APIRequestError(f"Failed to retrieve inbox: {response.text}")
        return response.json().get("messages", [])

    def get_logs(self):
        url = f"{self.base_url}/logs"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError("Invalid or missing API key")
        if not response.ok:
            raise APIRequestError(f"Failed to retrieve logs: {response.text}")
        return response.json()
