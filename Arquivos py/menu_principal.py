from os import system


english = [
    {
        'Titulo': '',
        'Paragrafos': [
            {
                'ingles': '',
                'portugues': ''
            },
            {
                'ingles': '',
                'portugues': ''
            }
        ]
    }
]


espanha = [
    {
        'Titulo': '',
        'Paragrafos': [
            {
                'espanhol': '',
                'portugues': ''
            },
            {
                'espanhol': '',
                'portugues': ''
            }
        ]
    }
]


franca = [
    {
        'Titulo': '',
        'Paragrafos': [
            {
                'frances': '',
                'portugues': ''
            },
            {
                'frances': "",
                'portugues': ''
            }
        ]
    }
]
system('cls')

while True:
    try:
        escolha = int(input('Escolha 1 para escolher o texto e 0 para sair: '))
    except ValueError:
        print('Opção inválida')
        continue

    if escolha == 1:
        print('Textos disponíveis:')
        for i, texto in enumerate(english):
            print(f"{i+1} - {texto['Titulo']}")
        print('0 - Voltar')

        try:
            opcao = int(input("Escolha o número do texto: "))
        except ValueError:
            print("Opção inválida.")
            continue

        if opcao == 0:
            continue

        if opcao <= 1 <= len(texto):
            texto_escolhide = texto(opcao - 1)
            print(f"Você escolheu: {texto_escolhide['titulo']}")
            print("1 - Ler em inglês")
            print("2 - Ler em português")
            print("3 - Ler lado a lado")
            idioma = input("Escolha o modo de leitura: ")
            for par in texto_escolhide["paragrafos"]:
                if idioma == "1":
                    print(par["en"], "\n")
                elif idioma == "2":
                    print(par["pt"], "\n")
                elif idioma == "3":
                    print(f"EN: {par['en']}\nPT: {par['pt']}\n")
                else:
                    print("Opção inválida.")
                    break

    elif opcao == 0:
        break
    else:
         print('opção invalida')
         continue
    




while True:
    try:
        escolha = int(input('Escolha 1 para escolher o texto e 0 para sair: '))
    except ValueError:
        print('Opção inválida')
        continue

    if escolha == 1:
        print('Textos disponíveis:')
        for i, texto in enumerate(espanha):
            print(f"{i+1} - {texto['Titulo']}")
        print('0 - Voltar')

        try:
            opcao = int(input("Escolha o número do texto: "))
        except ValueError:
            print("Opção inválida.")
            continue

        if opcao == 0:
            continue

        if opcao <= 1 <= len(texto):
            texto_escolhide = texto(opcao - 1)
            print(f"Você escolheu: {texto_escolhide['titulo']}")
            print("1 - Ler em espanhol")
            print("2 - Ler em português")
            print("3 - Ler lado a lado")
            idioma = input("Escolha o modo de leitura: ")
            for par in texto_escolhide["paragrafos"]:
                if idioma == "1":
                    print(par["es"], "\n")
                elif idioma == "2":
                    print(par["pt"], "\n")
                elif idioma == "3":
                    print(f"EN: {par['es']}\nPT: {par['pt']}\n")
                else:
                    print("Opção inválida.")
                    break

    elif opcao == 0:
        break
    else:
         print('opção invalida')
         continue
    



while True:
    try:
        escolha = int(input('Escolha 1 para escolher o texto e 0 para sair: '))
    except ValueError:
        print('Opção inválida')
        continue

    if escolha == 1:
        print('Textos disponíveis:')
        for i, texto in enumerate(franca):
            print(f"{i+1} - {texto['Titulo']}")
        print('0 - Voltar')

        try:
            opcao = int(input("Escolha o número do texto: "))
        except ValueError:
            print("Opção inválida.")
            continue

        if opcao == 0:
            continue

        if opcao <= 1 <= len(texto):
            texto_escolhide = texto(opcao - 1)
            print(f"Você escolheu: {texto_escolhide['titulo']}")
            print("1 - Ler em fraçes")
            print("2 - Ler em português")
            print("3 - Ler lado a lado")
            idioma = input("Escolha o modo de leitura: ")
            for par in texto_escolhide["paragrafos"]:
                if idioma == "1":
                    print(par["fr"], "\n")
                elif idioma == "2":
                    print(par["pt"], "\n")
                elif idioma == "3":
                    print(f"EN: {par['fr']}\nPT: {par['pt']}\n")
                else:
                    print("Opção inválida.")
                    break

    elif opcao == 0:
        break
    else:
         print('opção invalida')
         continue