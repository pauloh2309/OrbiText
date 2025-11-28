from os import system
from time import sleep
import dados
import usuario

def orbitext():
    system('cls')

    while True:
        if not usuario.Usuario.usuario_logado:
            print("Saindo do menu principal: usuário não logado.")
            return

        print('=' * 50)
        print('      🌐 ORBITEXT - MENU PRINCIPAL')
        print('=' * 50)
        print('Escolha uma opção:')
        print(' 1 - Leitura em Outro Idioma')
        print(' 2 - Ver os Rankings')
        print(' 3 - Ver/Gerenciar Seus Parágrafos Salvos') 
        print(' 4 - Ver Parágrafos Públicos dos Outros') 
        print(' 0 - Encerrar o Programa')
        print('=' * 50)
        try:
            numero = int(input("Digite o número para escolher onde você deseja ir: "))
        except ValueError:
            system('cls')
            print('\033[31mERRO: Escolha entre os números definidos (0 a 4).\033[m')
            sleep(1.5)
            continue

        if numero == 1:
            system('cls')
            if hasattr(dados, 'Colocar_jsson') and hasattr(dados.Colocar_jsson, 'mostrar_textos_por_idioma'):
                dados.Colocar_jsson.mostrar_textos_por_idioma()
            else:
                print('\033[31mERRO: Módulo de dados de leitura não disponível.\033[m')
                sleep(2)

        elif numero == 2:
            system('cls')
            if hasattr(dados, 'RankingManager') and hasattr(dados.RankingManager, 'mostrar_rankings'):
                dados.RankingManager.mostrar_rankings()
            else:
                print('\033[31mERRO: Módulo de ranking não disponível.\033[m')
                sleep(2)

        elif numero == 3:
            while True:
                system('cls')
                print('=' * 50)
                print(f"  GERENCIAR PARÁGRAFOS SALVOS - {usuario.Usuario.usuario_logado[0]}")
                print('=' * 50)
                print(' 1 - Ver Meus Parágrafos')
                print(' 2 - Remover Parágrafo Salvo')
                print(' 0 - Voltar ao Menu Principal')
                print('=' * 50)
                
                escolha_gerenciar = input("Escolha a opção (0-2): ").strip()

                if escolha_gerenciar == '1':
                    usuario.Usuario.mostrar_meus_paragrafos(para_remover=False)
                elif escolha_gerenciar == '2':
                    usuario.Usuario.mostrar_meus_paragrafos(para_remover=True)
                elif escolha_gerenciar == '0':
                    system('cls')
                    break
                else:
                    print('\033[31mOpção inválida.\033[m')
                    sleep(1.5)

        elif numero == 4:
            usuario.Usuario.mostrar_paragrafos_publicos()

        elif numero == 0:
            usuario.Usuario.usuario_logado = None
            system('cls')
            print("Saindo do sistema...")
            sleep(1)
            system("cls")
            print("Agradecemos o uso do ORBITEXT!")
            break
        
        else:
            system('cls')
            print('\033[31mOpção inválida.\033[m')
            sleep(1.5)