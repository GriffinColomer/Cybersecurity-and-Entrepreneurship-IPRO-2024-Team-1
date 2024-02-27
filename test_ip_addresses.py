import requests
import json
import subprocess

# Path to the JSON file
json_file_path = 'Backend_Scripts/localIP.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Extract IP addresses
ip_addresses = [device["IP"] for device in json_data.values()]

# List to store responsive IP addresses
responsive_ips = []

# Loop through each IP address
for ip in ip_addresses:
    url = f'http://{ip}'
    try:
        # Send a GET request to the IP address
        response = requests.get(url, timeout=5)
        # Check if the request was successful
        if response.status_code == 200:
            print(f'Successfully accessed {url}')
            responsive_ips.append(ip)
        else:
            print(f'Failed to access {url} - Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur
        print(f'Error accessing {url} - {e}')

# Pass the responsive IPs to the seleniumLoginRouter.py script
if responsive_ips:
    ip_string = ','.join(responsive_ips)
    subprocess.run(['python', 'Backend_Scripts/seleniumLoginRouter.py', ip_string])
else:
    print('No responsive IP addresses found.')