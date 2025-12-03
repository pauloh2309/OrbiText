

from os import system
from time import sleep
import dados
import usuario
import menu_leitura
import util
from pathlib import Path

MENU_MAP = {
    '1': 'Ler Textos (Opções de Leitura)',
    '2': 'Gerenciar Textos (Meus Parágrafos)',
    '3': 'Ver Parágrafos Públicos',
    '4': 'Adicionar Texto Personalizado',
    '5': 'Ver Ranks',
    '0': 'Sair'
}



def adicionar_texto_personalizado():
    if not usuario.Usuario.usuario_logado:
        print("\033[31mVocê precisa estar logado para adicionar um texto.\033[m")
        sleep(2)
        return

    util.limpar_tela()
    print('=' * 50)
    print('      ➕ ADICIONAR TEXTO PERSONALIZADO')
    print('=' * 50)
    
    while True:
        print("\nEscolha o idioma original do texto:")
        print(" 1 - Inglês")
        print(" 2 - Francês")
        print(" 3 - Espanhol")
        print(" 0 - Sair")
        print('=' * 50)
        
        escolha_idioma = input("Opção: ").strip()
        
        if escolha_idioma == '0':
            util.limpar_tela()
            return
            
        idioma_key = dados.DataManager.IDIOMAS_MAP.get(escolha_idioma)
        
        if idioma_key:
            idioma_nome = dados.DataManager.IDIOMAS_NOMES.get(idioma_key)
            break
        else:
            print('\033[31mOpção inválida.\033[m')
            sleep(1.5)
            util.limpar_tela()

    util.limpar_tela()
    print('=' * 50)
    print(f'      ADICIONAR PARÁGRAFO EM {idioma_nome.upper()}')
    print('=' * 50)
    
    titulo = input("\nDigite o título do parágrafo (ou 0 para sair): ").strip()
    if titulo == '0':
        util.limpar_tela()
        return
        
    paragrafo_original = ''
    while not paragrafo_original:
        paragrafo_original = input(f"\nEscreva o parágrafo no idioma {idioma_nome} (ou 0 para sair):\n").strip()
        
        if paragrafo_original == '0':
            util.limpar_tela()
            return
            
        if not paragrafo_original:
            print('\033[31mO parágrafo não pode ser vazio.\033[m')
            sleep(1.5)
            
    traducao = input("\nEscreva a tradução em Português do parágrafo:\n").strip()
    
    if not traducao:
        traducao = "[SEM TRADUÇÃO]"

    while True:
        print('\nEscolha a visibilidade do parágrafo:')
        print(' 1 - Público')
        print(' 2 - Privado')
        print(' 0 - Sair (Não salvar)')
        print('=' * 50)

        escolha_visibilidade = input("Opção: ").strip()

        if escolha_visibilidade == '0':
            util.limpar_tela()
            print('\033[33mOperação cancelada. Parágrafo não salvo.\033[m')
            sleep(2)
            return

        if escolha_visibilidade == '1':
            visibilidade = 'publico'
            break
        elif escolha_visibilidade == '2':
            visibilidade = 'privado'
            break
        else:
            print('\033[31mOpção inválida. Digite 1, 2 ou 0.\033[m')
            sleep(1.5)
            
    autor = usuario.Usuario.usuario_logado[0]
    novo_id = dados.DataManager.gerar_novo_id()
    
    novo_paragrafo = {
        "id": novo_id,
        "autor": autor,
        "idioma": idioma_key,
        "texto_original": paragrafo_original,
        "traducao": traducao,
        "titulo": titulo,
        "visibilidade": visibilidade
    }
    
    try:
        salvo_id = dados.DataManager.salvar_paragrafo_publico(
            titulo,
            idioma_key,
            paragrafo_original,
            traducao,
            visibilidade
        )

        if usuario.Usuario.usuario_logado is not None:
            try:
                usuario.Usuario.usuarios
            except Exception:
                usuario.Usuario.usuarios = usuario.Usuario.carregar_usuarios()

            usuario.Usuario.usuario_logado[3].append(salvo_id)
            usuario.Usuario.salvar_usuarios(usuario.Usuario.usuarios)

        util.limpar_tela()
        print('\033[32m✅ Parágrafo adicionado com sucesso!\033[m')
        sleep(2)
    except Exception as e:
        util.limpar_tela()
        print(f'\033[31m❌ Falha ao adicionar o parágrafo: {e}\033[m')
        sleep(2)



