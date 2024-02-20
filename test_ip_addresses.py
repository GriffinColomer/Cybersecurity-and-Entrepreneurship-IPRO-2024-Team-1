import requests
import json

# Path to the JSON file
json_file_path = 'Backend_Scripts/localIP.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Extract IP addresses
ip_addresses = [device["IP"] for device in json_data.values()]

# Loop through each IP address
for ip in ip_addresses:
    url = f'http://{ip}'
    try:
        # Send a GET request to the IP address
        response = requests.get(url, timeout=5)
        # Check if the request was successful
        if response.status_code == 200:
            print(f'Successfully accessed {url}')
        else:
            print(f'Failed to access {url} - Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur
        print(f'Error accessing {url} - {e}')
