import json
from os import system
from time import sleep
import re
import menu_principal
import verificação
import maskpass
import util
from pathlib import Path
import dados 

ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_PUBLICOS = 'paragrafos_publicos.json'

class Usuario:
    
    usuario_logado = None 
    XP_BASE = 100
    FATOR_XP = 1.5
    
    NIVEIS_IDIOMA = {
        1: '🐇', 2: '🦊', 3: '🐺', 4: '🐻', 5: '🦅',
        6: '🐴', 7: '🐘', 8: '🐅', 9: '🦁', 10: '🦏'
    }

    NIVEIS_GERAL = {
        1: '🧚', 2: '🗿', 3: '👁️', 4: '🦅', 5: '🧐',
        6: '🦄', 7: '🐂', 8: '🔥', 9: '🐲', 10: '🌊'
    }

    @staticmethod
    def obter_emoji_nivel(nivel, tipo='geral'):
        if tipo == 'geral':
            emojis = Usuario.NIVEIS_GERAL
        else:
            emojis = Usuario.NIVEIS_IDIOMA

        if nivel in emojis and nivel <= 10:
            return emojis[nivel]
        elif nivel > 10:
            return emojis[10] 
        return '❓'
        
    @staticmethod
    def calcular_nivel(xp_total):
        nivel = 1
        xp_necessario = Usuario.XP_BASE
        while xp_total >= xp_necessario:
            xp_total -= xp_necessario
            nivel += 1
            xp_necessario = int(Usuario.XP_BASE * (Usuario.FATOR_XP ** (nivel - 1)))
        return nivel
    
    @staticmethod
    def carregar_usuarios():

        if Path(ARQUIVO_USUARIOS).exists():
            with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    @staticmethod
    def salvar_usuarios(usuarios):
        with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _encontrar_usuario(usuarios, nome_ou_email):
        """Procura um usuário pelo nome ou email (case-insensitive)."""
        nome_ou_email = nome_ou_email.strip().lower()
        for i, user in enumerate(usuarios):
            nome_existente = user[0].lower()
            email_existente = user[2].lower() if len(user) > 2 and user[2] else None
            
            if nome_existente == nome_ou_email:
                return i, user 
            if email_existente and email_existente == nome_ou_email:
                return i, user 
        return -1, None

    @staticmethod
    def _usuario_existe(usuarios, nome_ou_email, check_email_only=False):
        """Verifica se nome ou email já existe (para cadastro)."""
        nome_ou_email = nome_ou_email.strip().lower()

        for user in usuarios:
            nome_existente = user[0].lower()
            email_existente = user[2].lower() if len(user) > 2 and user[2] else None

            if not check_email_only and nome_existente == nome_ou_email:
                return True, 'Nome de usuário'
            if email_existente == nome_ou_email:
                return True, 'E-mail'
        return False, None
    
    @staticmethod
    def cadastrar_usuario(usuarios):
        util.limpar_tela()
        print('=' * 50)
        print('      ✍️  NOVO REGISTRO (CONTA)')
        print('=' * 50)

        tentativas_nome = 0
        nome_usuario = ""
        while tentativas_nome < 3:
            nome_usuario = input("Digite o nome de usuário (será usado para login): ").strip()
            if not nome_usuario:
                print('\033[31mErro: Nome de usuário não pode estar vazio.\033[m')
                tentativas_nome += 1
                sleep(1.5)
                continue

            existe, tipo = Usuario._usuario_existe(usuarios, nome_usuario)
            if existe and tipo == 'Nome de usuário':
                print(f'\033[31mErro: O {tipo} "{nome_usuario}" já está cadastrado. Tente outro.\033[m')
                tentativas_nome += 1
                sleep(1.5)
            else:
                break
        
        if tentativas_nome == 3:
            print('\033[31mNúmero máximo de tentativas excedido para o nome de usuário. Voltando ao Menu Principal.\033[m')
            sleep(2)
            return False

        tentativas_email = 0
        email_usuario = ""
        while tentativas_email < 3:
            email_usuario = input("Digite o seu e-mail (usado para recuperação de senha): ").strip()
            
            if not verificação.Verificar_dados.validar_email(email_usuario):
                print('\033[31mErro: O e-mail digitado não é válido. Verifique o formato e o domínio.\033[m')
                tentativas_email += 1
                sleep(1.5)
                continue

            
            existe, tipo = Usuario._usuario_existe(usuarios, email_usuario, check_email_only=True)
            if existe and tipo == 'E-mail':
                
                print(f'\033[31mErro: O {tipo} "{email_usuario}" já está cadastrado. Tente outro.\033[m')
                tentativas_email += 1
                sleep(1.5)
            else:
                break

        if tentativas_email == 3:
            print('\033[31mNúmero máximo de tentativas excedido para o e-mail. Voltando ao Menu Principal.\033[m')
            sleep(2)
            return False

        tentativas_senha = 0
        senha_usuario = ""
        while tentativas_senha < 3:
            print('Digite sua senha (Mínimo de 8 e máximo de 12 caracteres, com letra maiúscula, minúscula, número e caracteres especiais): ')
            senha_usuario = maskpass.askpass(prompt='Senha: ', mask='*').strip()

            if verificação.Verificar_dados.verificar_senha(senha_usuario): 
                conf_senha = maskpass.askpass(prompt='Confirme a senha: ', mask='*').strip()
                
                if conf_senha == senha_usuario:
                    break 
                else:
                    print('\033[31mErro: A Senha de confirmação não confere. Por favor, digite a senha novamente.\033[m')
                    tentativas_senha += 1 
                    sleep(2)
            else:
                tentativas_senha += 1
                sleep(1) 
                
        if tentativas_senha == 3:
            print('\033[31mNúmero máximo de tentativas excedido para a senha. Voltando ao Menu Principal.\033[m')
            sleep(2)
            return False
        novo_usuario = [nome_usuario, senha_usuario, email_usuario, [], 1, 0] 
        usuarios.append(novo_usuario)
        Usuario.salvar_usuarios(usuarios)
        
        print(f'\n\033[32mUsuário "{nome_usuario}" cadastrado com sucesso! Retornando ao Menu Principal.\\033[m')
        sleep(2)
        return True

    @staticmethod
    def fazer_login(usuarios):
        util.limpar_tela()
        print('=' * 50)
        print('      🔑 LOGIN (CONTA EXISTENTE)')
        print('=' * 50)
        tentativas_nome_email = 0
        indice_usuario = -1
        dados_usuario = None
        while tentativas_nome_email < 3:
            nome_ou_email = input("Digite o nome de usuário ou e-mail: ").strip()
            
            if not nome_ou_email:
                print('\033[31mErro: Nome de usuário ou e-mail não pode estar vazio.\033[m')
                tentativas_nome_email += 1
                sleep(1.5)
                continue
                
            indice_usuario, dados_usuario = Usuario._encontrar_usuario(usuarios, nome_ou_email)
            
            if indice_usuario == -1:
                print('\033[31mErro: Nome de usuário ou e-mail NÃO cadastrado ou não encontrado. Tente novamente.\033[m')
                tentativas_nome_email += 1
                sleep(1.5)
            else:
                break 
                
        if tentativas_nome_email == 3:
            print('\033[31mNúmero máximo de tentativas excedido para nome/e-mail. Voltando ao Menu Principal.\033[m')
            sleep(2)
            return False

        tentativas_senha = 0
        while tentativas_senha < 3:
            senha_input = maskpass.askpass(prompt='Senha: ', mask='*').strip()
            
            senha_correta = dados_usuario[1] 
            
            if senha_input == senha_correta:
                Usuario.usuario_logado = dados_usuario
                util.limpar_tela()
                print(f'\n\033[32mBem-vindo(a), {dados_usuario[0]}! Login realizado com sucesso.\033[m')
                sleep(2)
                menu_principal.menu_principal()
                return True
            else:
                print('\033[31mErro: Senha incorreta. Tente novamente.\033[m')
                tentativas_senha += 1
                sleep(1.5)
        print('\033[31mNúmero máximo de tentativas excedido para a senha. Voltando ao Menu Principal.\\033[m')
        sleep(2)
        return False
    

    @staticmethod
    def carregar_paragrafos_publicos():
        if Path(ARQUIVO_PUBLICOS).exists():
            with open(ARQUIVO_PUBLICOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    @staticmethod
    def mostrar_paragrafos_publicos():
        paragrafos_publicos = Usuario.carregar_paragrafos_publicos()
        
        titulo_sec = '      📝 PARÁGRAFOS PÚBLICOS'
        util.limpar_tela()
        print('=' * 50)
        print(titulo_sec)
        print('=' * 50)
        
        if not paragrafos_publicos:
            print('\033[33mNenhum parágrafo público disponível no momento.\033[m')
            sleep(2)
            return

        print(f"{'#':<4} | {'IDIOMA':<10} | {'TÍTULO':<30} | {'AUTOR':<15} | TEXTO (SNIPPET)")
        print('-' * 90)
        for i, p in enumerate(paragrafos_publicos):
            texto_snippet = p['texto_original'][:40] + '...' if len(p['texto_original']) > 40 else p['texto_original']
            autor_display = p.get('autor', 'Desconhecido')
            print(f"{i+1:<4} | {p['idioma']:<10} | {p['titulo']:<30} | {autor_display:<15} | {texto_snippet}")
        print('-' * 90)

        while True:
            try:
                escolha = input("Digite o número do parágrafo para EXPANDIR/VER DETALHES (0 para voltar): ").strip()
                if escolha.lower() == '0':
                    break
                
                indice = int(escolha) - 1
                if 0 <= indice < len(paragrafos_publicos):
                    Usuario.expandir_paragrafo(paragrafos_publicos[indice], origem=titulo_sec.strip())
                    util.limpar_tela()
                    
                    print('=' * 50)
                    print(titulo_sec)
                    print('=' * 50)
                    print(f"{'#':<4} | {'IDIOMA':<10} | {'TÍTULO':<30} | {'AUTOR':<15} | TEXTO (SNIPPET)")
                    print('-' * 90)
                    for i, p in enumerate(paragrafos_publicos):
                        texto_snippet = p['texto_original'][:40] + '...' if len(p['texto_original']) > 40 else p['texto_original']
                        autor_display = p.get('autor', 'Desconhecido')
                        print(f"{i+1:<4} | {p['idioma']:<10} | {p['titulo']:<30} | {autor_display:<15} | {texto_snippet}")
                    print('-' * 90)
                    
                else:
                    print('\033[31mOpção inválida. Digite um número da lista ou 0 para voltar.\033[m')
                    sleep(1.5)
            except ValueError:
                print('\033[31mOpção inválida. Digite apenas números.\033[m')
                sleep(1.5)

    @staticmethod
    def expandir_paragrafo(paragrafo, origem=""):
        util.limpar_tela()
        print('=' * 50)
        print(f"      EXPANDINDO: {paragrafo['titulo'].upper()}")
        if origem:
             print(f"      (Origem: {origem})")
        print('=' * 50)
        
        print(f"\033[34mAutor: {paragrafo.get('autor', 'Desconhecido')}\033[m")
        print(f"\033[34mIdioma: {paragrafo['idioma'].capitalize()}\033[m")
        print("-" * 50)
        
        print("\n\033[33m--- Texto Original ---\033[m")
        print(paragrafo['texto_original'])
        
        print("\n\033[33m--- Tradução (Português) ---\033[m")
        print(paragrafo['traducao'])
        
        print("-" * 50)
        input("Pressione ENTER para voltar...")
        
    @staticmethod
    def remover_texto_do_usuario(texto_id):
        if not Usuario.usuario_logado:
            print("\033[31mErro: Nenhum usuário logado.\033[m")
            sleep(1)
            return

        autor = Usuario.usuario_logado[0]
        
        sucesso = dados.DataManager.remover_texto_personalizado(texto_id, autor)
        
        if sucesso:
            print('\033[32mTexto removido com sucesso!\033[m')
        else:
            print('\033[31mErro: Não foi possível remover o texto. Talvez ele não exista ou você não seja o autor.\033[m')
        
        sleep(2)
        util.limpar_tela()

    @staticmethod
    def mostrar_meus_paragrafos(para_remover=False):
        util.limpar_tela()
        if not Usuario.usuario_logado:
            print("\033[31mVocê precisa estar logado para ver seus textos.\033[m")
            sleep(2)
            return

        nome_usuario = Usuario.usuario_logado[0]
        ids_proprios = Usuario.usuario_logado[3] 

        if not ids_proprios:
            print('=' * 50)
            print(f"      📝 MEUS TEXTOS ({nome_usuario})")
            print('=' * 50)
            print("\nVocê ainda não possui textos personalizados salvos.")
            print('\n' + '=' * 50)
            input("Pressione ENTER para voltar...")
            return

        while True:
            util.limpar_tela()
            print('=' * 50)
            print(f"      📝 MEUS TEXTOS ({nome_usuario})")
            print('=' * 50)
            print(f"{'#':<4}{'TÍTULO':<40}{'IDIOMA':<15}{'AUTOR':<20}")
            print('-' * 79)

            textos_proprios = []
            for i, texto_id in enumerate(ids_proprios):
                texto = dados.DataManager.buscar_texto_por_id(texto_id)
                if texto:
                    textos_proprios.append(texto)
                    titulo_exibir = (texto['Titulo'][:37] + '...') if len(texto['Titulo']) > 40 else texto['Titulo']
                    print(f"{i+1:<4}{titulo_exibir:<40}{texto['idioma_nome']:<15}{texto['Autor']:<20}")
            
            print('\n' + '=' * 50)
            if para_remover:
                print(" 0 - Voltar")
                print('=' * 50)
                escolha = input("Digite o NÚMERO do texto que deseja remover (ou 0 para voltar): ").strip()
            else:
                print(" 0 - Voltar")
                print('=' * 50)
                escolha = input("Pressione ENTER para voltar: ").strip()

            if escolha == '0' or (not para_remover and not escolha):
                util.limpar_tela()
                return
            
            if para_remover:
                try:
                    indice = int(escolha) - 1
                    if 0 <= indice < len(textos_proprios):
                        texto_remover = textos_proprios[indice]
                        confirmacao = input(f"\033[33mTem certeza que deseja remover o texto '{texto_remover['Titulo']}'? (s/n): \033[m").strip().lower()
                        if confirmacao == 's':
                            Usuario.remover_texto_do_usuario(texto_remover['id'])
                            Usuario.usuarios = Usuario.carregar_usuarios()
                            Usuario.usuario_logado = Usuario.usuarios[Usuario.obter_indice_usuario(nome_usuario, Usuario.usuarios)]
                        else:
                            print("\033[33mRemoção cancelada.\033[m")
                            sleep(1)
                    else:
                        print("\033[31mOpção inválida.\033[m")
                        sleep(1)
                except ValueError:
                    print("\033[31mOpção inválida. Digite um número.\033[m")
                    sleep(1)
            else:
                 if escolha:
                    print("\033[31mOpção inválida. Pressione ENTER para voltar.\033[m")
                    sleep(1)
    @staticmethod
    def salvar_paragrafos_publicos(novo_paragrafo, remover=False):
        paragrafos_publicos = Usuario.carregar_paragrafos_publicos()
        
        if remover:
            try:
                item_chave = (novo_paragrafo['titulo'], novo_paragrafo['autor'])
                
                paragrafos_publicos[:] = [
                    p for p in paragrafos_publicos 
                    if (p['titulo'], p['autor']) != item_chave
                ]
            except Exception as e:
                print(f"Erro ao tentar remover dos públicos: {e}")
                
        elif novo_paragrafo['visibilidade'] == 'publico':
            paragrafos_publicos.append(novo_paragrafo)

        with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
            json.dump(paragrafos_publicos, f, indent=4, ensure_ascii=False)
            
    @staticmethod
    def salvar_usuarios_com_alteracao(usuario_alterado, todos_usuarios):
        for i, user in enumerate(todos_usuarios):
            if user[0] == usuario_alterado[0]:
                todos_usuarios[i] = usuario_alterado
                break
        
        Usuario.salvar_usuarios(todos_usuarios)
        
    @staticmethod
    def remover_usuario(usuarios):
        util.limpar_tela()
        print('=' * 50)
        print('      ❌ REMOVER CONTA')
        print('=' * 50)

        nome_ou_email = input("Nome de usuário ou E-mail da conta a ser excluída: ").strip()
        senha = maskpass.askpass(prompt="Senha: ", mask='*').strip() 
        
        indice_remover = -1
        for i, user in enumerate(usuarios):
            if (user[0] == nome_ou_email or (user[2] and user[2] == nome_ou_email)) and user[1] == senha:
                indice_remover = i
                break

        if indice_remover != -1:
            confirmacao = input(f"\033[33mTem certeza que deseja EXCLUIR a conta de '{usuarios[indice_remover][0]}'? Esta ação é irreversível. (s/n): \033[m").strip().lower()
            if confirmacao == 's':
                usuarios.pop(indice_remover)
                Usuario.salvar_usuarios(usuarios)
                print('\033[32mConta excluída com sucesso!\033[m')
                sleep(2)
                if Usuario.usuario_logado and Usuario.usuario_logado[0] == nome_ou_email:
                    Usuario.usuario_logado = None
                return True
            else:
                print('\033[34mExclusão cancelada.\033[m')
                sleep(2)
        else:
            print('\033[31mNome de usuário ou e-mail/senha inválidos ou não encontrados.\033[m')
            sleep(2)
        return False