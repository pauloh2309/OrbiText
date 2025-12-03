from time import sleep, time
import usuario
import dados
from util import limpar_tela
import json
from os import system

def escolher_opcao(prompt):
    while True:
        try:
            print(" 0 - Voltar")
            escolha = input(prompt).strip()
            if escolha == '0':
                return 0
            
            opcao = int(escolha)
            if opcao >= 1:
                return opcao
            else:
                print("\033[31mOpção inválida. Digite um número positivo ou 0 para voltar.\033[m")
                sleep(1.5)
        except ValueError:
            print("\033[31mEntrada inválida. Digite um número.\033[m")
            sleep(1.5)

def listar_textos(lista_textos):
    for i, texto in enumerate(lista_textos):
        autor = texto.get('Autor', 'N/A')
        print(f" {i + 1} - {texto['Titulo']} (por {autor})")


def exibir_paragrafos_organizado(paragrafos, indice_inicio, num_mostrar, idioma_key):
    idioma_nome = dados.DataManager.IDIOMAS_NOMES.get(idioma_key, idioma_key.capitalize())
    CHAVE_ORIGINAL = 'Lingua' 
    CHAVE_PORTUGUES = 'portugues'
    
    print('~' * 70)
    
    paragrafos_exibidos = 0
    
    for i in range(indice_inicio, min(indice_inicio + num_mostrar, len(paragrafos))):
        p = paragrafos[i]
        
        print(f"\033[1mPÁRAGRAFO {i+1}:\033[0m")
        
       
        print(f"\033[34m[{idioma_nome}]\033[0m")
        print('=' * 20)
        print(p.get(CHAVE_ORIGINAL, "Texto original não encontrado."))
        print('=' * 20)
        
      
        print("\n\033[32m[Português]\033[0m")
        print('-' * 20)
        print(p.get(CHAVE_PORTUGUES, "Tradução não encontrada."))
        print('-' * 20)
        
        print('\n' + '~' * 70)
        paragrafos_exibidos += 1
        
    return paragrafos_exibidos


