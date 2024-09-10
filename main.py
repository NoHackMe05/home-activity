import os
import sys

from utils.database import Database
from utils.file_operations import FileManager
from utils.network import NetworkScanner

try:
    from dotenv import load_dotenv
except ImportError as err:
    print(err)
    sys.stdout.write('[!] All required modules are not installed.\n')
    sys.stdout.write('[!] Please try: pip install -r requirements.txt\n')
    sys.exit(1)

load_dotenv()

def main():
    my_path = os.getcwd()
    _interface = sys.argv[1]

    db = Database(os.path.join(my_path, "scans.db"))
    file_manager = FileManager(my_path)
    network_scanner = NetworkScanner(_interface, db, file_manager)

    network_scanner.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("CTRL+C pressed. Exiting.")
        sys.exit(0)
