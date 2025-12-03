import json
import maskpass
from os import system
from time import sleep
from pathlib import Path
import util
import dados
import verificação
import menu_principal

ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_PUBLICOS = 'paragrafos_publicos.json'


class Usuario:
    

    usuarios = []
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
                try:
                    return json.load(f)
                except Exception:
                    return []
        return []

    @staticmethod
    def salvar_usuarios(usuarios):
        with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _encontrar_usuario(usuarios, nome_ou_email):
        def norm(s):
            return s.strip().lower() if s else ''
        chave = norm(nome_ou_email)
        for i, u in enumerate(usuarios):
            if len(u) < 3:
                continue
            if norm(u[0]) == chave or norm(u[2]) == chave:
                return i, u
        return -1, None

    @staticmethod
    def _usuario_existe(usuarios, nome_ou_email, check_email_only=False):
        def norm(s):
            return s.strip().lower() if s else ''
        chave = norm(nome_ou_email)
        for u in usuarios:
            if len(u) < 3:
                continue
            if not check_email_only and norm(u[0]) == chave:
                return True, 'Nome de usuário'
            if norm(u[2]) == chave:
                return True, 'E-mail'
        return False, None

    @staticmethod
    def cadastrar_usuario(usuarios):
        util.limpar_tela()
        print('=' * 50)
        print('      ✍️  NOVO REGISTRO (CONTA)')
        print('=' * 50)

        tentativas = 0
        while tentativas < 3:
            nome = input('Digite o nome de usuário (será usado para login): ').strip()
            if not nome:
                print('\033[31mErro: Nome não pode ser vazio.\033[m')
                tentativas += 1
                sleep(1.5)
                continue
            if len(nome) < 4:
                print('\033[31mErro: Nome muito curto. Deve ter pelo menos 4 letras.\033[m')
                tentativas += 1
                sleep(1.5)
                continue
            if len(nome) > 10:
                print('\033[31mErro: Nome muito longo. Máximo de 10 letras permitido.\033[m')
                tentativas += 1
                sleep(1.5)
                continue
            if not nome.isalpha():
                print('\033[31mErro: Nome deve conter apenas letras (A-Z). Remova números ou espaços.\033[m')
                tentativas += 1
                sleep(1.5)
                continue
            existe, tipo = Usuario._usuario_existe(usuarios, nome)
            if existe and tipo == 'Nome de usuário':
                print(f'\033[31mErro: Nome "{nome}" já cadastrado.\033[m')
                tentativas += 1
                sleep(1.5)
                continue
            break
        if tentativas == 3:
            print('\033[31mNúmero máximo de tentativas atingido.\033[m')
            sleep(1.5)
            return False

        tentativas = 0
        while tentativas < 3:
            email = input('Digite seu e-mail (usado para recuperação): ').strip()
            if not verificação.Verificar_dados.validar_email(email):
                print('\033[31mE-mail inválido.\033[m')
                tentativas += 1
                sleep(1.5)
                continue
            existe, tipo = Usuario._usuario_existe(usuarios, email, check_email_only=True)
            if existe and tipo == 'E-mail':
                print(f'\033[31mE-mail "{email}" já cadastrado.\033[m')
                tentativas += 1
                sleep(1.5)
                continue
            break
        if tentativas == 3:
            print('\033[31mNúmero máximo de tentativas atingido.\033[m')
            sleep(1.5)
            return False

        tentativas = 0
        while tentativas < 3:
            print('Digite sua senha (8-12 caracteres, com maiúscula, minúscula, número e especial):')
            senha = maskpass.askpass(prompt='Senha: ', mask='*').strip()
            if not verificação.Verificar_dados.verificar_senha(senha):
                tentativas += 1
                continue
            conf = maskpass.askpass(prompt='Confirme a senha: ', mask='*').strip()
            if conf != senha:
                print('\033[31mSenhas não conferem.\033[m')
                tentativas += 1
                continue
            break
        if tentativas == 3:
            print('\033[31mNúmero máximo de tentativas atingido.\033[m')
            sleep(1.5)
            return False

        novo = [nome, senha, email, [], 0, {'english': 0, 'french': 0, 'spanish': 0}]
        usuarios.append(novo)
        Usuario.salvar_usuarios(usuarios)
        print(f"\033[32mUsuário '{nome}' cadastrado com sucesso!\033[m")
        sleep(1.5)
        return True

    @staticmethod
    def fazer_login(usuarios):
        util.limpar_tela()
        print('=' * 50)
        print('      🔑 LOGIN (CONTA EXISTENTE)')
        print('=' * 50)
        tentativas = 0
        while tentativas < 3:
            nome_email = input('Digite o nome de usuário ou e-mail: ').strip()
            if not nome_email:
                print('\033[31mEntrada vazia.\033[m')
                tentativas += 1
                sleep(1)
                continue
            idx, u = Usuario._encontrar_usuario(usuarios, nome_email)
            if idx == -1:
                print('\033[31mUsuário não encontrado.\033[m')
                tentativas += 1
                sleep(1)
                continue
            senha = maskpass.askpass(prompt='Senha: ', mask='*').strip()
            if senha != u[1]:
                print('\033[31mSenha incorreta.\033[m')
                tentativas += 1
                sleep(1)
                continue
            Usuario.usuarios = Usuario.carregar_usuarios()
            idx = Usuario.obter_indice_usuario(u[0], Usuario.usuarios)
            Usuario.usuario_logado = Usuario.usuarios[idx] if idx != -1 else u
            util.limpar_tela()
            print(f"\033[32mBem-vindo(a), {Usuario.usuario_logado[0]}!\033[m")
            sleep(1.5)
            menu_principal.menu_principal()
            return True
        print('\033[31mTentativas excedidas. Voltando.\033[m')
        sleep(1)
        return False

    @staticmethod
    def carregar_paragrafos_publicos():
        if Path(ARQUIVO_PUBLICOS).exists():
            with open(ARQUIVO_PUBLICOS, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except Exception:
                    return []
        return []

    @staticmethod
    def salvar_paragrafos_publicos(novo_paragrafo, remover=False):
        paragrafos = Usuario.carregar_paragrafos_publicos()
        if remover:
            paragrafos = [p for p in paragrafos if p.get('id') != novo_paragrafo.get('id')]
        else:
            if novo_paragrafo.get('visibilidade') == 'publico' or novo_paragrafo.get('visibilidade') == 'privado':
                paragrafos.append(novo_paragrafo)
        with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
            json.dump(paragrafos, f, indent=4, ensure_ascii=False)

    @staticmethod
    def mostrar_meus_paragrafos(para_remover=False):
        util.limpar_tela()
        if not Usuario.usuario_logado:
            print('\033[31mVocê precisa estar logado para ver seus textos.\033[m')
            sleep(1.5)
            return
        nome = Usuario.usuario_logado[0]
        ids = Usuario.usuario_logado[3] if len(Usuario.usuario_logado) > 3 else []

        itens = []
        for tid in ids:
            texto = dados.DataManager.buscar_texto_por_id(tid)
            if texto:
                itens.append({'id': tid, 'titulo': texto.get('Titulo'), 'tipo': 'personalizado', 'autor': texto.get('Autor')})
                continue
            p = next((pp for pp in Usuario.carregar_paragrafos_publicos() if pp.get('id') == tid), None)
            if p:
                itens.append({'id': tid, 'titulo': p.get('titulo'), 'tipo': 'paragrafo', 'autor': p.get('autor'), 'visibilidade': p.get('visibilidade')})

        if not itens:
            print('\n\033[33mNenhum texto/parágrafo salvo por você.\033[m')
            input('Pressione ENTER para voltar...')
            return

        while True:
            util.limpar_tela()
            print('=' * 50)
            print(f"      📝 MEUS TEXTOS ({nome})")
            print('=' * 50)
            for i, it in enumerate(itens):
                tipo = 'Texto' if it['tipo'] == 'personalizado' else 'Parágrafo'
                ref = ''
                vis = ''
                snippet = ''
                if it['tipo'] == 'paragrafo':
                    p = next((pp for pp in Usuario.carregar_paragrafos_publicos() if pp.get('id') == it['id']), None)
                    if p:
                        if p.get('paragrafo_numero'):
                            ref = f" - Parágrafo {p.get('paragrafo_numero')}"
                        vis = f" [{p.get('visibilidade')}]" if p.get('visibilidade') else ''
                        texto_full = p.get('texto_original') or p.get('original') or ''
                        snippet = (texto_full[:60] + '...') if len(texto_full) > 60 else texto_full
                else:
                    t = dados.DataManager.buscar_texto_por_id(it['id'])
                    if t:
                        texto_first = ''
                        paragrafos = t.get('Paragrafos', [])
                        if paragrafos:
                            texto_first = paragrafos[0].get('Lingua') or paragrafos[0].get('original') or ''
                        snippet = (texto_first[:60] + '...') if len(texto_first) > 60 else texto_first

                title = it['titulo'] or '[sem título]'
                display = f"{i+1} - {title}{ref}{vis} ({tipo})"
                if snippet:
                    display += f" - {snippet}"
                print(display)
            print('0 - Voltar')
            escolha = input('Opção: ').strip()
            if escolha == '0':
                return
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(itens):
                    it = itens[idx]
                    if para_remover:
                        conf = input(f"Confirma remover '{it['titulo']}'? (s/n): ").strip().lower()
                        if conf == 's':
                            if it['id'] in Usuario.usuario_logado[3]:
                                Usuario.usuario_logado[3].remove(it['id'])
                                Usuario.salvar_usuarios(Usuario.usuarios)
                            if it['tipo'] == 'personalizado':
                                dados.DataManager.remover_texto_personalizado(it['id'], nome)
                            else:
                                if it.get('autor') != nome:
                                    print('\033[31mApenas o autor pode remover este parágrafo público.\033[m')
                                    sleep(1.5)
                                else:
                                    Usuario.remover_paragrafo_publico(it['id'])
                            itens.pop(idx)
                            print('\033[32mRemovido.\033[m')
                            sleep(1)
                    else:
                        if it['tipo'] == 'personalizado':
                            texto = dados.DataManager.buscar_texto_por_id(it['id'])
                            if not texto:
                                print('\033[31mTexto personalizado não encontrado.\033[m')
                                sleep(1.5)
                                continue
                            while True:
                                util.limpar_tela()
                                print('=' * 50)
                                print(f"Título: {texto.get('Titulo') or '[sem título]'}")
                                print(f"Autor: {texto.get('Autor') or '[desconhecido]'}")
                                print(f"Referência: {texto.get('Referencia') or '-'}")
                                print('=' * 50)
                                paragrafos = texto.get('Paragrafos', []) or []
                                for j, p in enumerate(paragrafos):
                                    snippet = (p.get('texto_original') or p.get('original') or p.get('Texto') or '')[:70]
                                    print(f"{j+1} - {snippet}{'...' if len(snippet) >= 70 else ''}")
                                print('0 - Voltar')
                                escolha_p = input('Parágrafo para ver: ').strip()
                                if escolha_p == '0':
                                    break
                                try:
                                    ip = int(escolha_p) - 1
                                    if 0 <= ip < len(paragrafos):
                                        p = paragrafos[ip]
                                        util.limpar_tela()
                                        print('=' * 50)
                                        print('--- ORIGINAL ---')
                                        print(p.get('texto_original') or p.get('original') or p.get('Texto') or '')
                                        print('\n--- TRADUÇÃO (Português) ---')
                                        print(p.get('traducao') or p.get('traducao_portugues') or p.get('traducao_pt') or p.get('Traducao') or '')
                                        print('=' * 50)
                                        while True:
                                            print('\n 1 - Ver/Adicionar Comentários')
                                            print(' 0 - Voltar')
                                            escolha_com = input('Opção: ').strip()
                                            if escolha_com == '0':
                                                break
                                            elif escolha_com == '1':
                                                try:
                                                    import menu_leitura
                                                    menu_leitura.ver_comentarios(f"{texto.get('id')}:{ip}")
                                                except Exception:
                                                    autor = Usuario.usuario_logado[0] if Usuario.usuario_logado else 'Anon'
                                                    txt = input('Digite seu comentário: ').strip()
                                                    if txt:
                                                        dados.DataManager.salvar_comentario(f"{texto.get('id')}:{ip}", autor, txt, 'publico')
                                                    input('Pressione ENTER para voltar...')
                                                break
                                            else:
                                                print('\033[31mOpção inválida.\033[m')
                                                sleep(1)
                                    else:
                                        print('\033[31mParágrafo inválido.\033[m')
                                        sleep(1)
                                except ValueError:
                                    print('\033[31mEntrada inválida.\033[m')
                                    sleep(1)
                        else:
                            p = next((pp for pp in Usuario.carregar_paragrafos_publicos() if pp.get('id') == it['id']), None)
                            if not p:
                                print('\033[31mParágrafo não encontrado.\033[m')
                                sleep(1.5)
                                continue
                            util.limpar_tela()
                            print('=' * 50)
                            print(f"Título: {p.get('titulo') or '[sem título]'}")
                            print(f"Autor: {p.get('autor') or '[desconhecido]'}")
                            print(f"Idioma: {p.get('idioma') or '-'} | Visibilidade: {p.get('visibilidade') or '-'}")
                            print('=' * 50)
                            print('\n--- ORIGINAL ---')
                            print(p.get('texto_original') or p.get('original') or '')
                            print('\n--- TRADUÇÃO (Português) ---')
                            print(p.get('traducao') or p.get('traducao_pt') or '')
                            print('=' * 50)
                            while True:
                                print('\n 1 - Ver/Adicionar Comentários')
                                print(' 0 - Voltar')
                                escolha_c = input('Opção: ').strip()
                                if escolha_c == '0':
                                    break
                                elif escolha_c == '1':
                                    try:
                                        import menu_leitura
                                        menu_leitura.ver_comentarios(p.get('id'))
                                    except Exception:
                                        autor = Usuario.usuario_logado[0] if Usuario.usuario_logado else 'Anon'
                                        txt = input('Digite seu comentário: ').strip()
                                        if txt:
                                            dados.DataManager.salvar_comentario(p.get('id'), autor, txt, 'publico')
                                        input('Pressione ENTER para voltar...')
                                    break
                                else:
                                    print('\033[31mOpção inválida.\033[m')
                                    sleep(1)
                else:
                    print('\033[31mOpção inválida.\033[m')
                    sleep(1)
            except ValueError:
                print('\033[31mEntrada inválida.\033[m')
                sleep(1)

    @staticmethod
    def remover_paragrafo_publico(paragrafo_id):
        paragrafos = Usuario.carregar_paragrafos_publicos()
        antes = len(paragrafos)
        paragrafos = [p for p in paragrafos if p.get('id') != paragrafo_id]
        if len(paragrafos) < antes:
            with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
                json.dump(paragrafos, f, indent=4, ensure_ascii=False)
            return True
        return False

    @staticmethod
    def mostrar_paragrafos_publicos():
        try:
            import menu_leitura
            menu_leitura.menu_ver_paragrafos_publicos()
        except Exception as e:
            print(f"\033[31mErro ao abrir parágrafos públicos: {e}\033[m")
            from time import sleep
            sleep(1.5)

    @staticmethod
    def salvar_usuarios_com_alteracao(usuario_alterado, todos_usuarios):
        for i, u in enumerate(todos_usuarios):
            if u[0] == usuario_alterado[0]:
                todos_usuarios[i] = usuario_alterado
                break
        Usuario.salvar_usuarios(todos_usuarios)

    @staticmethod
    def remover_usuario(usuarios):
        util.limpar_tela()
        print('=' * 50)
        print('      ❌ REMOVER CONTA')
        print('=' * 50)
        nome = input('Nome ou e-mail: ').strip()
        senha = maskpass.askpass(prompt='Senha: ', mask='*').strip()
        idx = -1
        for i, u in enumerate(usuarios):
            if (u[0] == nome or u[2] == nome) and u[1] == senha:
                idx = i
                break
        if idx == -1:
            print('\033[31mUsuário/senha inválidos.\033[m')
            sleep(1.5)
            return False
        conf = input(f"Confirma excluir '{usuarios[idx][0]}'? (s/n): ").strip().lower()
        if conf == 's':
            usuarios.pop(idx)
            Usuario.salvar_usuarios(usuarios)
            print('\033[32mConta excluída.\033[m')
            sleep(1)
            return True
        print('\033[33mCancelado.\033[m')
        sleep(1)
        return False

    @staticmethod
    def obter_indice_usuario(nome_usuario, todos_usuarios):
        for i, u in enumerate(todos_usuarios):
            if u[0] == nome_usuario:
                return i
        return -1

    @staticmethod
    def adicionar_xp_leitura(tempo_total_s, tempo_minimo_s, idioma_key=None):
        if not Usuario.usuario_logado:
            return
        try:
            proporcao = float(tempo_total_s) / float(tempo_minimo_s) if tempo_minimo_s > 0 else 0
        except Exception:
            proporcao = 0
        ganho = int(Usuario.XP_BASE * proporcao)
        if ganho < 1:
            ganho = 1
        if not Usuario.usuarios:
            Usuario.usuarios = Usuario.carregar_usuarios()
        nome = Usuario.usuario_logado[0]
        for i, u in enumerate(Usuario.usuarios):
            if u[0] == nome:
                u[4] = (u[4] if isinstance(u[4], int) else 0) + ganho
                if idioma_key:
                    if not isinstance(u[5], dict):
                        u[5] = {'english': 0, 'french': 0, 'spanish': 0}
                    key = idioma_key.lower()
                    if key in u[5]:
                        u[5][key] = int(u[5].get(key, 0)) + ganho
                Usuario.usuario_logado = u
                break
        Usuario.salvar_usuarios(Usuario.usuarios)
        print(f"\033[32mVocê ganhou {ganho} XP por leitura! XP total: {Usuario.usuario_logado[4]}\033[m")