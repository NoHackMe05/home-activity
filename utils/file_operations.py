import json
import os

class FileManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def load_json(self, filename):
        try:
            with open(os.path.join(self.base_path, filename), "r") as read_file:
                return json.load(read_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_json(self, filename, data):
        with open(os.path.join(self.base_path, filename), 'w') as file:
            json.dump(data, file)
