# 🔐 Sistema de Gerenciamento de Usuários em Python

Este projeto é um sistema simples de cadastro e login de usuários desenvolvido em Python. Ele utiliza arquivos JSON para armazenar os dados de forma persistente, sem necessidade de banco de dados externo.

## 📌 Funcionalidades

- Cadastro de usuários com nome de usuário e senha
- Login com verificação de credenciais
- Verificação de duplicidade no cadastro
- Listagem de todos os usuários registrados
- Armazenamento em arquivo `data.json`

## 🧠 Estrutura do Código

A classe principal do projeto é a `UserManager`, que contém os seguintes métodos:

- `register(username, password)`: Registra um novo usuário, impedindo nomes duplicados.
- `login(username, password)`: Verifica se as credenciais informadas são válidas.
- `get_all_users()`: Retorna uma lista com os nomes de todos os usuários cadastrados.
- Métodos internos `_load_data()` e `_save_data()` cuidam da leitura e escrita do arquivo JSON.

## 🗃️ Estrutura de Arquivos


## ▶️ Como usar

1. Clone ou baixe o repositório.
2. Execute o script Python em um ambiente com Python 3 instalado.
3. Utilize a classe `UserManager` em seu código:

```python
from user_manager import UserManager

manager = UserManager()

# Cadastrar usuário
manager.register("arthur", "1234")

# Login
if manager.login("arthur", "1234"):
    print("Login bem-sucedido!")
else:
    print("Credenciais inválidas.")
