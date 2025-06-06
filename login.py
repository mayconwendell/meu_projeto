import tkinter as tk
from tkinter import ttk, messagebox
from estilo import aplicar_estilo, BRANCO, ROXO, ROXO_CLARO
from banco import cursor, conn
import estudante
import professor

def abrir_login():
    login_window_main = tk.Tk()
    login_window_main.title("Login")
    login_window_main.geometry("400x300")
    login_window_main.minsize(350, 300)
    login_window_main.configure(bg=BRANCO)

    aplicar_estilo(login_window_main)

    ttk.Label(login_window_main, text="* Professores: usuário admin, senha admin\n* Estudantes: usuário 01-05 e senha igual ao usuário", foreground=ROXO).pack(pady=5)

    tipo_var = tk.StringVar(value="Estudante")

    frame = ttk.Frame(login_window_main)
    frame.pack(pady=10)

    ttk.Label(frame, text="Usuário:").grid(row=0, column=0, sticky='e', pady=5)
    usuario_entry = ttk.Entry(frame)
    usuario_entry.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Senha:").grid(row=1, column=0, sticky='e', pady=5)
    senha_entry = ttk.Entry(frame, show="*")
    senha_entry.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Tipo:").grid(row=2, column=0, sticky='e', pady=5)
    tipo_frame = ttk.Frame(frame)
    tipo_frame.grid(row=2, column=1, sticky='w', pady=5)
    ttk.Radiobutton(tipo_frame, text="Estudante", variable=tipo_var, value="Estudante").pack(side='left')
    ttk.Radiobutton(tipo_frame, text="Professor", variable=tipo_var, value="Professor").pack(side='left')

    def login():
        usuario = usuario_entry.get()
        senha = senha_entry.get()
        tipo = tipo_var.get()

        if tipo == "Professor":
            if usuario == "admin" and senha == "admin":
                login_window_main.destroy()
                professor.abrir_pagina_professor()
            else:
                messagebox.showerror("Erro", "Login de professor incorreto")
        else:
            if usuario in ["01", "02", "03", "04", "05"] and senha == usuario:
                # Insere o usuário na tabela, se não existir
                cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, senha, tipo) VALUES (?, ?, ?)", (usuario, senha, tipo))
                conn.commit()
                login_window_main.destroy()
                estudante.abrir_pagina_estudante(usuario)
            else:
                messagebox.showerror("Erro", "Login ou senha de estudante incorretos")

    ttk.Button(login_window_main, text="Entrar", command=login).pack(pady=20)

    login_window_main.mainloop()
