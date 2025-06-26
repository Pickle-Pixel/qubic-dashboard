from qli_login import TokenManager
import requests
import json
import tls_requests
from pymongo import MongoClient
import time
from flask import Flask, jsonify

# DataManager class to handle API requests and data management


class DataManager:
    def __init__(self):
        
        # Initalizing TokenManager object
        self.token = TokenManager()
        self.token.login()

        # User API Datapoint
        self.epoch = None
        self.active_connections = None
        self.total_shares = None
        self.shares_per_solution = None
        self.total_hashrate = None

        # EstimatedSolutionRevenue API Datapoint
        self.qubic_per_solution100 = None
        self.qubic_per_solution95 = None
        self.qubic_per_solution90 = None

        # Custom API Datapoint
        self.estimated_qubic_price = None


        
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
    def get_esr_api(self):
        data_url = "https://api.qubic.li/Score/EstimatedSolutionRevenue"

        response = requests.get(data_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.status_code} - {response.text}")
        
        # unpacking the response
        data = response.json()
        
        self.qubic_per_solution100 = data["qubicPerSolution100"]
        self.qubic_per_solution95 = data["qubicPerSolution95"]
        self.qubic_per_solution90 = data["qubicPerSolution90"]
    

    def get_dashboard_api(self):
        data_url = "https://stats-test.qubic.li/stats/dashboard"

        # using wrapper-tls-request to bypass cloudflare
        response = tls_requests.get(data_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch Dashboard data: {response.status_code} - {response.text}")
        
        #unpacking the response
        data = response.json()
        self.total_hashrate = data["currentStats"][-1]["hashratePps"]

    def get_user_api(self):
        data_url = "https://stats-test.qubic.li/user"
        
        # using wrapper-tls-request to bypass Cloudflare
        response = tls_requests.get(data_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {response.status_code} - {response.text}")
        
        # unpacking the response
        data = response.json()
        self.epoch = data["epoch"]
        self.shares_per_solution = data["sharesPerSolution"]
        self.active_connections = data["userStats"]["activeConnections"]
        self.total_shares = data["userStats"]["totalShares"]

    def get_qubic_price(self):
        data_url = "https://api.coinpaprika.com/v1/tickers/qu-qubic"

        response = requests.get(data_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from PaprikaCoin API. {response.status_code} - {response.text}")
        data = response.json()
        self.estimated_qubic_price = data["quotes"]["USD"]["price"]



    def save_to_db(self):     
        document = {
            "time_stamp": int(time.time()),
            "epoch": self.epoch,
            "active_connections": self.active_connections,
            "total_shares": self.total_shares,
            "shares_per_solution": self.shares_per_solution,
            "total_solutions": self.total_shares / self.shares_per_solution,
            "qubic_per_solution100": self.qubic_per_solution100,
            "qubic_per_solution95": self.qubic_per_solution95,
            "qubic_per_solution90": self.qubic_per_solution90,
            "total_hashrate": self.total_hashrate,
            "qubic_price": self.estimated_qubic_price
        }
        
        # This function can be used to save the data to a database or file
        uri = f"mongodb+srv://{self.token.mongo_username}:{self.token.mongo_password}@cluster0.4s0bnni.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        db = client["qubic_dashboard"]
        collection = db["metrics"]
        collection.insert_one(document)
        
        

        
   


        

