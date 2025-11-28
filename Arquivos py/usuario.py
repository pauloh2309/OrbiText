import json
from os import system
from time import sleep
import re
import menu_principal
import verificação
import maskpass

ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_PUBLICOS = 'paragrafos_publicos.json'

class Usuario:
    
    usuario_logado = None 

    @staticmethod
    def carregar_usuarios():
        try:
            with open(ARQUIVO_USUARIOS, 'r') as arquivo:
                usuarios = json.load(arquivo)
                usuarios_completos = []
                for user in usuarios:
                    if len(user) == 2:
                        user.append('')
                        user.append([])
                    elif len(user) == 3:
                        user.append([])
                    usuarios_completos.append(user)
                return usuarios_completos
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Aviso: Arquivo de usuários JSON corrompido ou vazio. Iniciando com lista vazia.")
            return []
            
    @staticmethod
    def salvar_usuarios(lista_usuarios):
        try:
            with open(ARQUIVO_USUARIOS, 'w') as arquivo:
                json.dump(lista_usuarios, arquivo, indent=4) 
        except Exception as e:
            print(f"ERRO ao salvar usuários: {e}")

    @staticmethod
    def carregar_publicos():
        try:
            with open(ARQUIVO_PUBLICOS, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    @staticmethod
    def salvar_publicos(paragrafos):
        try:
            with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as arquivo:
                json.dump(paragrafos, arquivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"ERRO ao salvar parágrafos públicos: {e}")

    usuarios = carregar_usuarios() 

    @staticmethod
    def cadastrar_usuario(lista_usuarios):
        system('cls')
        print('=' * 50)
        print('          CADASTRO DE USUÁRIO')
        print('=' * 50)
        
        while True:
            nome = str(input('Digite seu nome: ').strip())
            if not nome:
                print("\033[31mNome não pode ser vazio.\033[m")
                continue
            
            for user in lista_usuarios:
                if user[0] == nome:
                    print('\033[31mUsuário já existe. Por favor, escolha outro nome de usuário.\033[m')
                    sleep(2)
                    break
            else:
                break

        while True:
            print('Digite sua senha (Mínimo de 8 e máximo de 12 caracteres, com letra maiúscula, minúscula, número e caracteres especiais): ')
            senha = maskpass.askpass(prompt='Senha: ', mask='*').strip()
            
            senha_valida = verificação.Verificar_dados.verificar_senha(senha)

            if not senha_valida:
                print("A senha que você colocou foi considerada fraca. Por favor, escreva uma senha considerada forte.")
                continue

            conf_senha = maskpass.askpass(prompt='Confirme sua senha: ', mask='*').strip()
            
            if conf_senha == senha:
                break
            else:
                print('\033[31mA Senha de confirmação não confere. Por favor, comece novamente o processo de seleção de senha.\033[m')
                sleep(2)

        while True:
            email = str(input('Digite seu email: ').strip())
            if not verificação.Verificar_dados.validar_email(email):
                print('\033[31mO email que você inseriu não está correto. Por favor, tente novamente.\033[m')
                sleep(2)
                continue
            break
        
        novo_usuario = [nome, senha, email, []]
        lista_usuarios.append(novo_usuario)
        Usuario.salvar_usuarios(lista_usuarios)

        print('\033[32mCadastro efetuado com sucesso!\033[m')
        sleep(2)
        system('cls')
        
    @staticmethod
    def fazer_login(lista_usuarios):
        system('cls')
        print('=' * 50)
        print('           LOGIN DE USUÁRIO')
        print('=' * 50)

        identificador = str(input('Nome de usuário ou Email: ').strip())
        
        try:
            senha = maskpass.askpass(prompt='Senha: ', mask='*').strip()
        except NameError:
            print("Aviso: 'maskpass' não está instalado. Usando entrada de senha padrão.")
            senha = str(input('Senha: ').strip())

        for user in lista_usuarios:
            if (user[0] == identificador or user[2] == identificador) and user[1] == senha:
                Usuario.usuario_logado = user
                system('cls')
                print(f'\033[32mLogin bem-sucedido! Bem-vindo(a), {user[0]}.\033[m')
                sleep(2)
                menu_principal.orbitext()
                return True
        
        system('cls')
        print('\033[31mIdentificador, Email ou senha inválidos.\033[m')
        sleep(2)
        system('cls')
        return False

    @staticmethod
    def expandir_paragrafo(paragrafo, origem="DETALHES"):
        system('cls')
        print('=' * 50)
        print(f"      EXPANSÃO DE LEITURA - {origem}")
        print(f"      Título: {paragrafo.get('titulo', 'N/A')} | Idioma: {paragrafo.get('idioma', 'N/A')}")
        print('=' * 50)

        print("\n--- TEXTO ORIGINAL ---")
        print(paragrafo.get('texto_original', 'Texto não encontrado.'))
        
        print("\n--- TRADUÇÃO (PORTUGUÊS) ---")
        print(paragrafo.get('traducao', 'Tradução não encontrada.'))
        
        print('=' * 50)
        input("Pressione ENTER para voltar à lista...")
        system('cls')
    
    @staticmethod
    def salvar_paragrafo(idioma, texto_original, traducao, titulo, visibilidade):
        if not Usuario.usuario_logado:
            print("\033[31mERRO: Necessário login para salvar parágrafo.\033[m")
            sleep(2)
            return False

        nome_usuario = Usuario.usuario_logado[0]
        
        paragrafo_base = {
            'texto_original': texto_original,
            'traducao': traducao,
            'idioma': idioma,
            'titulo': titulo
        }

        if visibilidade == 'privado':
            
            usuarios_lista_atualizada = Usuario.carregar_usuarios()
            usuario_index = -1
            for i, user in enumerate(usuarios_lista_atualizada):
                if user[0] == nome_usuario:
                    usuario_index = i
                    break
            
            if usuario_index != -1:
                if len(usuarios_lista_atualizada[usuario_index]) < 4:
                    usuarios_lista_atualizada[usuario_index].append([])
                
                paragrafos_salvos_do_usuario = usuarios_lista_atualizada[usuario_index][3]
                
                for p in paragrafos_salvos_do_usuario:
                    if (p.get('texto_original') == texto_original and 
                        p.get('titulo') == titulo):
                        print("\033[31mERRO: Este parágrafo já está salvo (privado).\033[m")
                        sleep(2)
                        return False # Retorna False em caso de duplicata
                
                novo_paragrafo_privado = paragrafo_base.copy()
                novo_paragrafo_privado['visibilidade'] = 'privado'
                
                usuarios_lista_atualizada[usuario_index][3].append(novo_paragrafo_privado)
                
                Usuario.usuarios = usuarios_lista_atualizada
                Usuario.usuario_logado = Usuario.usuarios[usuario_index]
                
                Usuario.salvar_usuarios(Usuario.usuarios)
                return True
            else:
                print("\033[31mERRO: Usuário não encontrado na lista.\033[m")
                sleep(2)
                return False

        elif visibilidade == 'publico':
            
            paragrafos_publicos = Usuario.carregar_publicos()
            paragrafo_existente = None
            paragrafo_salvo_pelo_user = False
            
            for p in paragrafos_publicos:
                if (p.get('texto_original') == texto_original and 
                    p.get('titulo') == titulo and 
                    p.get('idioma') == idioma):
                    paragrafo_existente = p
                    break
            
            if paragrafo_existente:
                if nome_usuario in paragrafo_existente['salvadores']:
                    print("\033[31mERRO: Este parágrafo já foi salvo por você (público).\033[m")
                    sleep(2)
                    return False # Retorna False em caso de duplicata pelo mesmo usuário
                else:
                    paragrafo_existente['salvadores'].append(nome_usuario)
                    paragrafo_existente['contagem'] += 1
                    paragrafo_salvo_pelo_user = True
            else:
                novo_paragrafo_publico = paragrafo_base.copy()
                novo_paragrafo_publico['salvadores'] = [nome_usuario]
                novo_paragrafo_publico['contagem'] = 1
                paragrafos_publicos.append(novo_paragrafo_publico)
                paragrafo_salvo_pelo_user = True

            if paragrafo_salvo_pelo_user:
                Usuario.salvar_publicos(paragrafos_publicos)
            
            usuarios_lista_atualizada = Usuario.carregar_usuarios()
            usuario_index = -1
            for i, user in enumerate(usuarios_lista_atualizada):
                if user[0] == nome_usuario:
                    usuario_index = i
                    break
            
            if usuario_index != -1:
                if len(usuarios_lista_atualizada[usuario_index]) < 4:
                    usuarios_lista_atualizada[usuario_index].append([])
                
                paragrafos_salvos_do_usuario = usuarios_lista_atualizada[usuario_index][3]
                
                for p in paragrafos_salvos_do_usuario:
                    if (p.get('texto_original') == texto_original and 
                        p.get('titulo') == titulo):
                        
                        if p.get('visibilidade') == 'publico':
                            # Se já está como publico no user list (improvável após check acima, mas seguro)
                            return True 
                            
                        # Remove a versão privada antiga se estiver sendo promovida a pública
                        paragrafos_salvos_do_usuario.remove(p)
                        break

                novo_paragrafo_user_publico = paragrafo_base.copy()
                novo_paragrafo_user_publico['visibilidade'] = 'publico'

                usuarios_lista_atualizada[usuario_index][3].append(novo_paragrafo_user_publico)
                
                Usuario.usuarios = usuarios_lista_atualizada
                Usuario.usuario_logado = Usuario.usuarios[usuario_index]
                
                Usuario.salvar_usuarios(Usuario.usuarios)

            return True

        return False

    @staticmethod
    def mostrar_meus_paragrafos(para_remover=False):
        system('cls')
        if not Usuario.usuario_logado or not Usuario.usuario_logado[3]:
            print(f"O usuário {Usuario.usuario_logado[0]} não possui parágrafos salvos.")
            input("Pressione ENTER para voltar ao Gerenciamento...")
            return

        paragrafos = Usuario.usuario_logado[3]
        titulo_sec = f"  MEUS PARÁGRAFOS SALVOS - {Usuario.usuario_logado[0]}"
        
        def exibir_lista(paragrafos, titulo_secao):
            system('cls')
            print('=' * 50)
            print(titulo_secao)
            print('=' * 50)
            
            print(f"{'#':<4} | {'IDIOMA':<10} | {'VISIBILIDADE':<15} | {'TÍTULO':<30} | TEXTO (SNIPPET)")
            print('-' * 90)
            
            for i, p in enumerate(paragrafos):
                texto_snippet = p['texto_original'][:40] + '...' if len(p['texto_original']) > 40 else p['texto_original']
                visibilidade = p.get('visibilidade', 'privado')
                print(f"{i+1:<4} | {p['idioma']:<10} | {visibilidade:<15} | {p['titulo']:<30} | {texto_snippet}")
                
            print('-' * 90)

        exibir_lista(paragrafos, titulo_sec)

        if not para_remover:
            while True:
                try:
                    escolha = input("Digite o número do parágrafo para EXPANDIR/VER DETALHES (0 para voltar): ")
                    if escolha.lower() == '0':
                        break
                    
                    indice = int(escolha) - 1
                    if 0 <= indice < len(paragrafos):
                        Usuario.expandir_paragrafo(paragrafos[indice], origem=titulo_sec.strip())
                        exibir_lista(paragrafos, titulo_sec) 
                        continue
                    else:
                        print("\033[31mNúmero de parágrafo inválido.\033[m")
                        sleep(1)
                except ValueError:
                    print("\033[31mEntrada inválida. Digite um número ou 0.\033[m")
                    sleep(1)
        
        else:
            while True:
                try:
                    escolha = input("Digite o número do parágrafo para remover (0 para cancelar): ")
                    if escolha.lower() == '0':
                        break
                    
                    indice = int(escolha) - 1
                    if 0 <= indice < len(paragrafos):
                        paragrafo_removido = Usuario.usuario_logado[3].pop(indice)
                        
                        if paragrafo_removido.get('visibilidade') == 'publico':
                            Usuario.remover_do_publico(paragrafo_removido)

                        usuarios_lista_atualizada = Usuario.carregar_usuarios()
                        for i, user in enumerate(usuarios_lista_atualizada):
                            if user[0] == Usuario.usuario_logado[0]:
                                usuarios_lista_atualizada[i] = Usuario.usuario_logado
                                break

                        Usuario.salvar_usuarios(usuarios_lista_atualizada)
                        
                        print(f"\033[32mParágrafo removido com sucesso: {paragrafo_removido['titulo']} ({paragrafo_removido['idioma']})\033[m")
                        sleep(2)
                        break
                    else:
                        print("\033[31mNúmero de parágrafo inválido.\033[m")
                        sleep(2)
                except ValueError:
                    print("\033[31mEntrada inválida. Digite um número.\033[m")
                    sleep(2)
        
        system('cls')
        
    @staticmethod
    def remover_do_publico(paragrafo_removido):
        
        paragrafos_publicos = Usuario.carregar_publicos()
        nome_usuario = Usuario.usuario_logado[0]
        
        for i, p in enumerate(paragrafos_publicos):
            if (p.get('texto_original') == paragrafo_removido.get('texto_original') and
                p.get('titulo') == paragrafo_removido.get('titulo') and
                p.get('idioma') == paragrafo_removido.get('idioma')):
                
                if nome_usuario in p['salvadores']:
                    p['salvadores'].remove(nome_usuario)
                    p['contagem'] -= 1
                    
                    if p['contagem'] <= 0:
                        paragrafos_publicos.pop(i)
                    
                    Usuario.salvar_publicos(paragrafos_publicos)
                    return

    @staticmethod
    def mostrar_paragrafos_publicos():
        system('cls')
        print('=' * 50)
        titulo_sec = "   PARÁGRAFOS PÚBLICOS SALVOS POR TODOS"
        print(titulo_sec)
        print('=' * 50)

        paragrafos_publicos = Usuario.carregar_publicos()
        
        if not paragrafos_publicos:
            print("\nNenhum parágrafo público encontrado.")
            input("Pressione ENTER para voltar ao Menu Principal...")
            system('cls')
            return

        print(f"{'#':<4} | {'IDIOMA':<10} | {'TÍTULO':<30} | {'SALVAMENTOS':<15} | TEXTO (SNIPPET)")
        print('-' * 90)
        for i, p in enumerate(paragrafos_publicos):
            texto_snippet = p['texto_original'][:40] + '...' if len(p['texto_original']) > 40 else p['texto_original']
            print(f"{i+1:<4} | {p['idioma']:<10} | {p['titulo']:<30} | {p['contagem']:<15} | {texto_snippet}")
        print('-' * 90)
        
        while True:
            try:
                escolha = input("Digite o número do parágrafo para EXPANDIR/VER DETALHES (0 para voltar): ")
                if escolha.lower() == '0':
                    break
                
                indice = int(escolha) - 1
                if 0 <= indice < len(paragrafos_publicos):
                    Usuario.expandir_paragrafo(paragrafos_publicos[indice], origem=titulo_sec.strip())
                    
                    # Re-display list after returning from expansion
                    system('cls')
                    print('=' * 50)
                    print(titulo_sec)
                    print('=' * 50)
                    print(f"{'#':<4} | {'IDIOMA':<10} | {'TÍTULO':<30} | {'SALVAMENTOS':<15} | TEXTO (SNIPPET)")
                    print('-' * 90)
                    for i, p in enumerate(paragrafos_publicos):
                        texto_snippet = p['texto_original'][:40] + '...' if len(p['texto_original']) > 40 else p['texto_original']
                        print(f"{i+1:<4} | {p['idioma']:<10} | {p['titulo']:<30} | {p['contagem']:<15} | {texto_snippet}")
                    print('-' * 90)
                    continue
                else:
                    print("\033[31mNúmero de parágrafo inválido.\033[m")
                    sleep(1)
            except ValueError:
                print("\033[31mEntrada inválida. Digite um número ou 0.\033[m")
                sleep(1)

        system('cls')