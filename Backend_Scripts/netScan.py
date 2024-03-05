from scapy.all import *
import requests
import socket
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def checkLastPasswordChange(macaddress):
    try:
        file = open('../Backend_Devices/deviceLog.json')
        data = json.load(file)
        file.close()
    except:
        return "No"
    try:
        return data[macaddress]['date_changed']
    except:
        return "No"

def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def has_password_field(ip):
    driver = init_driver()
    print("Currently attempting to log in to", ip)
    try:
        driver.get(f'http://{ip}')
        sleep(1)
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

        if password_field:
            print('password field found')
            driver.quit()
            return True
        else:
            print('password field not found')
            driver.quit()
            return False
    except Exception as e:
        print(f"An error occurred while attempting to log in to {ip}: {e}")
        driver.quit()
        return False

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def ping_device(IP):
    url = f'http://{IP}'
    try:
        # Send a GET request to the IP address
        response = requests.get(url, timeout=2)
        # Check if the request was successful
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur
        return False

def lookup_mac(mac_address):
    api_url = f"https://api.maclookup.app/v2/macs/{mac_address}/company/name"
    headers = {'X-Authentication-Token': '01hpfz52rgcmadx8fj1nk2hvbf01hpfzbn2yc9fwk95sma3s7xenjgbkij9m0nrc'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.text.strip()  # Removes any leading/trailing whitespace
    elif response.status_code in [400, 401, 409]:
        return response.json().get('message', 'Error')
    else:
        return '*NO COMPANY*'

def arp_scan(ip):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, unans = srp(request, timeout=2, retry=1)
    result = {}

    for i, (name, received) in enumerate(ans):

        result[f'Device {i+1}'] = {'IP': received.psrc,
                                   'MAC': received.hwsrc,
                                   'Company': lookup_mac(received.hwsrc),
                                   'flagged': False,
                                   'passwordChanged': checkLastPasswordChange(received.hwsrc),                                   'lastPasswordChange': '',
                                   'Accessible': ping_device(received.psrc),
                                   'hasPasswordField': has_password_field(received.psrc) }
    return result


def main():
    # Creates dictionary of Ip address on network must input the range of IP to search
    local_IP = arp_scan(get_IP() + '/24')

    # Creates the Json object
    json_IP = json.dumps(local_IP, indent = 3)

    # Writes json to a file
    with open("localIP.json", "w") as output:
        output.write(json_IP)
        print(json_IP)

if __name__ == '__main__':
    main()
