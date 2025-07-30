import requests
from .exceptions import AsanakSmsException, AsanakHttpException


class AsanakSmsClient:
    def __init__(self, username: str, password: str, base_url: str = "https://sms.asanak.ir", log: bool = False):
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.log = log

    def _post(self, endpoint: str, data: dict) -> dict:
        payload = {
            "username": self.username,
            "password": self.password,
            **data
        }
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise AsanakHttpException(response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            raise AsanakHttpException(str(e))
            raise AsanakSmsException(str(e))

    def send_sms(self, source, destination, message, send_to_black_list=True):
        return self._post("/webservice/v2rest/sendsms", {
            "source": source,
            "destination": destination,
            "message": message,
            "send_to_black_list": int(send_to_black_list)
        })

    # دیگر متدها مانند template, p2p, get_credit, ... به همین صورت اضافه می‌شوند.
