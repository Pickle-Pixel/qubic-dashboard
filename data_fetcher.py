from qli_login import TokenManager
import requests
import json
import tls_requests

# DataManager class to handle API requests and data management


class DataManager:
    def __init__(self):
        
        # Initalizing TokenManager object
        self.token = TokenManager()
        self.token.login()
        print("test: ", self.token.access_token)

        # User API Datapoint
        self.epoch = None
        self.active_connections = None
        self.total_shares = None
        self.shares_per_solution = None

        # EstimatedSolutionRevenue API Datapoint
        self.qubic_per_solution100 = None
        self.qubic_per_solution95 = None
        self.qubic_per_solution90 = None
        

        
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': "Bearer " + self.token.access_token,
            'origin': 'https://pool.qubic.li',
            'referer': 'https://pool.qubic.li/',
            'sec-ch-ua': '"Not.A/Brand";v="99", "Chromium";v="136"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }

    # EstimatedSolutionRevenue API
    def get_ESR_API(self):
        data_url = "https://api.qubic.li/Score/EstimatedSolutionRevenue"

        response = requests.get(data_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.status_code} - {response.text}")
        
        # unpacking the response
        data = response.json()
        
        self.qubic_per_solution100 = data["qubicPerSolution100"]
        self.qubic_per_solution95 = data["qubicPerSolution95"]
        self.qubic_per_solution90 = data["qubicPerSolution90"]
        return data
        

    def get_User_API(self):
        data_url = "https://stats-test.qubic.li/user"
        
        # using wrapper-tls-request to bypass Cloudflare
        response = tls_requests.get(data_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.status_code} - {response.text}")
        
        # unpacking the response
        data = response.json()
        return data
        



#debugging
data = DataManager()
test = data.get_User_API()
print(test)

        

