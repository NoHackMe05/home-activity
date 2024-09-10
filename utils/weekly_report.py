import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

try:
    import requests
except ImportError as err:
    print(err)
    sys.stdout.write('[!] All required modules are not installed.\n')
    sys.stdout.write('[!] Please try: pip install -r requirements.txt\n')
    sys.exit(1)

class WeeklyReport:
    def __init__(self, db, file_manager):
        self.db = db
        self.file_manager = file_manager

    def get_previous_week_dates(self):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday() + 7)
        return [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    def generate_weekly_report(self):
        cursor = self.db.conn.cursor()
        dates = self.get_previous_week_dates()
        report = defaultdict(lambda: defaultdict(int))  # {date: {mac_addr: total_duree}}

        for date in dates:
            cursor.execute("SELECT mac_addr, duree FROM scans WHERE last_view LIKE ?", (date + '%',))
            rows = cursor.fetchall()

            for mac_addr, duree in rows:
                report[date][mac_addr] += duree if duree > 0 else 5

        return report

    def send_weekly_report_via_api(self, report):
        message = "Weekly MAC Address Activity Report\n\n"

        identity = self.file_manager.load_json("json/identity.json")
        
        for date, mac_data in report.items():
            message += f"Date: {date}\n"
            for mac_addr, total_duree in mac_data.items():
                my_identity = identity.get(mac_addr, 'Unknown')

                if total_duree <= 60:
                    message += f"  {my_identity}, Total Duration: {total_duree} minutes\n"
                else:
                    heures = total_duree // 60
                    minutes = total_duree % 60
                    message += f"  {my_identity}, Total Duration: {heures} hours and {minutes} minutes\n"
                
            message += "\n"

        data = {
            'api_dev_key': os.getenv("API_KEY"),
            'api_sujet': 'Weekly MAC Address Activity Report',
            'api_message': message
        }

        r = requests.post(url=os.getenv("API_ENDPOINT"), data=data)
        if r.status_code == 200:
            print("Report sent successfully")
        else:
            print(f"Failed to send report: {r.status_code}")

    def cleanup_old_data(self):
        cursor = self.db.conn.cursor()
        cutoff_date = (datetime.today() - timedelta(days=8)).strftime('%Y-%m-%d')
        cursor.execute("DELETE FROM scans WHERE last_view < ?", (cutoff_date + '%',))
        self.db.conn.commit()
