from os import system
from time import sleep
import textos

def limpar_tela():
    system('cls')


def escolher_opcao(msg):
    """Lê um número e trata erro."""
    try:
        return int(input(msg))
    except ValueError:
        print("Opção inválida.")
        return None


def listar_textos(lista):
    """Exibe os títulos dos textos."""
    print("Textos disponíveis:")
    for i, texto in enumerate(lista):
        print(f"{i + 1} - {texto['Titulo']}")
    print("0 - Voltar")


def exibir_texto(texto, idioma):
    """Exibe o texto conforme o idioma escolhido."""
    limpar_tela()
    print('Carregando texto...')
    sleep(1)

    print(f"Título: {texto['Titulo']}\n")
    print(f"Referência: {texto['Referencia']}\n")

    for par in texto["Paragrafos"]:
        if idioma == "1":
            print(par[list(par.keys())[0]], "\n")
        elif idioma == "2":
            print(par["portugues"], "\n")
        elif idioma == "3":
            keys = list(par.keys())
            origem = keys[0]  
            print(f"{origem.upper()}: {par[origem]}\nPT: {par['portugues']}\n")
        else:
            print("Opção inválida.")
            return

    input("Pressione ENTER para voltar.")
    limpar_tela()

def escolher_modo_leitura(texto):
    """Escolhe como ler (inglês/espanhol/francês, português, lado a lado)."""
    print("1 - Ler no idioma original")
    print("2 - Ler em português")
    print("3 - Ler lado a lado")
    return input("Escolha o modo de leitura: ")

def leitura_generica(lista_textos, nome_idioma):
    limpar_tela()

    while True:
        escolha = escolher_opcao("Escolha 1 para escolher o texto e 0 para sair: ")
        if escolha is None:
            continue

        if escolha == 0:
            print(f"Finalizando leitura em {nome_idioma}...")
            sleep(1)
            break

        if escolha == 1:
            listar_textos(lista_textos)

            opcao = escolher_opcao("Escolha o número do texto: ")
            if opcao is None:
                continue

            if opcao == 0:
                continue

            if 1 <= opcao <= len(lista_textos):
                texto_escolhido = lista_textos[opcao - 1]

                print(f"Você escolheu: {texto_escolhido['Titulo']}")
                idioma = escolher_modo_leitura(texto_escolhido)

                exibir_texto(texto_escolhido, idioma)

            else:
                print("Opção inválida.")
        else:
            print("Opção inválida.")

def leitura_ingles():
    lista = textos.list_englesh()
    leitura_generica(lista, "inglês")

def leitura_espanhol():
    lista = textos.leitura_espanhol()
    leitura_generica(lista, "espanhol")

def leitura_frances():
    lista = textos.leitura_fraça()
    leitura_generica(lista, "francês")
