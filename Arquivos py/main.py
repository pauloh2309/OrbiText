import usuario
import os
import recuperação_senha

os.system('cls')

def menu_inicial():
    os.system('cls')
    print("Voltando ao menu principal")

while True:
    print("\n--- Menu Principal ---")
    print("1 - Cadastre-se")
    print("2 - Fazer login")
    print("3 - Esqueci minha senha")
    print("0 - Sair do programa")

    escolha = input("Digite sua opção: ")
    if escolha == "1":
        usuario.cadastrar_usuario(usuario.usuarios)
        os.system('cls')
    elif escolha == "2":
        usuario.fazer_login(usuario.usuarios)
    elif escolha == "3":
        recuperação_senha.recuperar_senha(usuario.usuarios,menu_inicial)
    elif escolha == "0":
        print("Saindo do programa. Até logo! ")
        break
    else:
        print("Opção inválida. Tente novamente. ")