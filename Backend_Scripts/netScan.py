from scapy.all import *
import requests
import socket
import json

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
                                   'passwordChanged': False,
                                   'lastPasswordChange': ''}
    return result

def main():
    # Creates dictionary of Ip address on network must input the range of IP to search
    local_IP = arp_scan(get_IP() + '/24')

    # Creates the Json object
    json_IP = json.dumps(local_IP, indent = 3)

    # Writes json to a file
    with open("localIP.json", "w") as output:
        output.write(json_IP)

if __name__ == '__main__':
    main()
