from os import system
from time import sleep
import menu_leitura 

def orbitext():
    system('cls')

    while True:
        print('=' * 100)
        print('Escolha:\n 1 para ir para a leitura em outro idioma\n 2 para ver os rankings\n 3 Ver as suas palavras marcadas\n 4 Ver as palavras marcadas dos outros\n 0 para encerrar o programa')
        print('=' * 100)
        try:
            numero = int(input("Digite o número para escolher onde você deseja ir: "))
        except ValueError:
            system('cls')
            print('Escolha entre os números que foram definidos')
            continue

        if numero == 1:
            system('cls')
            print('Escolha o idioma no qual se deseja fazer a leitura')
            while True:
                try:
                    opção_1 = int(input('1 para inglês\n2 para espanhol\n3 para francês\n0 para sair\nEscolha: '))
                except ValueError:
                    print('Opção inválida')
                    continue

                if opção_1 == 1:
                    menu_leitura.leitura_ingles()
                elif opção_1 == 2:
                    menu_leitura.leitura_espanhol()
                elif opção_1 == 3:
                    menu_leitura.leitura_frances()
                elif opção_1 == 0:
                    break
                else:
                    print('Opção inválida')

        elif numero == 2:
            system('cls')
        elif numero == 3:
            system('cls')
        elif numero == 4:
            system('cls')
        elif numero == 0:
            system('cls')
            print("Saindo do sistema...")
            sleep(1)
            system("cls")
            print("Agradecemos o uso do ORBITEXT")
            break
        else:
            print("Opção inválida")