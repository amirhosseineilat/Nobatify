import requests
from abc import ABC, abstractmethod

sand_box_urls = {
    "send_infor": "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
    "redirect_to_zarinpal": "https://sandbox.zarinpal.com/pg/StartPay/",
    "verify_url": "https://sandbox.zarinpal.com/pg/v4/payment/verify.json",
}


class SandBoxPayment:
    def __init__(self, urls: dict):
        self.urls = urls

    def send_information(
        self, merchat_id, amount, descriptoin, callback_url, metadata, **kwargs
    ):
        data = {
            "merchant_id": merchat_id,
            "amount": amount,
            "callback_url": callback_url,
            # "referrer_id": ,
            "description": descriptoin,
            "metadata": metadata,
        }
        header = {
            "accept": "application/json",
            "content-type": "content-type: application/json",
        }
        r = requests.post(self.urls["send_infor"], json=data, headers=header)
        if r.status_code == 200:
            return True, r.json()
        return False, None

    def redirect_to_zarinpal(self, data):
        url = self.urls["redirect_to_zarinpal"] + data["data"]["authority"]
        return url

    def verify(self, data):
        header = {
            "accept": "application/json",
            "content-type": "content-type: application/json",
        }

        r = requests.post(self.urls["verify_url"], json=data, headers=header)
        if r.status_code == 200:
            return True, r.json()
        return False, None

    def pay(self, amount):
        return super().pay(amount)