def menu_principal():


    
    if not usuario.Usuario.usuario_logado:
        print('\033[31mErro: Não há usuário logado. Retornando ao menu principal.\033[m')
        sleep(2)
        return

    user = usuario.Usuario.usuario_logado[0]
    
    while True:
        util.limpar_tela()
        print('=' * 50)
        print(f'      👤 BEM-VINDO, {user.upper()}! (MENU PRINCIPAL)')
        print('=' * 50)
        print('Escolha uma opção:')
        
      
        for num, desc in MENU_MAP.items():
            if num != '0':
                print(f" {num} - {desc}")
        print(f" 0 - {MENU_MAP['0']}")
        print('=' * 50)
        
        escolha = input("Digite o número para escolher onde você deseja ir: ").strip()
        
        if not escolha.isdigit():
            print('\033[31mOpção inválida.\033[m')
            sleep(1.5)
            continue
            
        try:
            numero = int(escolha)
            
            if numero == 1:
                menu_leitura.menu_leitura_idioma()

                
            elif numero == 2: 
                while True:
                    util.limpar_tela()
                    print('=' * 50)
                    print('      📝 GERENCIAR MEUS TEXTOS')
                    print('=' * 50)
                    print(' 1 - Ver/Expandir meus parágrafos salvos')
                    print(' 2 - Remover parágrafos salvos')
                    print(' 0 - Voltar ao Menu Principal')
                    print('=' * 50)
                    
                    escolha_gerenciar = input("Escolha a opção (0-2): ").strip()

                    if escolha_gerenciar == '1':
                        usuario.Usuario.mostrar_meus_paragrafos(para_remover=False)
                    elif escolha_gerenciar == '2':
                        usuario.Usuario.mostrar_meus_paragrafos(para_remover=True)
                    elif escolha_gerenciar == '0':
                        util.limpar_tela()
                        break
                    else:
                        print('\033[31mOpção inválida.\033[m')
                        sleep(1.5)

            elif numero == 3: 
                usuario.Usuario.mostrar_paragrafos_publicos()

            elif numero == 4:
                while True:
                    util.limpar_tela()
                    print('=' * 50)
                    print('      ➕ ADICIONAR / REGISTRAR TEXTOS')
                    print('=' * 50)
                    print(' 1 - Adicionar Parágrafo Personalizado (rápido)')
                    print(' 2 - Registrar Texto Completo (salva em textos_idiomas.json)')
                    print(' 0 - Voltar')
                    print('=' * 50)
                    sub = input('Opção: ').strip()
                    if sub == '1':
                        adicionar_texto_personalizado()
                        break
                    elif sub == '2':
                        try:
                            menu_leitura.criar_e_salvar_novo_texto()
                        except Exception as e:
                            print(f"\033[31mErro ao abrir registro de texto: {e}\033[m")
                            sleep(1.5)
                        break
                    elif sub == '0':
                        break
                    else:
                        print('\033[31mOpção inválida.\033[m')
                        sleep(1)

            elif numero == 5:
                dados.DataManager.mostrar_rankings_gerais()

            elif numero == 0:
                usuario.Usuario.usuario_logado = None
                util.limpar_tela()
                print("Saindo do sistema...")
                sleep(1)
                util.limpar_tela()
                print("Agradecemos o uso...")
                sleep(1)
                return

            else:
                print('\033[31mOpção inválida.\033[m')
                sleep(1.5)
                util.limpar_tela()
        
        except ValueError:
            print('\033[31mOpção inválida. Por favor, digite um número.\033[m')
            sleep(1.5)