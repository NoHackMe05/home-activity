import sqlite3
import datetime

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.initialize()

    def initialize(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac_addr TEXT NOT NULL,
                last_view TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duree INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def update_or_insert_scan(self, mac_addr):
        cursor = self.conn.cursor()
        new_time = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT * FROM scans WHERE mac_addr = ? AND last_view >= ?
        ''', (mac_addr, new_time))
        
        if cursor.fetchone():
            cursor.execute('''
                UPDATE scans SET duree = duree + 5, last_view = CURRENT_TIMESTAMP
                WHERE mac_addr = ? AND last_view >= ?
            ''', (mac_addr, new_time))
            print(f"UPDATE scans SET duree = duree + 5, last_view = CURRENT_TIMESTAMP WHERE mac_addr = {mac_addr} AND last_view >= {new_time}")
        else:
            cursor.execute('''
                INSERT INTO scans (mac_addr, last_view, duree) VALUES (?, CURRENT_TIMESTAMP, 0)
            ''', (mac_addr,))
            print(f"INSERT INTO scans (mac_addr, last_view, duree) VALUES ({mac_addr}, CURRENT_TIMESTAMP, 0)")
        
        self.conn.commit()
