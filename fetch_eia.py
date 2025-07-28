import pandas as pd
import numpy as np
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() 

# Load API key from .env file; Place .env file in the same directory as this script
# Ensure the .env file contains a line like: EIA_API_KEY=your_api_key_here
api_key = os.getenv("EIA_API_KEY")
if api_key is None:
    raise ValueError("EIA_API_KEY environment variable not set")


def load_config(config_path):
    """
    Load API configuration from a JSON file.

    Parameters:
        config_path (str): Path to the JSON config file containing 'url' and 'header' keys.

    Returns:
        tuple: A tuple containing the API URL (str) and the request header (dict).
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config["url"], config["header"]


# Header for pulling net generation for all balancing authorities and fuel types for the year of 2019
## Header for pulling total interchange (transmission) for all balancing authorities and fuel types for the year of 2019
## Header for pulling transmission balancing authority to balancing authority 

def fetch_data(config_path, output_file="./outputs/output.csv", chunk_size=6000):
    """
    Fetch data from the EIA API using a .json file in /configs and save the results to a CSV.

    Parameters:
        config_path (str): Path to the JSON config file containing API URL and header.
        output_file (str): Path to the output CSV file. Defaults to './outputs/output.csv'.
        chunk_size (int): Number of records to collect before writing to CSV. Suggested value = 6000.

    Notes:
        - Requires the 'EIA_API_KEY' to be set as an environment variable.
        - Automatically paginates using the 'offset' and 'length' values in the header.
        - Overwrites the output file if it already exists.
    """

    url, header = load_config(config_path)
    header = header.copy()
    params = {"api_key": api_key}
    all_data = []

    if os.path.exists(output_file):
        os.remove(output_file)

    while True:
        try:
            r = requests.get(url, params=params, headers={"X-Params": json.dumps(header)})
            r.raise_for_status()
            json_data = r.json()
            data = json_data["response"]["data"]

            if not data:
                break

            all_data.extend(data)

            # Save chunk to CSV
            if len(all_data) >= chunk_size:
                df = pd.DataFrame(all_data)
                df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                all_data = [] # Clear the list for the next chunk

            header["offset"] += header["length"]

        except Exception as e:
            print(f"Error during request: {e}")
            break

    # Save any remaining data
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)


if __name__ == "__main__":
    fetch_data(config_path="configs/nc_plant_generation.json", output_file="./outputs/nc_plant_generation.csv")
