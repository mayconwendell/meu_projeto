import sqlite3

conn = sqlite3.connect('trabalhos_academicos.db')
cursor = conn.cursor()

def criar_tabelas():
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS trabalhos (
        id_trabalho INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id TEXT NOT NULL,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        curso TEXT NOT NULL,
        data_entrega TEXT NOT NULL,
        orientador TEXT NOT NULL
    )''')
    conn.commit()
def fechar_conexao():
    conn.close()
