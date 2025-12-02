import usuario
import recuperação_senha
import menu_principal
from util import limpar_tela 
from time import sleep 

if 'Usuario' in dir(usuario) and hasattr(usuario.Usuario, 'carregar_usuarios'):
    usuario.Usuario.usuarios = usuario.Usuario.carregar_usuarios()

def handle_cadastro():
    limpar_tela()
    print("\n--- INICIANDO CADASTRO (INTERAJA ABAIXO) ---")
    
    try:
        usuario.Usuario.cadastrar_usuario(usuario.Usuario.usuarios)
        print('\033[32mProcesso de cadastro concluído. Retornando ao menu principal...\033[m')
        sleep(2)
    except Exception as e:
        print(f"\033[31mERRO durante o cadastro: {e}\033[m")
        sleep(2)

def handle_login():
    limpar_tela()
    print("\n--- INICIANDO LOGIN (INTERAJA ABAIXO) ---")
    
    try:
        usuario.Usuario.fazer_login(usuario.Usuario.usuarios)
    except Exception as e:
         print(f"\033[31mERRO durante o login: {e}\033[m")
         sleep(2)

def handle_recuperacao():
    limpar_tela()
    print("\n--- INICIANDO RECUPERAÇÃO DE SENHA (INTERAJA ABAIXO) ---")
    
    try:
        recuperação_senha.Recuperar_Senha(usuario.Usuario.usuarios, main_console).menu_principal()
    except Exception as e:
        print(f"\033[31mERRO durante a recuperação: {e}\033[m")
        sleep(2)

def handle_remover_usuario():
    if usuario.Usuario.remover_usuario(usuario.Usuario.usuarios):
        usuario.Usuario.usuarios = usuario.Usuario.carregar_usuarios()
        
def main_console():
    limpar_tela()
    
    while True:
        print('=' * 50)
        print('      🌐 ORBITEXT - MENU PRINCIPAL (CONSOLE)')
        print('=' * 50)
        print('Escolha uma opção:')
        print(' 1 - Fazer Login')
        print(' 2 - Criar Conta')
        print(' 3 - Recuperar Senha')
        print(' 4 - Excluir Conta (Remoção de Usuário)') 
        print(' 0 - Sair do Programa')
        print('=' * 50)
        
        opcao = input("Digite o número para escolher onde você deseja ir: ").strip()
        
        if opcao == '1':
            handle_login()
            limpar_tela()
        elif opcao == '2':
            handle_cadastro()
            limpar_tela()
        elif opcao == '3':
            handle_recuperacao()
            limpar_tela()
        elif opcao == '4':
            handle_remover_usuario()
            limpar_tela()
        elif opcao == '0':
            print("Saindo do programa...")
            limpar_tela()
            break
        else:
            print('\033[31mOpção inválida.\033[m')
            sleep(1.5)
            limpar_tela()

if __name__ == '__main__':
    main_console()