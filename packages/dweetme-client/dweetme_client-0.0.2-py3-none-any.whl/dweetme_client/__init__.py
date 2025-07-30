import requests

class DweetClient:
    def __init__(self, base_url="http://dweet.me:3333"):
        self.base_url = base_url

    def publish_dweet(self, topic, data):
        url = f"{self.base_url}/publish/yoink/for/{topic}"
        response = requests.get(url, params=data)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON response", "status_code": response.status_code, "text": response.text}

    def get_latest_dweet(self, topic):
        url = f"{self.base_url}/get/latest/yoink/from/{topic}"
        response = requests.get(url)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON response", "status_code": response.status_code, "text": response.text}

    def get_last_num_dweets(self, topic, count):
        url = f"{self.base_url}/get/latest/{count}/yoinks/from/{topic}"
        response = requests.get(url)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON response", "status_code": response.status_code, "text": response.text}

    def get_all_dweets(self, topic):
        url = f"{self.base_url}/get/all/yoinks/from/{topic}"
        response = requests.get(url)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON response", "status_code": response.status_code, "text": response.text}

#functions missing
#   def get_last_num_dweets
#   def get_all_dweets