def exibir_texto(texto, modo, idioma_key):
    limpar_tela()
    
    start_time = time()
    paragrafos = texto["Paragrafos"]
    num_paragrafos = len(paragrafos)
    tempo_minimo_s = num_paragrafos * 5
    print(f"\033[34mTempo mínimo de leitura para XP base: {tempo_minimo_s} segundos.\033[m")
    sleep(1) 
    
    print('=' * 50)
    print(f"      LENDO: {texto['Titulo'].upper()}")
    print(f"      AUTOR: {texto.get('Autor', 'N/A')}")
    print(f"      REF: {texto.get('Referencia', 'N/A')}")
    print('=' * 50)
    
    indice_atual = 0
    
    while indice_atual < num_paragrafos:
        
        restantes = num_paragrafos - indice_atual
        
     
        prompt = (f"Pressione ENTER para ler o próximo parágrafo (1) "
                  f"ou digite quantos parágrafos deseja ler de uma vez (1-{restantes}): ")
        
        num_mostrar = 0
        while True:
           
            limpar_tela() 
            print('=' * 50)
            print(f"      LENDO: {texto['Titulo'].upper()} (Parágrafo {indice_atual + 1} de {num_paragrafos})")
            print('=' * 50)

            entrada = input(prompt).strip()
            
            if not entrada:
                num_mostrar = 1 
                break
            
            try:
                num_mostrar = int(entrada)
                if num_mostrar > 0 and num_mostrar <= restantes:
                    break
                else:
                    print(f"\033[31mNúmero inválido. Digite um número entre 1 e {restantes}.\033[m")
                    sleep(1.5)
            except ValueError:
                print("\033[31mEntrada inválida. Digite um número ou apenas ENTER.\033[m")
                sleep(1.5)

        
        paragrafos_exibidos = exibir_paragrafos_organizado(paragrafos, indice_atual, num_mostrar, idioma_key)
        
        
 
        while True:
            print('\n' + '~' * 50)
            print("AÇÕES DE SALVAMENTO DE PARÁGRAFOS:")
            print(f"Digite o NÚMERO do parágrafo que deseja salvar/publicar (entre {indice_atual + 1} e {indice_atual + paragrafos_exibidos})")
            print("Ou digite 0 para continuar a leitura (sem salvar/publicar).")
            
            acao_paragrafo = input("Opção (Número do Parágrafo | 0): ").strip()
            
            if acao_paragrafo == '0':
                break  
            
            try:
                num_paragrafo_escolhido = int(acao_paragrafo)
                
                if indice_atual + 1 <= num_paragrafo_escolhido <= indice_atual + paragrafos_exibidos:
                    
                    if not usuario.Usuario.usuario_logado:
                        print('\033[31mVocê precisa estar logado para salvar ou publicar parágrafos.\033[m')
                        sleep(2)
                        continue

                    indice_paragrafo_salvar = num_paragrafo_escolhido - 1
                    paragrafo_obj = paragrafos[indice_paragrafo_salvar]
                    titulo_paragrafo = texto['Titulo']
                    
                    print('\n--- ESCOLHA A VISIBILIDADE ---')
                    print(" 1 - Publicar Parágrafo (Para todos verem)")
                    print(" 2 - Salvar Parágrafo (Apenas para você)")
                    print(" 0 - Cancelar e voltar para a seleção do parágrafo")
                    print('------------------------------')
                    
                    while True:
                        modo_salvamento = input("Opção: ").strip()
                        
                        if modo_salvamento == '0':
                            break 
                        
                        if modo_salvamento in ['1', '2']:
                            tipo_visibilidade = 'publico' if modo_salvamento == '1' else 'privado'
                            

                            salvo_id = dados.DataManager.salvar_paragrafo_publico(
                                titulo_paragrafo,
                                idioma_key,
                                paragrafo_obj.get('Lingua'),
                                paragrafo_obj.get('portugues'),
                                tipo_visibilidade,
                                paragrafo_numero=num_paragrafo_escolhido,
                                texto_id=texto.get('id', dados.DataManager.gerar_novo_id())
                            )
                            if salvo_id and usuario.Usuario.usuario_logado:
                                if not usuario.Usuario.usuarios:
                                    usuario.Usuario.usuarios = usuario.Usuario.carregar_usuarios()
                                usuario.Usuario.usuario_logado[3].append(salvo_id)
                                usuario.Usuario.salvar_usuarios(usuario.Usuario.usuarios)
                            print(f'\033[32mParágrafo {num_paragrafo_escolhido} salvo como {tipo_visibilidade} com sucesso!\033[m')
                            sleep(1.5)
                            break 
                        else:
                            print("\033[31mOpção de visibilidade inválida. Digite 1, 2 ou 0.\033[m")
                            sleep(1)

                else:
                    print(f"\033[31mNúmero de parágrafo inválido. Escolha entre {indice_atual + 1} e {indice_atual + paragrafos_exibidos}.\033[m")
                    sleep(1.5)
            except ValueError:
                print("\033[31mEntrada inválida. Digite o número do parágrafo ou 0.\033[m")
                sleep(1.5)

        indice_atual += paragrafos_exibidos
        
        
        if indice_atual < num_paragrafos:
            input("\nPressione ENTER para continuar a leitura...")
        
    end_time = time()
    tempo_total = end_time - start_time
    
    if usuario.Usuario.usuario_logado:
        usuario.Usuario.adicionar_xp_leitura(tempo_total, tempo_minimo_s, idioma_key)
    
    print('\n' + '=' * 50)
    print('\033[32mLeitura concluída!\033[m')
    input("Pressione ENTER para voltar ao menu de leitura...")
    

def leitura_generica(lista_textos, nome_idioma):
    limpar_tela()
    if not lista_textos:
        print(f"\033[31mNenhum texto disponível para {nome_idioma.upper()}.\033[m")
        sleep(2)
        return

    while True:
        limpar_tela()
        print('=' * 50)
        print(f"      TEXTOS DISPONÍVEIS - {nome_idioma.upper()}")
        print('=' * 50)
        listar_textos(lista_textos)
        print('=' * 50)
        
        opcao = escolher_opcao("Digite o número do texto que você deseja ler: ")
        
        if opcao is None:
            sleep(1.5)
            continue
        
        if opcao == 0:
            return
        
        try:
            indice = opcao - 1
            texto_escolhido = lista_textos[indice]
            
            limpar_tela()
            print('=' * 50)
            print(f"      MODOS DE LEITURA PARA: {texto_escolhido['Titulo'].upper()}")
            print('=' * 50)
            print(" 1 - Ler no idioma original")
            print(" 2 - Ler em português")
            print(" 3 - Ler lado a lado")
            print(" 0 - Voltar")
            print('=' * 50)
            
            while True:
                modo = input("Escolha o modo de leitura: ").strip()
                if modo in ['1', '2', '3']:
                    
                    idioma_key = texto_escolhido.get('Nome_Idioma_Exibicao', 'English').lower()
                    exibir_texto(texto_escolhido, modo, idioma_key)
                    return
                elif modo == '0':
                    break
                else:
                    print("\033[31mOpção inválida.\033[m")
                    sleep(1.5)

        except IndexError:
            print("\033[31mOpção inválida. Escolha um número da lista ou 0 para voltar.\033[m")
            sleep(1.5)
        except Exception as e:
            print(f"\033[31mOcorreu um erro: {e}\033[m")
            sleep(1.5)


