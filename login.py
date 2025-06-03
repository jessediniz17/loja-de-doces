# Arquivos para salvar usuários e carrinho
USUARIOS_FILE = "usuarios.json"
CARRINHO_FILE = "carrinho.json"

# Funções para carregar e salvar dados
def carregar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def carregar_carrinho():
    if not os.path.exists(CARRINHO_FILE):
        return {}
    with open(CARRINHO_FILE, "r") as f:
        return json.load(f)

def salvar_carrinho(carrinho):
    with open(CARRINHO_FILE, "w") as f:
        json.dump(carrinho, f, indent=4)

# Classes dos doces e carrinho
class Doce:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

class Carrinho:
    def __init__(self):
        self.itens = {}

    def adicionar(self, doce):
        if doce.nome in self.itens:
            self.itens[doce.nome] += 1
        else:
            self.itens[doce.nome] = 1
        salvar_carrinho(self.itens)

    def calcular_total(self, doces_catalogo):
        total = 0
        for nome, qtd in self.itens.items():
            preco = next((d.preco for d in doces_catalogo if d.nome == nome), 0)
            total += preco * qtd
        return total

    def limpar(self):
        self.itens = {}
        salvar_carrinho(self.itens)

# Tela de login
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loja de Doces - Login")
        self.root.geometry("400x280")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)

        self.usuarios = carregar_usuarios()

        # Frame principal com padding e fundo branco
        self.frame = ttk.Frame(root, padding=25, style="White.TFrame")
        self.frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Título
        self.titulo = ttk.Label(self.frame, text="Bem-vindo(a) à Loja de Doces!", font=("Helvetica", 16, "bold"))
        self.titulo.pack(pady=(0, 15))

        # Entrada usuário
        ttk.Label(self.frame, text="Usuário:", font=("Helvetica", 12)).pack(anchor="w", pady=(5, 0))
        self.entrada_usuario = ttk.Entry(self.frame, font=("Helvetica", 12))
        self.entrada_usuario.pack(fill="x", pady=(0, 10))

        # Entrada senha
        ttk.Label(self.frame, text="Senha:", font=("Helvetica", 12)).pack(anchor="w", pady=(5, 0))
        self.entrada_senha = ttk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.entrada_senha.pack(fill="x", pady=(0, 20))

        # Botões alinhados horizontalmente
        self.frame_botoes = ttk.Frame(self.frame)
        self.frame_botoes.pack(fill="x")

        self.btn_login = ttk.Button(self.frame_botoes, text="Entrar", command=self.verificar_login)
        self.btn_login.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_cadastro = ttk.Button(self.frame_botoes, text="Cadastrar", command=self.abrir_cadastro)
        self.btn_cadastro.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Estilo personalizado
        estilo = ttk.Style()
        estilo.configure("White.TFrame", background="white")
        estilo.configure("TLabel", background="white")
        estilo.configure("TButton", font=("Helvetica", 11, "bold"))

    def verificar_login(self):
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get().strip()
        if usuario in self.usuarios and self.usuarios[usuario] == senha:
            messagebox.showinfo("Sucesso", f"Bem-vindo(a), {usuario}!")
            self.root.destroy()
            abrir_loja()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def abrir_cadastro(self):
        CadastroUsuario(self.root, self)

# Tela de cadastro de usuário
class CadastroUsuario(tk.Toplevel):
    def __init__(self, parent, login_app):
        super().__init__(parent)
        self.title("Cadastro de Usuário")
        self.geometry("400x320")
        self.configure(bg="#f5f5f5")
        self.resizable(False, False)
        self.login_app = login_app

        self.frame = ttk.Frame(self, padding=25, style="White.TFrame")
        self.frame.pack(expand=True, fill="both", padx=30, pady=30)

        ttk.Label(self.frame, text="Novo usuário:", font=("Helvetica", 12)).pack(anchor="w", pady=(5, 0))
        self.entrada_usuario = ttk.Entry(self.frame, font=("Helvetica", 12))
        self.entrada_usuario.pack(fill="x", pady=(0, 10))

        ttk.Label(self.frame, text="Senha:", font=("Helvetica", 12)).pack(anchor="w", pady=(5, 0))
        self.entrada_senha = ttk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.entrada_senha.pack(fill="x", pady=(0, 10))

        ttk.Label(self.frame, text="Confirme a senha:", font=("Helvetica", 12)).pack(anchor="w", pady=(5, 0))
        self.entrada_confirma = ttk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.entrada_confirma.pack(fill="x", pady=(0, 20))

        self.btn_cadastrar = ttk.Button(self.frame, text="Cadastrar", command=self.cadastrar_usuario)
        self.btn_cadastrar.pack(fill="x")

    def cadastrar_usuario(self):
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get().strip()
        confirma = self.entrada_confirma.get().strip()

        if not usuario or not senha or not confirma:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != confirma:
            messagebox.showerror("Erro", "As senhas não conferem.")
            return

        if usuario in self.login_app.usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
            return

        self.login_app.usuarios[usuario] = senha
        salvar_usuarios(self.login_app.usuarios)
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.destroy()

