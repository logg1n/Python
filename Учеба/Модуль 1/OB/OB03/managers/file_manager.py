import json
import os
from typing import Dict


class FileManager:
    def __init__(self, file_name: str, file_path: str):
        self.name = file_name
        self.path = f"{file_path}/save"

    def save(self, data: str):
        with open(f"{self.path}/{self.name}.zoo", "w") as file:
            json.dump(data, file)

    def load(self) -> Dict:
        try:
            with open(f"{self.path}/{self.name}.zoo", "r") as file:
                data = json.load(file)

                return json.loads(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
