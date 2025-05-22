import json
import os

class ProductManager:
    def __init__(self, username):
        self.username = username
        self.data_file = f"{username}_estoque.json"
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as file:
                json.dump([], file)

    def _load_data(self):
        with open(self.data_file, "r") as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)

    def add_product(self, name, quantity):
        products = self._load_data()
        for product in products:
            if product["name"].lower() == name.lower():
                product["quantity"] += quantity
                self._save_data(products)
                return "atualizado"
        products.append({"name": name, "quantity": quantity})
        self._save_data(products)
        return "novo"

    def remove_product(self, name):
        products = self._load_data()
        products = [p for p in products if p["name"] != name]
        self._save_data(products)
        return True

    def list_products(self, search_term=""):
        products = self._load_data()
        if search_term:
            products = [p for p in products if search_term.lower() in p["name"].lower()]
        return products

    def edit_product(self, old_name, new_name, new_quantity):
        products = self._load_data()
        for product in products:
            if product["name"] == old_name:
                product["name"] = new_name
                product["quantity"] = new_quantity
                self._save_data(products)
                return True
        return False

    def total_quantity(self):
        products = self._load_data()
        return sum(p["quantity"] for p in products)
