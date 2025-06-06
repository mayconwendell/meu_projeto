import tkinter as tk
from tkinter import ttk, messagebox
from estilo import aplicar_estilo, BRANCO, ROXO
from banco import cursor, conn

def abrir_pagina_estudante(usuario_atual):
    root = tk.Tk()
    root.title("Página do Estudante")
    root.geometry("900x600")
    root.configure(bg=BRANCO)
    aplicar_estilo(root)

    ttk.Label(root, text=f"Bem-vindo, estudante {usuario_atual}!", font=("Arial", 14)).pack(pady=10)

    campos = ["ID do Aluno", "Título", "Autor", "Curso", "Data de Entrega", "Orientador"]
    entradas = {}

    frame = ttk.Frame(root)
    frame.pack(pady=10, padx=10, fill='x')

    for idx, campo in enumerate(campos):
        ttk.Label(frame, text=campo).grid(row=idx, column=0, sticky='e', pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=idx, column=1, pady=5)
        entradas[campo] = entry

    entradas["ID do Aluno"].insert(0, usuario_atual)
    entradas["ID do Aluno"].config(state='readonly')

    tree = ttk.Treeview(root, columns=("ID do Trabalho", "ID do Aluno", "Título", "Autor", "Curso", "Data de Entrega", "Orientador"), show="headings")
    for col in tree['columns']:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=120)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    def listar():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM trabalhos WHERE aluno_id=?", (usuario_atual,))
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)

    def limpar():
        for campo in campos:
            entradas[campo].config(state='normal')
            entradas[campo].delete(0, tk.END)
        entradas["ID do Aluno"].insert(0, usuario_atual)
        entradas["ID do Aluno"].config(state='readonly')

    def selecionar(event):
        selecionado = tree.selection()
        if selecionado:
            item = tree.item(selecionado)
            valores = item['values']
            for i, campo in enumerate(campos):
                entradas[campo].config(state='normal')
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, valores[i+1])
            entradas["ID do Aluno"].config(state='readonly')

    def adicionar():
        valores = [e.get() for e in entradas.values()]
        if "" in valores:
            messagebox.showwarning("Erro", "Preencha todos os campos")
            return
        if valores[0] != usuario_atual:
            messagebox.showerror("Erro", "Você só pode adicionar trabalhos com seu próprio ID")
            return
        cursor.execute("INSERT INTO trabalhos (aluno_id, titulo, autor, curso, data_entrega, orientador) VALUES (?, ?, ?, ?, ?, ?)", tuple(valores))
        conn.commit()
        listar()
        limpar()

    def editar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um trabalho para editar")
            return

        item = tree.item(selecionado)
        id_trabalho = item['values'][0]

        if item['values'][1] != usuario_atual:
            messagebox.showerror("Erro", "Você só pode editar seus próprios trabalhos")
            return

        valores = [entradas[campo].get() for campo in campos]
        if "" in valores:
            messagebox.showwarning("Erro", "Preencha todos os campos")
            return

        cursor.execute("""
            UPDATE trabalhos
            SET titulo=?, autor=?, curso=?, data_entrega=?, orientador=?
            WHERE id_trabalho=? AND aluno_id=?
        """, (valores[1], valores[2], valores[3], valores[4], valores[5], id_trabalho, usuario_atual))
        conn.commit()
        listar()
        limpar()

    def deletar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um trabalho para deletar")
            return
        item = tree.item(selecionado)
        id_trabalho = item['values'][0]
        if item['values'][1] != usuario_atual:
            messagebox.showerror("Erro", "Você só pode deletar seus próprios trabalhos")
            return
        cursor.execute("DELETE FROM trabalhos WHERE id_trabalho=?", (id_trabalho,))
        conn.commit()
        listar()
        limpar()

    tree.bind('<<TreeviewSelect>>', selecionar)

    botoes = ttk.Frame(root)
    botoes.pack(pady=10)
    ttk.Button(botoes, text="Adicionar", command=adicionar).pack(side='left', padx=5)
    ttk.Button(botoes, text="Editar", command=editar).pack(side='left', padx=5)
    ttk.Button(botoes, text="Deletar", command=deletar).pack(side='left', padx=5)
    ttk.Button(botoes, text="Limpar", command=limpar).pack(side='left', padx=5)

    def sair():
        root.destroy()
        import login
        login.abrir_login()

    ttk.Button(botoes, text="Sair", command=sair).pack(side='left', padx=5)

    listar()
    root.mainloop()
