import tkinter as tk
from tkinter import messagebox
import usuario
import recuperação_senha
import menu_principal1
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
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=150, pady=30)
        
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        options = [
            ("1 - Cadastre-se", self.handle_cadastro),
            ("2 - Fazer login", self.handle_login),
            ("3 - Esqueci minha senha", self.handle_recuperacao),
            ("0 - Sair do programa", master.quit)
        ]

        for i, (text, command) in enumerate(options):
            self.button_frame.grid_rowconfigure(i, weight=1)
            btn = tk.Button(
                self.button_frame, 
                text=text, 
                command=command, 
                font=BUTTON_FONT,
                bg=BUTTON_COLOR,
                fg=FOREGROUND_COLOR,
                activebackground=BACKGROUND_COLOR, 
                activeforeground=FOREGROUND_COLOR,
                relief=tk.RAISED, 
                bd=5 
            )
            btn.grid(row=i, column=0, pady=15, padx=80, sticky="ew")

    def menu_inicial(self):
        limpar_tela()
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
                pass
        except Exception as e:
             print(f"ERRO durante o login: {e}")
        
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
        
        
def main():
    root = tk.Tk()
    app = OrbitextApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()