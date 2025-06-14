# credential_fetcher.py

import boto3
from botocore.exceptions import ClientError
import json

_credentials = None

def get_secret():

    global _credentials

    if _credentials is not None:
        print("credentials already cached")
        return _credentials # already cached
    
    secret_name = "Qubic-Account"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    # Convert string to list
    secret_list = json.loads(secret)
    # Your code goes here.
    #print(secret) #debugging purposes
    # Return credentials
    _credentials = secret_list["username"], secret_list["password"]
    return _credentials # _credentials[0] username _credentials[1] password







