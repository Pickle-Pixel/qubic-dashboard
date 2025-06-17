from flask import Flask, jsonify
from pymongo import MongoClient
from credential_fetcher import get_secret

def serve_data():
    app = Flask(__name__)
    
    qubic_username, qubic_password, mongo_username, mongo_password = get_secret()

    # debug purposes
    #print(mongo_password, mongo_username)

    # MongoDB connection
    uri = f"mongodb+srv://{mongo_username}:{mongo_password}@cluster0.4s0bnni.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri)
    db = client["qubic_dashboard"]
    collection = db["metrics"]

    @app.route('/data', methods=['GET'])
    def get_data():
        latest_entries = list(
            collection.find({}, {'_id': 0}).sort("time_stamp", -1).limit(48)    
        )
        return jsonify(latest_entries)



        # Start Flask server
    app.run(host='0.0.0.0', port=5001)
    
if __name__ == '__main__':
    serve_data()