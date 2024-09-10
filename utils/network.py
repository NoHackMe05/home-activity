import hashlib
import os
import ipaddress
import uuid
import random
import time
import sys

try:
    import requests
    from scapy.all import Ether, ARP, srp
except ImportError as err:
    print(err)
    sys.stdout.write('[!] All required modules are not installed.\n')
    sys.stdout.write('[!] Please try: pip install -r requirements.txt\n')
    sys.exit(1)

class NetworkScanner:
    def __init__(self, interface, db, file_manager):
        self.interface = interface
        self.db = db
        self.file_manager = file_manager

    def run(self):
        check_sha256 = self.file_manager.load_json(f"data/liste_sha256_{self.interface}.json")
        check_host = self.file_manager.load_json("json/uphosts.json")
        surveillance = self.file_manager.load_json("json/surveillance.json")

        _range = os.getenv("range")
        network = ipaddress.IPv4Network(_range, strict=False)
        ip_addresses = [str(ip) for ip in network.hosts()]
        random.shuffle(ip_addresses)

        message = ''
        scan_rate = float(os.getenv("SCAN_RATE"))

        for ip in ip_addresses:
            message += self.scan_network(ip, check_sha256, check_host, surveillance)
            time.sleep(scan_rate)

        self.file_manager.save_json(f"data/liste_sha256_{self.interface}.json", check_sha256)

        if message:
            self.send_alert(message)

    def scan_network(self, ip, check_sha256, check_host, surveillance):
        message = ''
        _pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        ans, _ = srp(_pkt, iface=self.interface, timeout=0.1, verbose=False)
        
        for _, recv in ans:
            if recv:
                my_sha256 = hashlib.sha256(str.encode(recv[Ether].src)).hexdigest()

                if my_sha256 not in check_host and my_sha256 not in check_sha256:
                    check_sha256.append(my_sha256)

                    unique_id = uuid.uuid4().hex
                    message += f"Host Alive: {unique_id}\n"

                    filename = f"data/{unique_id}.txt"
                    with open(filename, 'w') as f:
                        f.write(f"Host Alive: {recv[ARP].psrc} - {recv[Ether].src} - {my_sha256}\n")
                
                if my_sha256 in surveillance:
                    self.db.update_or_insert_scan(recv[Ether].src)

        return message

    def send_alert(self, message):
        data = {
            'api_dev_key': os.getenv("API_KEY"),
            'api_sujet': 'One or more machines detected...',
            'api_message': message
        }
        requests.post(url=os.getenv("API_ENDPOINT"), data=data)
