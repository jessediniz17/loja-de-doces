import tkinter as tk
from tkinter import messagebox

# Lista de doces com nome e preço
doces = [
    {"nome": "Brigadeiro", "preco": 3.50},
    {"nome": "Brownie", "preco": 5.00},
    {"nome": "Suspiro", "preco": 2.00}
]

# Variável para armazenar o total do carrinho
total_carrinho = 0.0

def adicionar_ao_carrinho(preco):
    global total_carrinho
    total_carrinho += preco
    label_total.config(text=f"Total no carrinho: R$ {total_carrinho:.2f}")

# Criando a janela principal
janela = tk.Tk()
janela.title("Loja de Doces - Menu")
janela.geometry("300x250")

# Criar um frame para a lista de doces
frame_doces = tk.Frame(janela)
frame_doces.pack(pady=10)

# Para cada doce, criar um label com o nome e preço e um botão para adicionar
for doce in doces:
    frame_item = tk.Frame(frame_doces)
    frame_item.pack(fill="x", padx=10, pady=5)

    label_doce = tk.Label(frame_item, text=f"{doce['nome']} - R$ {doce['preco']:.2f}")
    label_doce.pack(side="left")

    btn_add = tk.Button(frame_item, text="Adicionar", command=lambda p=doce['preco']: adicionar_ao_carrinho(p))
    btn_add.pack(side="right")

# Label para mostrar o total
label_total = tk.Label(janela, text="Total no carrinho: R$ 0.00", font=("Arial", 14))
label_total.pack(pady=20)

# Rodar a janela
janela.mainloop()
