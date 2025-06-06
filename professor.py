import tkinter as tk
from tkinter import ttk, messagebox
from estilo import aplicar_estilo, BRANCO, ROXO
from banco import cursor, conn

def abrir_pagina_professor():
    root = tk.Tk()
    root.title("Página do Professor")
    root.geometry("900x600")
    root.configure(bg=BRANCO)
    aplicar_estilo(root)

    ttk.Label(root, text="Bem-vindo, professor!", font=("Arial", 14)).pack(pady=10)

    campos = ["ID do Aluno", "Título", "Autor", "Curso", "Data de Entrega", "Orientador"]
    entradas = {}

    frame = ttk.Frame(root)
    frame.pack(pady=10, padx=10, fill='x')

    # Cria campos de entrada para dados do trabalho
    for idx, campo in enumerate(campos):
        ttk.Label(frame, text=campo).grid(row=idx, column=0, sticky='e', pady=5)
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=idx, column=1, pady=5)
        entradas[campo] = entry

    tree = ttk.Treeview(root, columns=("ID do Trabalho", "ID do Aluno", "Título", "Autor", "Curso", "Data de Entrega", "Orientador"), show="headings")
    for col in tree['columns']:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=120)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    # Faz uma rolagem vertical para a tabela
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Lista os trabalhos na tabela
    def listar():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM trabalhos")
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)

    # Limpa os campos de entrada
    def limpar():
        for campo in campos:
            entradas[campo].delete(0, tk.END)

    # Atualiza os campos com o trabalho selecionado na tabela
    def selecionar(event):
        selecionado = tree.selection()
        if selecionado:
            item = tree.item(selecionado)
            valores = item['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, valores[i+1])

    # Edita o trabalho selecionado no banco
    def editar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um trabalho para editar")
            return
        item = tree.item(selecionado)
        id_trabalho = item['values'][0]
        valores = [e.get() for e in entradas.values()]
        cursor.execute("""
            UPDATE trabalhos 
            SET aluno_id=?, titulo=?, autor=?, curso=?, data_entrega=?, orientador=? 
            WHERE id_trabalho=?""", tuple(valores + [id_trabalho]))
        conn.commit()
        listar()
        limpar()

    # Deleta o trabalho selecionado
    def deletar():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um trabalho para deletar")
            return
        item = tree.item(selecionado)
        id_trabalho = item['values'][0]
        cursor.execute("DELETE FROM trabalhos WHERE id_trabalho=?", (id_trabalho,))
        conn.commit()
        listar()
        limpar()

    # Limpa os trabalhos e reinicia os IDs
    def deletar_tudo():
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar todos os trabalhos? Esta ação não pode ser desfeita."):
            cursor.execute("DELETE FROM trabalhos")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='trabalhos'")
            conn.commit()
            listar()
            limpar()
            messagebox.showinfo("Sucesso", "Todos os trabalhos foram deletados e o ID reiniciado.")

    # Gera um relatório em uma nova janela com todos os trabalhos
    def gerar_relatorio():
        cursor.execute("SELECT * FROM trabalhos ORDER BY aluno_id")
        trabalhos = cursor.fetchall()
        if not trabalhos:
            messagebox.showinfo("Relatório", "Nenhum trabalho cadastrado.")
            return

        relatorio_texto = "Relatório de Trabalhos Acadêmicos\n\n"
        for t in trabalhos:
            relatorio_texto += (f"ID Trabalho: {t[0]}, Aluno: {t[1]}, Título: {t[2]}, Autor: {t[3]}, "
                                f"Curso: {t[4]}, Data Entrega: {t[5]}, Orientador: {t[6]}\n")

        popup = tk.Toplevel(root)
        popup.title("Relatório de Trabalhos")
        text = tk.Text(popup, wrap='word', width=100, height=30)
        text.pack(padx=10, pady=10)
        text.insert('1.0', relatorio_texto)
        text.config(state='disabled')

        ttk.Button(popup, text="Fechar", command=popup.destroy).pack(pady=5)

    tree.bind('<<TreeviewSelect>>', selecionar)

    botoes = ttk.Frame(root)
    botoes.pack(pady=10)
    ttk.Button(botoes, text="Editar", command=editar).pack(side='left', padx=5)
    ttk.Button(botoes, text="Deletar", command=deletar).pack(side='left', padx=5)
    ttk.Button(botoes, text="Limpar", command=limpar).pack(side='left', padx=5)
    ttk.Button(botoes, text="Gerar Relatório", command=gerar_relatorio).pack(side='left', padx=5)
    ttk.Button(botoes, text="Deletar Todos", command=deletar_tudo).pack(side='left', padx=5)
    ttk.Button(botoes, text="Sair", command=lambda: (root.destroy(), __import__('login').abrir_login())).pack(side='left', padx=5)

    listar()
    root.mainloop()
