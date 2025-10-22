from os import system
from time import sleep
import dados


def leitura_ingles():
    english = dados.list_englesh()
    system('cls')

    while True:
        system('cls')
        try:
            escolha = int(input('Escolha 1 para escolher o texto e 0 para sair: '))
        except ValueError:
            print('Opção inválida')
            continue

        if escolha == 1:
            print('Textos disponíveis:')
            for i, texto in enumerate(english):
                print(f"{i + 1} - {texto['Titulo']}")
            print('0 - Voltar')

            try:
                opcao = int(input("Escolha o número do texto: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if opcao == 0:
                continue

            if 1 <= opcao <= len(english):
                texto_escolhido = english[opcao - 1]
                print(f"Você escolheu: {texto_escolhido['Titulo']}")
                print("1 - Ler em inglês")
                print("2 - Ler em português")
                print("3 - Ler lado a lado")
                idioma = input("Escolha o modo de leitura: ")
                system('cls')
                print('Carregando texto...')
                sleep(1)
                print(f"Título: {texto_escolhido['Titulo']}\n")
                print(f"Referência: {texto_escolhido['Referencia']}\n")

                for par in texto_escolhido["Paragrafos"]:
                    if idioma == "1":
                        print(par["ingles"], "\n")
                    elif idioma == "2":
                        print(par["portugues"], "\n")
                    elif idioma == "3":
                        print(f"EN: {par['ingles']}\nPT: {par['portugues']}\n")
                    else:
                        print("Opção inválida.")
                        break
                input("Pressione ENTER para voltar.")
                system('cls')
        elif escolha == 0:
            print('Finalizando leitura em inglês...')
            sleep(1)
            break
        else:
            print('Opção inválida.')
            continue


def leitura_espanhol():
    espanha = dados.leitura_espanhol()


    while True:
        
        try:
            escolha = int(input('Escolha 1 para escolher o texto e 0 para sair: '))
        except ValueError:
            print('Opção inválida')
            continue

        if escolha == 1:
            print('Textos disponíveis:')
            for i, texto in enumerate (espanha):
                print(f"{i + 1} - {texto['Titulo']}")
            print('0 - Voltar')

            try:
                opcao = int(input("Escolha o número do texto: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if opcao == 0:
                continue

            if 1 <= opcao <= len(espanha):
                texto_escolhido = espanha[opcao - 1]
                print(f"Você escolheu: {texto_escolhido['Titulo']}")
                print("1 - Ler em espanhol")
                print("2 - Ler em português")
                print("3 - Ler lado a lado")
                idioma = input("Escolha o modo de leitura: ")
                system('cls')
                print('Carregando texto...')
                sleep(1)
                print('Referencia',texto_escolhido['Referencia'])
                for par in texto_escolhido["Paragrafos"]:
                    if idioma == "1":
                        print(par["espanhol"], "\n")
                    elif idioma == "2":
                        print(par["portugues"], "\n")
                    elif idioma == "3":
                        print(f"ES: {par['espanhol']}\nPT: {par['portugues']}\n")
                    else:
                        print("Opção inválida.")
                        break
                input("\nPressione ENTER para voltar.")
                system('cls')
        elif escolha == 0:
            print('Finalizando leitura em espanhol...')
            sleep(1)
            break
        else:
            print('Opção inválida.')
            continue


def leitura_frances():
    franca = dados.leitura_fraça()
    



    while True:
        try:
            escolha = int(input('Escolha 1 para escolher o texto e 0 para sair: '))
        except ValueError:
            print('Opção inválida')
            continue

        if escolha == 1:
            print('Textos disponíveis:')
            for i, texto in enumerate(franca):
                print(f"{i + 1} - {texto['Titulo']}")
            print('0 - Voltar')

            try:
                opcao = int(input("Escolha o número do texto: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if opcao == 0:
                continue

            if 1 <= opcao <= len(franca):
                texto_escolhido = franca[opcao - 1]
                print(f"Você escolheu: {texto_escolhido['Titulo']}")
                print("1 - Ler em francês")
                print("2 - Ler em português")
                print("3 - Ler lado a lado")
                idioma = input("Escolha o modo de leitura: ")
                system('cls')
                print('Carregando texto...')
                sleep(1)
                print(f"Título: {texto_escolhido['Titulo']}\n")
                print(f"Referência: {texto_escolhido['Referencia']}\n")


                for par in texto_escolhido["Paragrafos"]:
                    if idioma == "1":
                        print(par["frances"], "\n")
                    elif idioma == "2":
                        print(par["portugues"], "\n")
                    elif idioma == "3":
                        print(f"FR: {par['frances']}\nPT: {par['portugues']}\n")
                    else:
                        print("Opção inválida.")
                        break
                input("\nPressione ENTER para voltar.")
                system('cls')
        elif escolha == 0:
            print('Finalizando leitura em francês...')
            sleep(1)
            break
        else:
            print('Opção inválida.')
            continue
