from qli_login import TokenManager



class DataManager:
    def __init__(self):
        
        # Initalizing TokenManager object
        token = TokenManager()

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




    def get_ESR_API(self):
        data_url = "https://api.qubic.li/Score/EstimatedSolutionRevenue"

        

