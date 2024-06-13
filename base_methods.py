import requests
from requests.exceptions import RequestException
from url_data import base_url, path


class BaseMethods:
    def __init__(self):
        self.base_url = base_url
        self.path = path

    def get_data(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}{self.path}{endpoint}")
            return response
        except RequestException:
            return None

    def post(self, endpoint, payload):
        try:
            response = requests.post(f"{self.base_url}{self.path}{endpoint}", json=payload)
            return response
        except RequestException:
            return None

    def delete(self, endpoint, object_id):
        try:
            response = requests.delete(f"{self.base_url}{self.path}{endpoint}/{object_id}")
            return response
        except RequestException:
            return None
