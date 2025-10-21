import verificação

while True:
    print("\n--- Menu Principal ---")
    print("1 - Cadastre-se")
    print("2 - Fazer login")
    print("3 - Recuperar senha")
    print("0 - Sair do programa")

    escolha = input("Digite sua opção: ")
    if escolha == "1":
        verificação.cadastrar_usuario(verificação.usuarios)
    elif escolha == "2":
        verificação.fazer_login(verificação.usuarios)
    elif escolha == "0":
        verificação.salvar_usuarios(verificação.usuarios)
        print("Saindo do programa. Até logo! ")
        break
    else:
        print("Opção inválida. Tente novamente. ")