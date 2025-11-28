import json
from os import path
from time import sleep
from os import system
import usuario

NOME_ARQUIVO = 'textos_idiomas.json'

class RankingManager:
    @staticmethod
    def mostrar_rankings():
        system('cls')
        print('=' * 50)
        print('      🏆 ORBITEXT - RANKING GERAL DE LEITORES 🏆')
        print('=' * 50)
        print('Abaixo está uma simulação de leitores com maior pontuação:')
        print('-' * 50)
        rankings_simulados = [
            (1, 'Alice', 1500),
            (2, 'Bob', 1200),
            (3, 'Charlie', 900)
        ]
        print(f"{'POS':<5}{'NOME':<30}{'PONTOS':>10}")
        print('-' * 50)
        for pos, nome, pontos in rankings_simulados:
            print(f"{pos:<5}{nome:<30}{pontos:>10}")
        print('-' * 50)
        input("Pressione ENTER para voltar ao Menu Principal...")
        system('cls')
        

class Colocar_jsson: 
    @staticmethod
    def carregar_textos_por_idioma():
        try:
            with open(NOME_ARQUIVO, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Aviso: Arquivo JSON corrompido ou vazio. Iniciando com dados vazios.")
            return {}

    @staticmethod
    def salvar_textos_por_idioma(textos):
        try:
            with open(NOME_ARQUIVO, 'w', encoding='utf-8') as arquivo:
                json.dump(textos, arquivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"ERRO ao salvar textos: {e}")
            
    @staticmethod
    def mostrar_textos_por_idioma():
        textos_por_idioma = Colocar_jsson.carregar_textos_por_idioma()
        
        while True:
            system('cls')
            print('=' * 50)
            print('          LEITURA EM OUTRO IDIOMA')
            print('=' * 50)
            
            idiomas = list(textos_por_idioma.keys())
            if not idiomas:
                print("Nenhum texto disponível para leitura.")
                input("Pressione ENTER para voltar...")
                break

            for i, idioma in enumerate(idiomas):
                print(f" {i+1} - {idioma}")
            print(" 0 - Voltar ao Menu Principal")
            print('=' * 50)

            try:
                escolha_idioma = int(input("Escolha o idioma (0-{}): ".format(len(idiomas))))
            except ValueError:
                system('cls')
                print('\033[31mERRO: Escolha entre os números definidos.\033[m')
                sleep(1.5)
                continue

            if escolha_idioma == 0:
                break
            
            if 1 <= escolha_idioma <= len(idiomas):
                idioma_selecionado = idiomas[escolha_idioma - 1]
                textos_do_idioma = textos_por_idioma[idioma_selecionado]

                while True:
                    system('cls')
                    print('=' * 50)
                    print(f"      TEXTOS DISPONÍVEIS em {idioma_selecionado}")
                    print('=' * 50)
                    
                    for i, texto in enumerate(textos_do_idioma):
                        print(f" {i+1} - {texto.get('Titulo', 'N/A')} por {texto.get('Autor', 'Autor Desconhecido')}")
                    print(" 0 - Voltar à seleção de idioma")
                    print('=' * 50)

                    try:
                        escolha_texto = int(input("Escolha o texto para ler (0-{}): ".format(len(textos_do_idioma))))
                    except ValueError:
                        system('cls')
                        print('\033[31mERRO: Escolha entre os números definidos.\033[m')
                        sleep(1.5)
                        continue
                    
                    if escolha_texto == 0:
                        break
                    
                    if 1 <= escolha_texto <= len(textos_do_idioma):
                        texto_selecionado = textos_do_idioma[escolha_texto - 1]
                        paragrafos = texto_selecionado.get('Paragrafos', [])
                        
                        while True:
                            system('cls')
                            print('=' * 50)
                            print(f"      LENDO: {texto_selecionado.get('Titulo', 'N/A')}")
                            print('=' * 50)

                            for i, paragrafo in enumerate(paragrafos):
                                texto = paragrafo.get('Lingua', 'N/A')
                                print(f"\n[Parágrafo {i+1}]")
                                print(texto)
                            
                            print('\n' + '=' * 50)
                            print(' 1 - Ver Tradução de um Parágrafo')
                            print(' 2 - Salvar um Parágrafo')
                            print(' 0 - Voltar para a seleção de textos')
                            print('=' * 50)

                            try:
                                escolha_acão = int(input("Escolha uma ação (0-2): "))
                            except ValueError:
                                print('\033[31mERRO: Escolha entre os números definidos.\033[m')
                                sleep(1.5)
                                continue

                            if escolha_acão == 0:
                                break
                            
                            elif escolha_acão == 1:
                                while True:
                                    try:
                                        escolha_paragrafo = int(input(f"Qual parágrafo você deseja ver a tradução? (1-{len(paragrafos)}, 0 para cancelar): "))
                                    except ValueError:
                                        print("\033[31mEntrada inválida. Digite um número.\033[m")
                                        sleep(2)
                                        continue
                                        
                                    if escolha_paragrafo == 0:
                                        break
                                        
                                    if 1 <= escolha_paragrafo <= len(paragrafos):
                                        paragrafo = paragrafos[escolha_paragrafo - 1]
                                        print('\n' + '-' * 50)
                                        print(f"TRADUÇÃO do Parágrafo {escolha_paragrafo}:")
                                        print(paragrafo.get('portugues', 'Tradução não disponível.'))
                                        print('-' * 50)
                                        input("Pressione ENTER para continuar lendo...")
                                        break
                                    else:
                                        print("\033[31mOpção inválida.\033[m")
                                        sleep(1.5)
                            
                            elif escolha_acão == 2:
                                while True:
                                    try:
                                        escolha_paragrafo = int(input(f"Qual parágrafo você deseja salvar? (1-{len(paragrafos)}, 0 para cancelar): "))
                                    except ValueError:
                                        print("\033[31mEntrada inválida. Digite um número.\033[m")
                                        sleep(2)
                                        continue
                                        
                                    if escolha_paragrafo == 0:
                                        break
                                        
                                    if 1 <= escolha_paragrafo <= len(paragrafos):
                                        paragrafo = paragrafos[escolha_paragrafo - 1]
                                        
                                        texto_original = paragrafo.get('Lingua', 'N/A')
                                        traducao = paragrafo.get('portugues', 'N/A')
                                        titulo = texto_selecionado.get('Titulo', 'N/A')

                                        while True:
                                            print("\nDefinir Visibilidade:")
                                            print(" 1 - Público")
                                            print(" 2 - Privado")
                                            print(" 0 - Cancelar Salvamento")
                                            
                                            visibilidade_input = input("Escolha a opção (0-2): ").strip()
                                            
                                            if visibilidade_input == '0':
                                                visibilidade = None
                                                break
                                            elif visibilidade_input == '1':
                                                visibilidade = 'publico'
                                                break
                                            elif visibilidade_input == '2':
                                                visibilidade = 'privado'
                                                break
                                            else:
                                                print("\033[31mOpção inválida. Digite 1, 2 ou 0.\033[m")
                                                sleep(1.5)
                                                
                                        if visibilidade is None:
                                            break
                                                
                                        paragrafo_salvo = usuario.Usuario.salvar_paragrafo(
                                            idioma=idioma_selecionado, 
                                            texto_original=texto_original, 
                                            traducao=traducao,
                                            titulo=titulo,
                                            visibilidade=visibilidade
                                        )
                                        
                                        if paragrafo_salvo:
                                            print('\033[32mParágrafo salvo com sucesso!\033[m')
                                            sleep(2)
                                            break
                                    else:
                                        print("\033[31mOpção inválida.\033[m")
                                        sleep(1.5)
                            else:
                                print("\nOpção de ação inválida.")
                                sleep(1.5)
                                system('cls')
                                continue
                    else:
                        print("\nOpção de texto inválida.")
                        sleep(1.5)
                        system('cls')
                        continue
            else:
                print("\nOpção de idioma inválida.")
                sleep(1.5)
                system('cls')
                continue