# import statements
import json
import ssl
import requests
from . import config as Config
verbose=False

def print_json_nicely(data):
    for x in dict(data):
        print(f"{x}:{data[x]}")


def read_experiment(experiment_id=75):
    endpoint = Config.base_url+"experiments/"+str(experiment_id)
    response = requests.get(endpoint, headers=Config.headers)
    data = response.json()
    if response.status_code == 200:
        # Request was successful
        if verbose:print_json_nicely(data)
    else:
        # Request failed
        print("Error:", response.status_code, response.text)
    return data