# Tela da loja com lista de doces e carrinho
class LojaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loja de Doces")
        self.root.geometry("550x500")
        self.root.configure(bg="#fafafa")
        self.root.resizable(False, False)

        self.doces = [
            Doce("Brigadeiro", 3.5),
            Doce("Brownie", 5.0),
            Doce("Suspiro", 2.0),
        ]

        self.carrinho = Carrinho()
        self.carrinho.itens = carregar_carrinho()

        # Frame dos produtos
        self.frame_produtos = ttk.Frame(root, padding=20, style="White.TFrame")
        self.frame_produtos.place(relx=0.02, rely=0.02, relwidth=0.46, relheight=0.9)

        ttk.Label(self.frame_produtos, text="Produtos Disponíveis", font=("Helvetica", 16, "bold")).pack(pady=(0,15))

        for doce in self.doces:
            btn = ttk.Button(self.frame_produtos, text=f"{doce.nome} - R$ {doce.preco:.2f}",
                            command=lambda d=doce: self.adicionar_ao_carrinho(d))
            btn.pack(fill="x", pady=7)

        # Frame do carrinho
        self.frame_carrinho = ttk.Frame(root, padding=20, style="White.TFrame")
        self.frame_carrinho.place(relx=0.5, rely=0.02, relwidth=0.48, relheight=0.9)

        ttk.Label(self.frame_carrinho, text="Carrinho", font=("Helvetica", 16, "bold")).pack()

        self.lista_carrinho = tk.Listbox(self.frame_carrinho, font=("Helvetica", 12), height=15)
        self.lista_carrinho.pack(fill="both", expand=True, pady=10)

        self.label_total = ttk.Label(self.frame_carrinho, text=f"Total: R$ {self.carrinho.calcular_total(self.doces):.2f}", font=("Helvetica", 14, "bold"))
        self.label_total.pack(pady=(0, 10))

        frame_botoes = ttk.Frame(self.frame_carrinho)
        frame_botoes.pack(fill="x")

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Carrinho", command=self.limpar_carrinho)
        btn_limpar.pack(side="left", expand=True, fill="x", padx=5)

        btn_finalizar = ttk.Button(frame_botoes, text="Finalizar Compra", command=self.finalizar_compra)
        btn_finalizar.pack(side="right", expand=True, fill="x", padx=5)

        self.atualizar_carrinho()

        estilo = ttk.Style()
        estilo.configure("White.TFrame", background="white")
        estilo.configure("TButton", font=("Helvetica", 12, "bold"))
        estilo.configure("TLabel", background="white")

    def adicionar_ao_carrinho(self, doce):
        self.carrinho.adicionar(doce)
        self.atualizar_carrinho()
        messagebox.showinfo("Item Adicionado", f"{doce.nome} adicionado ao carrinho!")

    def atualizar_carrinho(self):
        self.lista_carrinho.delete(0, tk.END)
        for nome, qtd in self.carrinho.itens.items():
            self.lista_carrinho.insert(tk.END, f"{nome} x{qtd}")
        total = self.carrinho.calcular_total(self.doces)
        self.label_total.config(text=f"Total: R$ {total:.2f}")

    def limpar_carrinho(self):
        self.carrinho.limpar()
        self.atualizar_carrinho()
        messagebox.showinfo("Carrinho", "Carrinho limpo!")

    def finalizar_compra(self):
        FinalizarCompra(self.root, self)

# Janela para finalizar compra
class FinalizarCompra(tk.Toplevel):
    def __init__(self, parent, loja_app):
        super().__init__(parent)
        self.title("Finalizar Compra")
        self.geometry("400x320")
        self.configure(bg="#f5f5f5")
        self.resizable(False, False)
        self.loja_app = loja_app

        self.frame = ttk.Frame(self, padding=25, style="White.TFrame")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(self.frame, text="Itens no Carrinho:", font=("Helvetica", 14, "bold")).pack(anchor="w")

        for nome, qtd in loja_app.carrinho.itens.items():
            preco = next((d.preco for d in loja_app.doces if d.nome == nome), 0)
            ttk.Label(self.frame, text=f"{nome} x{qtd} - R$ {preco * qtd:.2f}", font=("Helvetica", 12)).pack(anchor="w")

        total = loja_app.carrinho.calcular_total(loja_app.doces)
        ttk.Label(self.frame, text=f"\nTotal a pagar: R$ {total:.2f}", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(15,0))

        btn_pagar = ttk.Button(self.frame, text="Confirmar Compra", command=self.confirmar_compra)
        btn_pagar.pack(pady=20, fill="x")

    def confirmar_compra(self):
        messagebox.showinfo("Compra", "Compra finalizada com sucesso!")
        self.loja_app.carrinho.limpar()
        self.loja_app.atualizar_carrinho()
        self.destroy()

# Função para abrir a loja depois do login
def abrir_loja():
    root_loja = tk.Tk()
    app = LojaApp(root_loja)
    root_loja.mainloop()

# Executar o app de login
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()