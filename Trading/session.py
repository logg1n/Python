import hashlib
import hmac
import time
import requests
from support import Support


class Session:
    def __init__(self, key, secret):
        self.api_key = key
        self.secret_key = secret
        self.httpClient = requests.Session()
        self.recv_window = str(5000)
        self.url = "https://api-demo.bybit.com"  #  endpoint
        self.headers = {}

    def HTTP_Request(self, endPoint, method, api_params):
        time_stamp = str(int(time.time() * 10**3))
        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": hmac.new(
                bytes(self.secret_key, "utf-8"),
                (time_stamp + self.api_key + self.recv_window + api_params).encode(
                    "utf-8"
                ),
                hashlib.sha256,
            ).hexdigest(),
            "X-BAPI-SIGN-TYPE": "2",
            "X-BAPI-TIMESTAMP": time_stamp,
            "X-BAPI-RECV-WINDOW": self.recv_window,
            "Content-Type": "application/json",
        }
        if method == "POST":
            return self.httpClient.request(
                method, self.url + endPoint, headers=headers, data=api_params
            ).json()
        else:
            return self.httpClient.request(
                method, self.url + endPoint + "?" + api_params, headers=headers
            ).json()
