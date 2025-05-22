import customtkinter as ctk
from tkinter import messagebox
from user_manager import UserManager
from product_manager import ProductManager
from PIL import Image
from history_manager import HistoryManager


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class Application(ctk.CTk):

    def view_selected_history(self):
        try:
            selected_user = self.user_listbox.get("insert linestart", "insert lineend").strip()
            if not selected_user:
                raise ValueError
            self.history_manager = HistoryManager(selected_user)
            self.username = selected_user
            self.show_history()
        except:
            messagebox.showerror("Erro", "Selecione um usuário com o cursor.")


    def view_selected_inventory(self):
        try:
            selected_user = self.user_listbox.get("insert linestart", "insert lineend").strip()
            if not selected_user:
                raise ValueError
            self.product_manager = ProductManager(selected_user)
            self.history_manager = HistoryManager(selected_user)
            self.username = selected_user
            self.is_admin = True  # mantém admin mesmo alternando usuário
            self.show_inventory()
        except:
            messagebox.showerror("Erro", "Selecione um usuário com o cursor.")

    def load_user_list(self):
        self.user_listbox.configure(state="normal")
        self.user_listbox.delete("1.0", "end")

        users = self.user_manager.get_all_users()
        for user in users:
            self.user_listbox.insert("end", f"{user}\n")

        self.user_listbox.configure(state="disabled")


    def show_admin_panel(self):
        #ctk.CTkLabel(frame, text=f"Logado como: {self.username}", font=ctk.CTkFont(size=14)).pack(pady=2)

        self.clear_window()

        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Painel Administrativo", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        self.user_listbox = ctk.CTkTextbox(frame, height=180)
        self.user_listbox.pack(pady=10, padx=20, fill="both")

        ctk.CTkButton(frame, text="Ver Estoque do Usuário", command=self.view_selected_inventory).pack(pady=5)
        ctk.CTkButton(frame, text="Ver Histórico do Usuário", command=self.view_selected_history).pack(pady=5)
        ctk.CTkButton(frame, text="Voltar para Login", command=self.logout).pack(pady=15)

        self.load_user_list()


    def show_history(self):
        historico = self.history_manager.listar()
        if not historico:
            messagebox.showinfo("Histórico", "Nenhuma ação registrada ainda.")
            return

        # Janela do histórico
        win = ctk.CTkToplevel(self)
        win.title("Histórico de Ações")
        win.geometry("600x400")
        win.resizable(False, False)

        # Label de título
        title = ctk.CTkLabel(win, text=f"Histórico de ações - {self.username}", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=10)

        # Frame com Scroll
        frame = ctk.CTkFrame(win)
        frame.pack(padx=10, pady=5, fill="both", expand=True)

        scrollbox = ctk.CTkTextbox(frame, wrap="word")
        scrollbox.pack(fill="both", expand=True, padx=5, pady=5)

        if self.is_admin:
            ctk.CTkButton(win, text="Voltar ao Painel Admin", command=win.destroy).pack(pady=5)


        # Preenchendo os dados no Textbox
        for item in historico:
            linha = f"{item['data']} - {item['ação']} {item['produto']}"
            if "quantidade" in item:
                linha += f" (Quantidade: {item['quantidade']})"
            if "novo_nome" in item:
                linha += f" → {item['novo_nome']}"
            scrollbox.insert("end", linha + "\n")

        scrollbox.configure(state="disabled")  # Evita edição


    def logout(self):
        confirm = messagebox.askyesno("Logout", "Deseja sair da sua conta?")
        if confirm:
            self.username = None
            self.product_manager = None
            self.history_manager = None
            self.is_admin = False
            self.show_login()

    def __init__(self):
        super().__init__()
        self.title("Sistema de Estoque")
        self.geometry("1080x920")

        self.user_manager = UserManager()
        self.username = None
        self.product_manager = None
        self.is_admin = False
        self.show_login()

    def show_login(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, corner_radius=20)
        frame.pack(pady=60, padx=60, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Login", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Usuário")
        self.username_entry.pack(pady=10, padx=20)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*")
        self.password_entry.pack(pady=10, padx=20)

        ctk.CTkButton(frame, text="Entrar", command=self.login).pack(pady=15)
        ctk.CTkButton(frame, text="Cadastrar-se", command=self.show_register).pack(pady=5)

    def show_register(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, corner_radius=20)
        frame.pack(pady=60, padx=60, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Cadastro", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Usuário")
        self.username_entry.pack(pady=10, padx=20)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*")
        self.password_entry.pack(pady=10, padx=20)

        ctk.CTkButton(frame, text="Cadastrar", command=self.register).pack(pady=15)
        ctk.CTkButton(frame, text="Voltar", command=self.show_login).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.user_manager.login(username, password):
            self.username = username
            self.is_admin = username == "admin"  # ← Aqui
            self.product_manager = ProductManager(username)
            self.history_manager = HistoryManager(username)

            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            if self.is_admin:
                self.show_admin_panel()
            else:
                self.show_inventory()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")


    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.user_manager.register(username, password):
            messagebox.showinfo("Sucesso", "Cadastro realizado!")
            self.show_login()
        else:
            messagebox.showerror("Erro", "Usuário já existe!")

    def show_inventory(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text=f"Estoque de {self.username}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        self.search_entry = ctk.CTkEntry(frame, placeholder_text="Buscar produto...")
        self.search_entry.pack(pady=5, padx=20, fill="x")
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_products())

        self.product_listbox = ctk.CTkTextbox(frame, height=180)
        self.product_listbox.pack(pady=10, padx=20, fill="both", expand=False)

        self.total_label = ctk.CTkLabel(frame, text="Total de itens: 0")
        self.total_label.pack(pady=5)

        self.product_name_entry = ctk.CTkEntry(frame, placeholder_text="Nome do Produto")
        self.product_name_entry.pack(pady=5, padx=20)

        self.product_qty_entry = ctk.CTkEntry(frame, placeholder_text="Quantidade")
        self.product_qty_entry.pack(pady=5, padx=20)

        ctk.CTkButton(frame, text="Adicionar / Atualizar", command=self.add_or_update_product).pack(pady=8)
        ctk.CTkButton(frame, text="Editar Selecionado", command=self.edit_product_window).pack(pady=5)
        ctk.CTkButton(frame, text="Remover Selecionado", command=self.remove_product).pack(pady=5)
        ctk.CTkButton(frame, text="Logout", fg_color="red", hover_color="#990000", command=self.logout).pack(pady=15)
        ctk.CTkButton(frame, text="Ver Histórico", command=self.show_history).pack(pady=5)

        if self.is_admin:
            ctk.CTkButton(frame, text="Voltar ao Painel Admin", command=self.show_admin_panel).pack(pady=5)

        self.load_products()

    def load_products(self):
        search_term = self.search_entry.get()
        products = self.product_manager.list_products(search_term)
        self.product_listbox.delete("1.0", "end")
        for p in products:
            self.product_listbox.insert("end", f"{p['name']} - Quantidade: {p['quantity']}\n")
        total = self.product_manager.total_quantity()
        self.total_label.configure(text=f"Total de itens: {total}")

    def add_or_update_product(self):
        name = self.product_name_entry.get()
        quantity = self.product_qty_entry.get()

        if name and quantity.isdigit():
            result = self.product_manager.add_product(name, int(quantity))
            msg = "Produto adicionado." if result == "novo" else "Quantidade atualizada."
            messagebox.showinfo("Produto", msg)
            self.product_name_entry.delete(0, "end")
            self.product_qty_entry.delete(0, "end")
            self.load_products()
        else:
            messagebox.showerror("Erro", "Preencha nome e quantidade válidos.")

        if result == "novo":
            self.history_manager.registrar("Adicionou", name, int(quantity))
        else:
            self.history_manager.registrar("Atualizou", name, int(quantity))

    def remove_product(self):
        try:
            selected_line = self.product_listbox.get("insert linestart", "insert lineend")
            product_name = selected_line.split(" - ")[0]
            self.product_manager.remove_product(product_name)
            self.history_manager.registrar("Removeu", product_name)
            self.load_products()
        except:
            messagebox.showerror("Erro", "Selecione um produto com o cursor.")

    def edit_product_window(self):
        try:
            selected_line = self.product_listbox.get("insert linestart", "insert lineend")
            old_name = selected_line.split(" - ")[0]
            old_qty = selected_line.split(": ")[1]
        except:
            messagebox.showerror("Erro", "Selecione um produto com o cursor.")
            return

        win = ctk.CTkToplevel(self)
        win.geometry("300x200")
        win.title("Editar Produto")

        ctk.CTkLabel(win, text="Novo Nome").pack(pady=5)
        new_name_entry = ctk.CTkEntry(win)
        new_name_entry.insert(0, old_name)
        new_name_entry.pack(pady=5)

        ctk.CTkLabel(win, text="Nova Quantidade").pack(pady=5)
        new_qty_entry = ctk.CTkEntry(win)
        new_qty_entry.insert(0, old_qty)
        new_qty_entry.pack(pady=5)

        def save():
            new_name = new_name_entry.get()
            new_qty = new_qty_entry.get()
            if new_name and new_qty.isdigit():
                self.product_manager.edit_product(old_name, new_name, int(new_qty))
                self.history_manager.registrar("Editou", old_name, int(new_qty), novo_nome=new_name)
                self.load_products()
                win.destroy()
            else:
                messagebox.showerror("Erro", "Valores inválidos.")

        ctk.CTkButton(win, text="Salvar", command=save).pack(pady=10)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