def menu_leitura_idioma():
    
   
    textos_por_idioma = dados.DataManager.carregar_textos_idiomas()
    

    idiomas_disponiveis = {}
    
    for idioma_chave, lista_textos in textos_por_idioma.items():
        if lista_textos:

            nome_exibicao = lista_textos[0].get("Nome_Idioma_Exibicao", idioma_chave.capitalize()) 
            idiomas_disponiveis[idioma_chave] = (nome_exibicao, lista_textos)

    idioma_opcoes = list(idiomas_disponiveis.keys())
    
    while True:
        limpar_tela()
        print('=' * 50)
        print('      📚 MENU DE LEITURA POR IDIOMA')
        print('=' * 50)
        print("Escolha o idioma para ler:")
        
        if not idioma_opcoes:
            print("\033[33mNenhum idioma com textos disponíveis. Adicione um texto para começar.\033[m")
            print(" 0 - Voltar")
            print('=' * 50)
            escolha = input("Opção: ").strip()
            if escolha == '0':
                return
            else:
                print("\033[31mOpção inválida.\033[m")
                sleep(1.5)
                continue


        for i, idioma_chave in enumerate(idioma_opcoes):
            nome_exibicao = idiomas_disponiveis[idioma_chave][0]
            print(f" {i + 1} - {nome_exibicao}")
            
        print(" 0 - Voltar")
        print('=' * 50)
        
        escolha = input("Opção: ").strip()
        
        if escolha == '0':
            return
        
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(idioma_opcoes):
                idioma_chave = idioma_opcoes[indice]
                nome_idioma, lista_textos = idiomas_disponiveis[idioma_chave]
                
                leitura_generica(lista_textos, nome_idioma)
 
                continue 

            else:
                print("\033[31mOpção inválida.\033[m")
                sleep(1.5)
        except ValueError:
            print("\033[31mOpção inválida.\033[m")
            sleep(1.5)


def criar_e_salvar_novo_texto():
    limpar_tela()
    
    print('=' * 50)
    print('      ✍️  CRIAR NOVO TEXTO PERSONALIZADO')
    print('=' * 50)
    
    if not usuario.Usuario.usuario_logado:
        print("\033[31mErro: É necessário estar logado para criar textos.\033[m")
        sleep(2)
        return

    titulo = input("Digite o Título/Referência do texto: ").strip()
    if not titulo:
        print("\033[31mErro: O título não pode ser vazio.\033[m")
        sleep(2)
        return

    while True:
        limpar_tela()
        print('Escolha o idioma original:')
        print(' 1 - English')
        print(' 2 - French')
        print(' 3 - Spanish')
        print(' 0 - Cancelar')
        escolha_idioma = input('Opção: ').strip()
        if escolha_idioma == '0':
            return
        mapa = {'1': 'English', '2': 'French', '3': 'Spanish'}
        if escolha_idioma in mapa:
            idioma_original = mapa[escolha_idioma]
            break
        else:
            print("\033[31mIdioma inválido. Digite 1, 2, 3 ou 0.\033[m")
            sleep(1)
            
    lista_paragrafos = []
    num_paragrafo = 1
    
    while True:
        limpar_tela()
        print(f"--- Adicionando Parágrafo {num_paragrafo} ---")
        print("Digite 0 para cancelar a criação do texto e voltar ao menu.")
        print('=' * 50)
        texto_original = input(f"[{idioma_original}] Parágrafo Original: ").strip()
        if texto_original == '0':
            return
        if not texto_original:
            print("\033[31mO parágrafo original não pode ser vazio.\033[m")
            sleep(1.5)
            continue
        texto_traducao = input("[Português] Tradução correspondente: ").strip()
        if texto_traducao == '0':
            return
        if not texto_traducao:
            print("\033[31mA tradução não pode ser vazia.\033[m")
            sleep(1.5)
            continue

        lista_paragrafos.append({'original': texto_original, 'traducao': texto_traducao})
        num_paragrafo += 1
        while True:
            print('\nEscolha: 1 - Adicionar outro parágrafo | 0 - Finalizar texto e salvar')
            escolha_cont = input('Opção (0/1): ').strip()
            if escolha_cont == '1':
                break
            elif escolha_cont == '0':
                break
            else:
                print("\033[31mOpção inválida. Digite 1 ou 0.\033[m")
                sleep(1)
        if escolha_cont == '0':
            break

    if not lista_paragrafos:
        print("\033[33mNenhum parágrafo foi adicionado. Voltando ao menu...\033[m")
        sleep(2)
        return

    print('\n' + '=' * 50)
    print(f"Você criou um texto com {len(lista_paragrafos)} parágrafo(s).")
    print('\nEscolha: 1 - Salvar texto | 0 - Descartar')
    while True:
        salvar = input('Opção (0/1): ').strip()
        if salvar == '1':
            dados.DataManager.salvar_texto_personalizado(titulo, idioma_original, lista_paragrafos)
            break
        elif salvar == '0':
            print("\033[33mTexto descartado. Voltando ao menu...\033[m")
            sleep(2)
            break
        else:
            print("\033[31mOpção inválida. Digite 1 ou 0.\033[m")
            sleep(1)

