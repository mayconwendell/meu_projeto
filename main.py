from banco import criar_tabelas, fechar_conexao
import login

if __name__ == "__main__":
    criar_tabelas()
    login.abrir_login()
    fechar_conexao()
