from qli_login import TokenManager
import requests
import json

class DataManager:
    def __init__(self):
        
        # Initalizing TokenManager object
        self.token = TokenManager()

        # User API Datapoint
        self.epoch = None
        self.active_connections = None
        self.total_shares = None
        self.shares_per_solution = None

        # EstimatedSolutionRevenue API Datapoint
        self.qubic_per_solution100 = None
        self.qubic_per_solution95 = None
        self.qubic_per_solution90 = None

    def get_User_API(self):
        data_url = "https://stats-test.qubic.li/user"

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.token.access_token,
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

        response = requests.get('https://api.qubic.li/Score/EstimatedSolutionRevenue', headers=headers)
        return response.text
        



    def get_ESR_API(self):
        data_url = "https://api.qubic.li/Score/EstimatedSolutionRevenue"



#debugging
data = DataManager()
data.get_User_API()


        

