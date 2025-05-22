import json
import os

class UserManager:
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as file:
                json.dump([], file)

    def _load_data(self):
        with open(self.data_file, "r") as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.data_file, "w") as file:
            json.dump(data, file)

    def register(self, username, password):
        users = self._load_data()
        if any(user["username"] == username for user in users):
            return False  # Usuário já existe

        users.append({"username": username, "password": password})
        self._save_data(users)
        return True

    def login(self, username, password):
        users = self._load_data()
        return any(user["username"] == username and user["password"] == password for user in users)

    def get_all_users(self):
        users = self._load_data()
        return [user["username"] for user in users]
