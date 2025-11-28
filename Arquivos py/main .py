import tkinter as tk
from tkinter import messagebox
import usuario
import recuperação_senha
import menu_principal
from util import limpar_tela 

BACKGROUND_COLOR = '#1f2833'
FOREGROUND_COLOR = '#ffffff'
BUTTON_COLOR = '#4a536b'
TITLE_FONT = ('Helvetica', 40, 'bold')
BUTTON_FONT = ('Arial', 24)

if 'Usuario' in dir(usuario) and hasattr(usuario.Usuario, 'carregar_usuarios'):
    usuario.Usuario.usuarios = usuario.Usuario.carregar_usuarios()

class OrbitextApp:
    def __init__(self, master):
        self.master = master
        master.title("ORBITEXT - Menu Principal")
        master.configure(bg=BACKGROUND_COLOR)
        
        master.state('zoomed')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, weight=1)
        
        limpar_tela() 

        self.label = tk.Label(
            master, 
            text="ORBITEXT", 
            font=TITLE_FONT,
            bg=BACKGROUND_COLOR, 
            fg='#66fcf1' 
        )
        self.label.grid(row=0, column=0, pady=70, sticky="nsew")

        self.button_frame = tk.Frame(master, bg=BACKGROUND_COLOR)
        self.button_frame.grid(row=1, column=0, pady=20)

        self.login_button = tk.Button(
            self.button_frame, 
            text="Fazer Login", 
            command=self.handle_login, 
            font=BUTTON_FONT, 
            bg=BUTTON_COLOR, 
            fg=FOREGROUND_COLOR, 
            width=20
        )
        self.login_button.pack(pady=15)

        self.cadastro_button = tk.Button(
            self.button_frame, 
            text="Criar Conta", 
            command=self.handle_cadastro, 
            font=BUTTON_FONT, 
            bg=BUTTON_COLOR, 
            fg=FOREGROUND_COLOR, 
            width=20
        )
        self.cadastro_button.pack(pady=15)

        self.recuperacao_button = tk.Button(
            self.button_frame, 
            text="Recuperar Senha", 
            command=self.handle_recuperacao, 
            font=BUTTON_FONT, 
            bg=BUTTON_COLOR, 
            fg=FOREGROUND_COLOR, 
            width=20
        )
        self.recuperacao_button.pack(pady=15)

        self.sair_button = tk.Button(
            self.button_frame, 
            text="Sair", 
            command=master.quit, 
            font=BUTTON_FONT, 
            bg='red', 
            fg=FOREGROUND_COLOR, 
            width=20
        )
        self.sair_button.pack(pady=30)
        
    def menu_inicial(self):
        self.master.deiconify()
        self.master.state('zoomed')

    def handle_cadastro(self):
        limpar_tela()
        print("\n--- INICIANDO CADASTRO NO CONSOLE (INTERAJA NO TERMINAL) ---")
        self.master.withdraw()
        
        try:
            usuario.Usuario.cadastrar_usuario(usuario.Usuario.usuarios)
        except Exception as e:
            print(f"ERRO durante o cadastro: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro durante o cadastro. Verifique o console.")
            
        self.master.deiconify()
        self.master.state('zoomed') 
        messagebox.showinfo("Cadastro", "Processo de cadastro concluído. Verifique o console para a próxima interação.")
        
    def handle_login(self):
        limpar_tela()
        print("\n--- INICIANDO LOGIN NO CONSOLE (INTERAJA NO TERMINAL) ---")
        self.master.withdraw()
        
        try:
            if usuario.Usuario.fazer_login(usuario.Usuario.usuarios):
                # O controle é passado para menu_principal.orbitext() e retorna
                pass
        except Exception as e:
             print(f"ERRO durante o login: {e}")
        
        # Volta para a janela do tkinter após o logout/fim do orbitext()
        self.master.deiconify()
        self.master.state('zoomed')
        
    def handle_recuperacao(self):
        limpar_tela()
        print("\n--- INICIANDO RECUPERAÇÃO DE SENHA NO CONSOLE (INTERAJA NO TERMINAL) ---")
        self.master.withdraw()
        
        try:
            recuperação_senha.Sistema_de_recuperação(usuario.Usuario.usuarios, self.menu_inicial)
        except Exception as e:
            print(f"ERRO durante a recuperação: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro durante a recuperação. Verifique o console.")
            
        self.master.deiconify()
        self.master.state('zoomed')


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = OrbitextApp(root)
        root.mainloop()
    except Exception as e:
        limpar_tela()
        print(f"Erro fatal: {e}")