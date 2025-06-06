import tkinter.ttk as ttk

BRANCO = "#FFFFFF"
ROXO = "#5A2A83"
ROXO_CLARO = "#8B66C9"

def aplicar_estilo(root):
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', background=BRANCO, foreground=ROXO)
    style.configure('TLabel', background=BRANCO, foreground=ROXO, font=('Arial', 11))
    style.configure('TEntry', foreground=ROXO)
    style.configure('TButton', background=ROXO, foreground=BRANCO, font=('Arial', 11, 'bold'))
    style.map('TButton',
              background=[('active', ROXO_CLARO)],
              foreground=[('disabled', '#d9d9d9')])
    style.configure('TRadiobutton', background=BRANCO, foreground=ROXO, font=('Arial', 10))