def ver_comentarios(paragrafo_id):
    limpar_tela()
    parag = next((p for p in dados.DataManager.carregar_paragrafos_publicos() if p.get('id') == str(paragrafo_id)), None)
    if parag:
        publicos = parag.get('comentarios_publicos', [])
        privados = parag.get('comentarios_privados', {})
        print('=' * 50)
        print('      💬 COMENTÁRIOS PÚBLICOS')
        print('=' * 50)
        if publicos:
            for i, c in enumerate(publicos):
                likes_count = dados.DataManager.obter_likes_comentario(f"{paragrafo_id}:c:{i}")
                print(f"[{i+1}] {c.get('autor', 'anon')}: {c.get('texto')} ❤️  {likes_count}")
        else:
            print('Nenhum comentário público.')

        if usuario.Usuario.usuario_logado:
            nome_usuario = usuario.Usuario.usuario_logado[0]
            comentarios_privados = privados.get(nome_usuario, [])
            print('\n' + '=' * 50)
            print('      🔒 SEUS COMENTÁRIOS PRIVADOS')
            print('=' * 50)
            if comentarios_privados:
                for i, c in enumerate(comentarios_privados):
                    print(f"[{i+1}] Você: {c.get('texto')}")
            else:
                print('Nenhum comentário privado seu.')

        can_public = parag.get('visibilidade') != 'privado'
        print('\n' + '=' * 50)
        if can_public:
            print(' 1 - Adicionar Comentário Público')
            print(' 2 - Adicionar Comentário Privado')
            print(' 3 - Curtir/Descurtir um Comentário Público')
        else:
            print(' 1 - (Comentário público indisponível para este parágrafo)')
            print(' 2 - Adicionar Comentário Privado')
            print(' 3 - Curtir/Descurtir um Comentário Público')
        print(' 0 - Voltar')
        print('=' * 50)

        while True:
            opcao = input('Opção: ').strip()
            if opcao == '0':
                break
            elif opcao == '3':
                
                if not publicos:
                    print('\033[33mNenhum comentário público para curtir.\033[m')
                    sleep(1.5)
                    continue
                
                if not usuario.Usuario.usuario_logado:
                    print('\033[31mÉ necessário estar logado para curtir comentários.\033[m')
                    sleep(2)
                    continue
                
                print('Qual comentário você deseja curtir/descurtir?')
                for i, c in enumerate(publicos):
                    likes_count = dados.DataManager.obter_likes_comentario(f"{paragrafo_id}:c:{i}")
                    usuario_curtiu = dados.DataManager.usuario_curtiu_comentario(f"{paragrafo_id}:c:{i}", usuario.Usuario.usuario_logado[0])
                    status = '✓ (você curtiu)' if usuario_curtiu else ''
                    print(f"[{i+1}] {c.get('texto')[:50]}... ❤️  {likes_count} {status}")
                print('[0] Cancelar')
                
                escolha_com = input('Opção: ').strip()
                if escolha_com == '0':
                    continue
                
                try:
                    idx_com = int(escolha_com) - 1
                    if 0 <= idx_com < len(publicos):
                        usuario_nome = usuario.Usuario.usuario_logado[0]
                        comentario_id = f"{paragrafo_id}:c:{idx_com}"
                        
                        if dados.DataManager.usuario_curtiu_comentario(comentario_id, usuario_nome):
                            
                            if dados.DataManager.descurtir_comentario(comentario_id, usuario_nome):
                                print('\033[32mCurtida removida!\033[m')
                            else:
                                print('\033[31mErro ao remover curtida.\033[m')
                        else:
                            
                            if dados.DataManager.curtir_comentario(comentario_id, usuario_nome):
                                print('\033[32mComentário curtido!\033[m')
                            else:
                                print('\033[31mErro ao curtir comentário.\033[m')
                        
                        sleep(1.5)
                        ver_comentarios(paragrafo_id)
                        return
                    else:
                        print('\033[31mOpção inválida.\033[m')
                        sleep(1)
                except ValueError:
                    print('\033[31mEntrada inválida.\033[m')
                    sleep(1)
                    
            elif opcao in ['1', '2']:
                if not usuario.Usuario.usuario_logado:
                    print('\033[31mÉ necessário estar logado para comentar.\033[m')
                    sleep(2)
                    continue
                comentario_texto = input('Digite seu comentário: ').strip()
                if not comentario_texto:
                    print('\033[31mO comentário não pode ser vazio.\033[m')
                    sleep(1.5)
                    continue
                autor = usuario.Usuario.usuario_logado[0]
                tipo = 'publico' if opcao == '1' else 'privado'
                
                res = dados.DataManager.salvar_comentario(paragrafo_id, autor, comentario_texto, tipo)
                if res is False:
                    print('\033[31mNão é possível adicionar comentário público a um parágrafo privado.\033[m')
                    sleep(1.5)
                    return
                print(f"\033[32mComentário {tipo} salvo com sucesso!\033[m")
                sleep(1.5)
                ver_comentarios(paragrafo_id)
                return
            else:
                print('\033[31mOpção inválida.\033[m')
                sleep(1)
        return
    pid_str = str(paragrafo_id)
    if ':' in pid_str:
        tid, idx = pid_str.split(':', 1)
        try:
            idxn = int(idx)
        except Exception:
            idxn = None
        if idxn is not None:
            data_textos = dados.DataManager.carregar_textos_idiomas()
            for idioma_key in data_textos:
                for texto_obj in data_textos[idioma_key]:
                    if texto_obj.get('id') == tid:
                        pargs = texto_obj.get('Paragrafos', [])
                        if 0 <= idxn < len(pargs):
                            par = pargs[idxn]
                            publicos = par.get('comentarios_publicos', [])
                            privados = par.get('comentarios_privados', {})
                            print('=' * 50)
                            print('      💬 COMENTÁRIOS PÚBLICOS')
                            print('=' * 50)
                            if publicos:
                                for i, c in enumerate(publicos):
                                    print(f"[{i+1}] {c.get('autor','anon')}: {c.get('texto')}")
                            else:
                                print('Nenhum comentário público.')
                            if usuario.Usuario.usuario_logado:
                                nome_usuario = usuario.Usuario.usuario_logado[0]
                                comentarios_privados = privados.get(nome_usuario, [])
                                print('\n' + '=' * 50)
                                print('      🔒 SEUS COMENTÁRIOS PRIVADOS')
                                print('=' * 50)
                                if comentarios_privados:
                                    for i, c in enumerate(comentarios_privados):
                                        print(f"[{i+1}] Você: {c.get('texto')}")
                                else:
                                    print('Nenhum comentário privado seu.')
                            print('\n' + '=' * 50)
                            print(' 1 - Adicionar Comentário Público')
                            print(' 2 - Adicionar Comentário Privado')
                            print(' 0 - Voltar')
                            print('=' * 50)
                            while True:
                                opcao = input('Opção: ').strip()
                                if opcao == '0':
                                    return
                                elif opcao in ['1','2']:
                                    if not usuario.Usuario.usuario_logado:
                                        print('\033[31mÉ necessário estar logado para comentar.\033[m')
                                        sleep(2)
                                        continue
                                    comentario_texto = input('Digite seu comentário: ').strip()
                                    if not comentario_texto:
                                        print('\033[31mO comentário não pode ser vazio.\033[m')
                                        sleep(1.5)
                                        continue
                                    autor = usuario.Usuario.usuario_logado[0]
                                    tipo = 'publico' if opcao == '1' else 'privado'
                                    res = dados.DataManager.salvar_comentario(pid_str, autor, comentario_texto, tipo)
                                    if res is False:
                                        print('\033[31mNão é possível adicionar comentário público a um parágrafo privado.\033[m')
                                        sleep(1.5)
                                        return
                                    print(f"\033[32mComentário {tipo} salvo com sucesso!\033[m")
                                    sleep(1.5)
                                    return
                                else:
                                    print('\033[31mOpção inválida.\033[m')
                                    sleep(1)
    comentarios_data = dados.DataManager.carregar_comentarios()
    paragrafo_id_str = pid_str
    if paragrafo_id_str not in comentarios_data:
        print('Nenhum comentário encontrado para este parágrafo.')
        input('\nPressione ENTER para voltar...')
        return
    data_paragrafo = comentarios_data[paragrafo_id_str]

    print('=' * 50)
    print('      💬 COMENTÁRIOS PÚBLICOS')
    print('=' * 50)
    if data_paragrafo['publicos']:
        for i, c in enumerate(data_paragrafo['publicos']):
            print(f"[{i+1}] {c['autor']}: {c['texto']}")
    else:
        print('Nenhum comentário público.')

    if usuario.Usuario.usuario_logado:
        nome_usuario = usuario.Usuario.usuario_logado[0]
        comentarios_privados = data_paragrafo['privados'].get(nome_usuario, [])
        print('\n' + '=' * 50)
        print('      🔒 SEUS COMENTÁRIOS PRIVADOS')
        print('=' * 50)
        if comentarios_privados:
            for i, c in enumerate(comentarios_privados):
                print(f"[{i+1}] Você: {c['texto']}")
        else:
            print('Nenhum comentário privado seu.')
    
    print('\n' + '=' * 50)
    print(" 1 - Adicionar Comentário Público")
    print(" 2 - Adicionar Comentário Privado")
    print(" 0 - Voltar")
    print('=' * 50)
    
    while True:
        opcao = input("Opção: ").strip()
        if opcao == '0':
            break
        elif opcao in ['1', '2']:
            if not usuario.Usuario.usuario_logado:
                print("\033[31mÉ necessário estar logado para comentar.\033[m")
                sleep(2)
                continue
            
            comentario_texto = input("Digite seu comentário: ").strip()
            if not comentario_texto:
                print("\033[31mO comentário não pode ser vazio.\033[m")
                sleep(1.5)
                continue
                
            autor = usuario.Usuario.usuario_logado[0]
            tipo = 'publico' if opcao == '1' else 'privado'
            dados.DataManager.salvar_comentario(paragrafo_id, autor, comentario_texto, tipo)
            print(f"\033[32mComentário {tipo} salvo com sucesso!\033[m")
            sleep(1.5)

            ver_comentarios(paragrafo_id)
            return

        else:
            print("\033[31mOpção inválida.\033[m")
            sleep(1)


