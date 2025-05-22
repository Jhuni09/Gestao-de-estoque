import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, username):
        self.filename = f"data/historico_{username}.json"
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def registrar(self, acao, nome, quantidade=None, novo_nome=None):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        registro = {"data": timestamp, "ação": acao, "produto": nome}

        if quantidade is not None:
            registro["quantidade"] = quantidade
        if novo_nome:
            registro["novo_nome"] = novo_nome

        with open(self.filename, "r+") as f:
            historico = json.load(f)
            historico.append(registro)
            f.seek(0)
            json.dump(historico, f, indent=2)

    def listar(self):
        with open(self.filename, "r") as f:
            return json.load(f)
