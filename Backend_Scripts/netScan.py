from scapy.all import *
import json

def arp_scan(ip):
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, unans = srp(request, timeout=2, retry=1)
    result = {}

    for i, (name, received) in enumerate(ans):
        result[f'Device {i+1}'] = {'IP': received.psrc, 'MAC': received.hwsrc}
    return result

def main():
    # Creates dictionary of Ip address on network must input the range of IP to search
    local_IP = arp_scan(read_routes()[2][4] + '/24')

    # Creates the Json object
    json_IP = json.dumps(local_IP, indent = 3)

    # Writes json to a file
    with open("loaclIP.json", "w") as output:
        output.write(json_IP)

if __name__ == '__main__':
    main()

