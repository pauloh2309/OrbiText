import verificação
import os

os.system('cls')

while True:
    print("\n--- Menu Principal ---")
    print("1 - Cadastre-se")
    print("2 - Fazer login")
    print("0 - Sair do programa")

    escolha = input("Digite sua opção: ")
    if escolha == "1":
        verificação.cadastrar_usuario(verificação.usuarios)
        os.system('cls')
    elif escolha == "2":
        verificação.fazer_login(verificação.usuarios)
    elif escolha == "0":
        print("Saindo do programa. Até logo! ")
        break
    else:
        print("Opção inválida. Tente novamente. ")