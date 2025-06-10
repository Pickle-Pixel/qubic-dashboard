import requests
import time
import jwt
from credential_fetcher import get_secret


class TokenManager:
    def __init__(self):
        self.username, self.password = get_secret()
        self.access_token = None
        self.refresh_token = None
        self.expiry_time = 0

    def login(self):
        login_url = "https://api.qubic.li/Auth/Login"

        # payload for request
        payload = {
        "username": self.username,
        "password": self.password,
        "twoFactorCode": "",
        "loadProfile": True
        }


        # headers for request
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://pool.qubic.li",
        "Referer": "https://pool.qubic.li/"
        }

        response = requests.post(login_url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Login failed error: {response}")
        

        data = response.json()
        self.access_token = data["token"]
        self.refresh_token = data["refreshToken"]

        # Decode token to get expiry time
        decoded = jwt.decode(self.access_token, options={"verify_signature": False})
        self.expiry_time = decoded["exp"]

        # Get token
    def get_token(self):
        if not self.access_token:
            self.login()
        return self.access_token
        # Get token expiry in seconds
    def get_expiry(self):
        return self.expiry_time - time.time()


    # Initialize the class
token_manager = TokenManager()


    # Debugging
token = token_manager.get_token()
expiry = token_manager.get_expiry()
print(token)
print(expiry)


    
    