def menu_ver_paragrafos_publicos():
    limpar_tela()
    paragrafos = dados.DataManager.carregar_paragrafos_publicos(visibilidade='publico')
    
    if not paragrafos:
        print("\033[33mNenhum parágrafo público disponível.\033[m")
        sleep(2)
        return

    while True:
        limpar_tela()
        print('=' * 50)
        print("      🌍 PARÁGRAFOS PÚBLICOS DISPONÍVEIS")
        print('=' * 50)
        
        for i, p in enumerate(paragrafos):
            paragrafo_ref = f" - Parágrafo {p.get('paragrafo_numero', 'N/A')}" if p.get('paragrafo_numero') else ''
            texto_assoc = ''
            if p.get('texto_id'):
                t = dados.DataManager.buscar_texto_por_id(p.get('texto_id'))
                if t:
                    texto_assoc = f" [do texto: {t.get('Titulo')}]"
            idioma_nome = dados.DataManager.IDIOMAS_NOMES.get(p.get('idioma'), p.get('idioma'))
            print(f"{i + 1} - {p.get('titulo') or '[sem título]'}{paragrafo_ref}{texto_assoc} ({idioma_nome}) por {p.get('autor')}")
            
        print("0 - Voltar")
        print('=' * 50)
        
        opcao = escolher_opcao("Digite o número do parágrafo que você deseja ver/comentar: ")
        
        if opcao is None:
            sleep(1.5)
            continue
        
        if opcao == 0:
            return
        
        try:
            paragrafo_escolhido = paragrafos[opcao - 1]
            limpar_tela()
            print('=' * 50)
            print(f"      PARÁGRAFO: {paragrafo_escolhido['titulo'].upper()}")
            print(f"      AUTOR: {paragrafo_escolhido['autor']}")
            print('=' * 50)
            print(f"\n[{paragrafo_escolhido['idioma']}]")
            print(paragrafo_escolhido['texto_original'])
            print("\n[Português]")
            print(paragrafo_escolhido['traducao'])
            print('\n' + '=' * 50)
            
            
            num_likes = dados.DataManager.obter_likes_paragrafo(paragrafo_escolhido['id'])
            print(f"❤️  {num_likes} curtida(s)")
            
            
            usuario_curtiu = False
            if usuario.Usuario.usuario_logado:
                usuario_curtiu = dados.DataManager.usuario_curtiu_paragrafo(
                    paragrafo_escolhido['id'], 
                    usuario.Usuario.usuario_logado[0]
                )
            
            print("\n 1 - Ver/Adicionar Comentários")
            if usuario.Usuario.usuario_logado:
                if usuario_curtiu:
                    print(" 2 - Remover minha curtida")
                else:
                    print(" 2 - Curtir este parágrafo")
            print(" 0 - Voltar para a lista")
            print('=' * 50)
            
            while True:
                sub_opcao = input("Opção: ").strip()
                if sub_opcao == '1':
                    ver_comentarios(paragrafo_escolhido['id'])
 
                elif sub_opcao == '2':
                    if not usuario.Usuario.usuario_logado:
                        print("\033[31mÉ necessário estar logado para curtir.\033[m")
                        sleep(1.5)
                        continue
                    
                    usuario_nome = usuario.Usuario.usuario_logado[0]
                    paragrafo_id = paragrafo_escolhido['id']
                    
                    if usuario_curtiu:
                        
                        if dados.DataManager.descurtir_paragrafo(paragrafo_id, usuario_nome):
                            print("\033[32mCurtida removida!\033[m")
                            usuario_curtiu = False
                        else:
                            print("\033[31mErro ao remover curtida.\033[m")
                    else:
                       
                        if dados.DataManager.curtir_paragrafo(paragrafo_id, usuario_nome):
                            print("\033[32mParágrafo curtido!\033[m")
                            usuario_curtiu = True
                        else:
                            print("\033[31mVocê já curtiu este parágrafo.\033[m")
                    
                    sleep(1.5)
                    limpar_tela()
                    print('=' * 50)
                    print(f"      PARÁGRAFO: {paragrafo_escolhido['titulo'].upper()}")
                    print(f"      AUTOR: {paragrafo_escolhido['autor']}")
                    print('=' * 50)
                    print(f"\n[{paragrafo_escolhido['idioma']}]")
                    print(paragrafo_escolhido['texto_original'])
                    print("\n[Português]")
                    print(paragrafo_escolhido['traducao'])
                    print('\n' + '=' * 50)
                    
                    
                    num_likes = dados.DataManager.obter_likes_paragrafo(paragrafo_escolhido['id'])
                    print(f"❤️  {num_likes} curtida(s)")
                    
                    print("\n 1 - Ver/Adicionar Comentários")
                    if usuario.Usuario.usuario_logado:
                        if usuario_curtiu:
                            print(" 2 - Remover minha curtida")
                        else:
                            print(" 2 - Curtir este parágrafo")
                    print(" 0 - Voltar para a lista")
                    print('=' * 50)
                    
                elif sub_opcao == '0':
                    break
                else:
                    print("\033[31mOpção inválida.\033[m")
                    sleep(1)
            
        except IndexError:
            print("\033[31mOpção inválida. Escolha um número da lista ou 0 para voltar.\033[m")
            sleep(1.5)
        except Exception as e:
            print(f"\033[31mOcorreu um erro: {e}\033[m")
            sleep(1.5)