import requests
from credential_fetcher import get_secret


response = ""
username, password = get_secret() #fetch username and password
def qli_login():
    login_url = "https://api.qubic.li/Auth/Login"

    # Payload
    payload = {
    "username": username,
    "password": password,
    "twoFactorCode": "",
    "loadProfile": True
    }

    # Headers
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://pool.qubic.li",
    "Referer": "https://pool.qubic.li/"
    }

    # Send Login Request
    response = requests.post(login_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Login Failed: {response.text}")
    
    # Extract tokens from response
    data = response.json()
    access_token = data["token"]
    refresh_token = data["refreshToken"]

    if not access_token:
        raise Exception(f"Access token not found in login response. {response.text}")
    
    return access_token, refresh_token

token, refresh = qli_login()
print(token, refresh)


    
    


