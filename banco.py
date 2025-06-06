import sqlite3

conn = sqlite3.connect('trabalhos_academicos.db')

cursor = conn.cursor()

def criar_tabelas():
    # Criação da tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- ID único e auto-incrementável
        usuario TEXT NOT NULL UNIQUE,           -- Nome de usuário, único e obrigatório
        senha TEXT NOT NULL,                    -- Senha do usuário, obrigatória
        tipo TEXT NOT NULL                      -- Tipo de usuário (ex: 'aluno', 'professor'), obrigatório
    )''')

    # Criação da tabela de trabalhos acadêmicos
    cursor.execute('''CREATE TABLE IF NOT EXISTS trabalhos (
        id_trabalho INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único do trabalho
        aluno_id TEXT NOT NULL,                        -- ID do aluno que enviou o trabalho
        titulo TEXT NOT NULL,                          -- Título do trabalho
        autor TEXT NOT NULL,                           -- Nome do autor
        curso TEXT NOT NULL,                           -- Curso relacionado ao trabalho
        data_entrega TEXT NOT NULL,                    -- Data de entrega do trabalho
        orientador TEXT NOT NULL                       -- Nome do orientador do trabalho
    )''')

    conn.commit()

def fechar_conexao():
    conn.close()
