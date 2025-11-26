from os import system
from time import sleep
import dados

def limpar_tela():
    system('cls')

def pausar():
    input("\nPressione ENTER para continuar...")

def exibir_menu():
    print('=' * 100)
    print('Escolha:')
    print(' 1 - Leitura em outro idioma')
    print(' 2 - Ver rankings')
    print(' 3 - Ver suas palavras marcadas')
    print(' 4 - Ver palavras marcadas dos outros')
    print(' 0 - Encerrar o programa')
    print('=' * 100)

def acao_leitura():
    limpar_tela()
    dados.Colocar_jsson.mostrar_textos_por_idioma()

def acao_rankings():
    limpar_tela()
    print(">>> Sistema de rankings ainda não implementado.")
    pausar()

def acao_palavras_usuario():
    limpar_tela()
    print(">>> Suas palavras marcadas aparecerão aqui.")
    pausar()

def acao_palavras_outros():
    limpar_tela()
    print(">>> Palavras marcadas por outros usuários aparecerão aqui.")
    pausar()

def acao_sair():
    limpar_tela()
    print("Saindo do sistema...")
    sleep(1)
    limpar_tela()
    print("Agradecemos o uso do ORBITEXT")

def orbitext():
    limpar_tela()

    while True:
        exibir_menu()

        try:
            numero = int(input("Digite o número da opção desejada: "))
        except ValueError:
            limpar_tela()
            print("Escolha apenas números válidos!")
            continue

        if numero == 1:
            acao_leitura()

        elif numero == 2:
            acao_rankings()

        elif numero == 3:
            acao_palavras_usuario()

        elif numero == 4:
            acao_palavras_outros()

        elif numero == 0:
            acao_sair()
            break

        else:
            print("Opção inválida.")
            sleep(1)
            limpar_tela()
