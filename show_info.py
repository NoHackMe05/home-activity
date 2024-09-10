import os
import sys

from utils.database import Database
from utils.file_operations import FileManager
from utils.weekly_report import WeeklyReport

try:
    from dotenv import load_dotenv
except ImportError as err:
    print(err)
    sys.stdout.write('[!] All required modules are not installed.\n')
    sys.stdout.write('[!] Please try: pip install -r requirements.txt\n')
    sys.exit(1)

load_dotenv()

def main():
    # Connexion à la base de données SQLite
    db_path = os.path.join(os.getcwd(), "scans.db")
    db = Database(db_path)
    file_manager = FileManager(os.getcwd())
    report_generator = WeeklyReport(db, file_manager)

    # Génération du rapport hebdomadaire
    report = report_generator.generate_weekly_report()

    # Envoi du rapport par email via l'API
    report_generator.send_weekly_report_via_api(report)

    # Nettoyage des données anciennes
    report_generator.cleanup_old_data()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("CTRL+C pressed. Exiting.")
        sys.exit(0)
