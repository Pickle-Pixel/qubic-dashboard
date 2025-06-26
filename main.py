from data_fetcher import DataManager
import time

while True:
    try:
        # initializing DataManager object
        data = DataManager()
        # Fetching data from the Qubic API and saving it to a MongoDB database
        data.get_esr_api()
        # Fetching user data from the Qubic API
        data.get_user_api()
        # Saving the fetched data to the database
        data.save_to_db()
        
        print("Data fetched and saved successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Sleep for 5 minutes before fetching again
    time.sleep(300)  