from scapy.all import *
import json
import requests

def arp_scan(ip):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, unans = srp(request, timeout=2, retry=1)
    result = {}

    for i, (name, received) in enumerate(ans):
        company_name = lookup_mac(received.hwsrc)
        result[f'Device {i+1}'] = {'IP': received.psrc, 'MAC': received.hwsrc, 'Company': company_name}
    return result

def lookup_mac(mac_address):
    api_url = f"https://api.maclookup.app/v2/macs/{mac_address}/company/name"
    headers = {
        'X-Authentication-Token': '01hpfz52rgcmadx8fj1nk2hvbf01hpfzbn2yc9fwk95sma3s7xenjgbkij9m0nrc'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.text.strip()  # Removes any leading/trailing whitespace
    elif response.status_code in [400, 401, 409]:
        return response.json().get('message', 'Error')
    else:
        return '*NO COMPANY*'

def main():
    # Replace '104.194.102.1/24' with the actual IP range you want to scan
    local_IP = arp_scan('104.194.102.1/24')
    json_IP = json.dumps(local_IP, indent=3)

    with open("localIP.json", "w") as output:
        output.write(json_IP)

if __name__ == '__main__':
    main()
