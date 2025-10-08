from os import system
from time import sleep 
system('cls')

# 1. Lista Global (temporário)

USUARIOS_CADASTRADOS = [] 

# 2. RF001 - CADASTRO

def cadastrar_usuario():
    """Coleta os dados do usuário e SALVA na lista global."""
    print("\n--- CADASTRO DE NOVO USUÁRIO ---")
    
    # uma pausa para o usuário ler a tela antes de limpar
    # sleep(1) 
    # system('cls')

    nome_usuario = input("Digite o nome de usuário: ").strip()
    
    # Checa se já existe
    if any(u['usuario'] == nome_usuario for u in USUARIOS_CADASTRADOS):
        print(f"\nERRO: O nome de usuário '{nome_usuario}' já existe.")
        sleep(2) # Pausa para o usuário ver o erro
        return

    # Confirmação de senha
    while True:
        senha1 = input("Digite a senha: ")
        senha2 = input("Confirme a senha: ")
        if senha1 == senha2:
            break
        else:
            print("As senhas não coincidem. Tente novamente.")

    # Cria e salva o dicionário
    novo_usuario = {
        'usuario': nome_usuario,
        'senha': senha1 
    }
    USUARIOS_CADASTRADOS.append(novo_usuario)
    
    print(f"\nSUCESSO: Usuário '{nome_usuario}' cadastrado!")
    sleep(2) # Pausa para o usuário ver o sucesso


# RF002 - LOGIN
def fazer_login():
    """Verifica se o usuário e senha correspondem a um registro na lista."""
    print("\n--- LOGIN DE USUÁRIO ---")
    usuario_digitado = input("Usuário: ").strip()
    senha_digitada = input("Senha: ")
    
    # Percorre a lista de usuários cadastrados
    for usuario_registrado in USUARIOS_CADASTRADOS:
        
        # Verifica a correspondência dos dados
        if usuario_registrado['usuario'] == usuario_digitado and \
           usuario_registrado['senha'] == senha_digitada:
            
            print(f"\nSUCESSO: Bem-vindo(a), {usuario_registrado['usuario']}!")
            sleep(2)
            return True, usuario_registrado # Login bem sucedido
            
    # Se o loop terminar sem encontrar nada
    print("\nERRO: Usuário ou senha inválidos.")
    sleep(2)
    return False, None # Login falhou

while True:
    system('cls')
    print("=== ORBITEXT MENU INICIAL ===")
    print("Escolha uma das opções abaixo;")
    print(" 1: Login")
    print(" 2: Cadastre-se")
    print(" 0: Sair")
    
    try:
        opção = int(input("escolha a opção desejada: "))
    except ValueError:
        system('cls')
        print("Escolha apenas os números definidos")
        sleep(1)
        continue
        
    system('cls') # Limpa a tela antes de ir para a próxima ação

    if opção == 1:
        sucesso, usuario = fazer_login() # Chama a função de login
        if sucesso:
            print("\n--- Redirecionando para a Página Principal do ORBITEXT ---")
            break # Quebra o loop do menu inicial

    elif opção == 2:
        cadastrar_usuario() # Chama a função de cadastro
        
    elif opção == 0:
        print("Saindo do sistema...")
        sleep(1)
        system("cls")
        print("Obrigado por usar o ORBITEXT!")
        break
    
    
    elif opção not in [0, 1, 2]:
        print("Opção inválida. Tente novamente.")
        sleep(2) 
        