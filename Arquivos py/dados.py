import json
from os import path
from time import sleep, time
import usuario
import menu_leitura
import verificação
import util
import os

NOME_ARQUIVO = 'textos_idiomas.json'
ARQUIVO_PUBLICOS = 'paragrafos_publicos.json'
ARQUIVO_COMENTARIOS = 'comentarios.json'
ARQUIVO_LIKES = 'likes.json'

class DataManager:
    IDIOMAS_MAP = {
        '1': 'english',
        '2': 'french',
        '3': 'spanish',
    }
    
    IDIOMAS_NOMES = {
        'english': 'Inglês',
        'french': 'Francês',
        'spanish': 'Espanhol'
    }

    @staticmethod
    def carregar_textos_idiomas():
        if path.exists(NOME_ARQUIVO):
            with open(NOME_ARQUIVO, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"english": [], "french": [], "spanish": []}
        return {"english": [], "french": [], "spanish": []}

    @staticmethod
    def salvar_textos_idiomas(data):
        with open(NOME_ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def gerar_novo_id():
        return str(int(time() * 1000))

    @staticmethod
    def salvar_texto_personalizado(titulo, idioma_original, lista_paragrafos):
        data = DataManager.carregar_textos_idiomas()
        
        idioma_key = idioma_original.lower()
        if idioma_key not in data:
            data[idioma_key] = []
            
        novo_id = DataManager.gerar_novo_id()
        autor = usuario.Usuario.usuario_logado[0] if usuario.Usuario.usuario_logado else 'Desconhecido'
        
        paragrafos_formatados = []
        for p in lista_paragrafos:
            paragrafos_formatados.append({
                "Lingua": p['original'], 
                "portugues": p['traducao']
            })
            
        novo_texto = {
            "id": novo_id,
            "Titulo": titulo,
            "Paragrafos": paragrafos_formatados,
            "Autor": autor,
            "Referencia": "Texto Personalizado",
            "Nome_Idioma_Exibicao": idioma_original
        }
        
        data[idioma_key].append(novo_texto)
        DataManager.salvar_textos_idiomas(data)
        
        if usuario.Usuario.usuario_logado:
            usuario.Usuario.usuario_logado[3].append(novo_id)
            usuario.Usuario.salvar_usuarios(usuario.Usuario.usuarios)
            
        print(f"\033[32mTexto '{titulo}' salvo com sucesso!\033[m")
        sleep(2)
        
    @staticmethod
    def remover_texto_personalizado(texto_id, autor):
        data = DataManager.carregar_textos_idiomas()
        encontrado = False
        
        for idioma_key in data:
            textos_antes = len(data[idioma_key])
            data[idioma_key] = [
                texto for texto in data[idioma_key] 
                if not (texto.get("id") == texto_id and texto.get("Autor") == autor)
            ]
            textos_depois = len(data[idioma_key])
            
            if textos_depois < textos_antes:
                encontrado = True
                break

        if encontrado:
            DataManager.salvar_textos_idiomas(data)
            
            user_data = usuario.Usuario.usuario_logado
            if user_data and texto_id in user_data[3]:
                user_data[3].remove(texto_id)
                usuario.Usuario.salvar_usuarios(usuario.Usuario.usuarios)
            
            return True
        return False
        
    @staticmethod
    def buscar_texto_por_id(texto_id):
        data = DataManager.carregar_textos_idiomas()
        for idioma_key in data:
            for texto in data[idioma_key]:
                if texto.get("id") == texto_id:
                    return texto
        return None

    @staticmethod
    def carregar_comentarios():
        if path.exists(ARQUIVO_COMENTARIOS):
            with open(ARQUIVO_COMENTARIOS, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    @staticmethod
    def salvar_comentarios(data):
        with open(ARQUIVO_COMENTARIOS, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def salvar_comentario(paragrafo_id, autor, texto, tipo='publico'):
        paragrafos = DataManager.carregar_paragrafos_publicos()
        encontrado = False
        for p in paragrafos:
            if p.get('id') == str(paragrafo_id):
                encontrado = True
                
                if tipo == 'publico' and p.get('visibilidade') == 'privado':
                    return False
                if tipo == 'publico':
                    p.setdefault('comentarios_publicos', []).append({'autor': autor, 'texto': texto})
                else:
                    privados = p.setdefault('comentarios_privados', {})
                    privados.setdefault(autor, []).append({'texto': texto})
                break

        if encontrado:
            with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
                json.dump(paragrafos, f, indent=4, ensure_ascii=False)
            return True

        data = DataManager.carregar_textos_idiomas()
        for idioma_key in data:
            for texto_obj in data[idioma_key]:
                if texto_obj.get('id') == str(paragrafo_id):
                    texto_obj.setdefault('comentarios_publicos', []).append({'autor': autor, 'texto': texto} if tipo == 'publico' else {'autor': autor, 'texto': texto})
                    DataManager.salvar_textos_idiomas(data)
                    return
                if isinstance(paragrafo_id, str) and ':' in paragrafo_id:
                    tid, idx = paragrafo_id.split(':', 1)
                    if texto_obj.get('id') == tid:
                        try:
                            idxn = int(idx)
                        except Exception:
                            continue
                        pargs = texto_obj.get('Paragrafos', [])
                        if 0 <= idxn < len(pargs):
                            par = pargs[idxn]
                            if tipo == 'publico':
                                par.setdefault('comentarios_publicos', []).append({'autor': autor, 'texto': texto})
                            else:
                                cp = par.setdefault('comentarios_privados', {})
                                cp.setdefault(autor, []).append({'texto': texto})
                            DataManager.salvar_textos_idiomas(data)
                            return

        data = DataManager.carregar_comentarios()
        paragrafo_id_str = str(paragrafo_id)
        if paragrafo_id_str not in data:
            data[paragrafo_id_str] = {'publicos': [], 'privados': {}}
        comentario = {'autor': autor, 'texto': texto}
        if tipo == 'publico':
            data[paragrafo_id_str]['publicos'].append(comentario)
        else:
            if autor not in data[paragrafo_id_str]['privados']:
                data[paragrafo_id_str]['privados'][autor] = []
            data[paragrafo_id_str]['privados'][autor].append(comentario)
        DataManager.salvar_comentarios(data)

    @staticmethod
    def carregar_paragrafos_publicos(visibilidade=None, autor=None):
        if path.exists(ARQUIVO_PUBLICOS):
            with open(ARQUIVO_PUBLICOS, 'r', encoding='utf-8') as f:
                try:
                    paragrafos = json.load(f)
                except json.JSONDecodeError:
                    paragrafos = []
        else:
            paragrafos = []

        if visibilidade:
            paragrafos = [p for p in paragrafos if p.get('visibilidade') == visibilidade]
        
        if autor:
            paragrafos = [p for p in paragrafos if p.get('autor') == autor]
            
        return paragrafos

    @staticmethod
    def salvar_paragrafo_publico(titulo, idioma, texto_original, traducao, visibilidade, paragrafo_numero=None, texto_id=None):
        paragrafos = DataManager.carregar_paragrafos_publicos()
        autor = usuario.Usuario.usuario_logado[0] if usuario.Usuario.usuario_logado else 'Desconhecido'
        
        novo_id = DataManager.gerar_novo_id()
        
        novo_paragrafo = {
            'id': novo_id,
            'autor': autor,
            'idioma': idioma,
            'texto_original': texto_original,
            'traducao': traducao,
            'titulo': titulo,
            'visibilidade': visibilidade, 
            'paragrafo_numero': paragrafo_numero,
            'texto_id': texto_id 
        }
        
        paragrafos.append(novo_paragrafo)
        
        with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
            json.dump(paragrafos, f, indent=4, ensure_ascii=False)
            
        return novo_id

    @staticmethod
    def remover_paragrafo_publico(paragrafo_id):
        paragrafos = DataManager.carregar_paragrafos_publicos()
        paragrafos_antes = len(paragrafos)
        
        paragrafos = [p for p in paragrafos if p.get('id') != paragrafo_id]
        
        if len(paragrafos) < paragrafos_antes:
            with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
                json.dump(paragrafos, f, indent=4, ensure_ascii=False)
            return True
        return False
    
    @staticmethod
    def publicar_paragrafo(paragrafo_id):
        paragrafos = DataManager.carregar_paragrafos_publicos()
        encontrado = False
        for p in paragrafos:
            if p.get('id') == paragrafo_id and p.get('visibilidade') == 'privado':
                p['visibilidade'] = 'publico'
                encontrado = True
                break
        
        if encontrado:
            with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
                json.dump(paragrafos, f, indent=4, ensure_ascii=False)
            return True
        return False

    @staticmethod
    def remover_paragrafos_por_autor(autor):
        if not path.exists(ARQUIVO_PUBLICOS):
            return 0
            
        paragrafos = DataManager.carregar_paragrafos_publicos()
        paragrafos_antes = len(paragrafos)
        
        paragrafos = [p for p in paragrafos if p.get('autor') != autor]
        
        if len(paragrafos) < paragrafos_antes:
            with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
                json.dump(paragrafos, f, indent=4, ensure_ascii=False)
            return paragrafos_antes - len(paragrafos)
        return 0

    @staticmethod
    def carregar_likes():
        """Carrega estrutura de likes: {usuario_nome: {paragrafo_id: True, comentario_id: True, ...}}"""
        if path.exists(ARQUIVO_LIKES):
            with open(ARQUIVO_LIKES, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    @staticmethod
    def salvar_likes(data):
        """Salva estrutura de likes"""
        with open(ARQUIVO_LIKES, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def curtir_paragrafo(paragrafo_id, usuario_nome):
        """Adiciona um like anônimo de um usuário a um parágrafo. Retorna True se adicionou, False se já havia"""
        likes_data = DataManager.carregar_likes()
        if usuario_nome not in likes_data:
            likes_data[usuario_nome] = {}
        
        
        chave = f"p:{paragrafo_id}"
        if chave in likes_data[usuario_nome]:
            return False  
        
        
        paragrafos = DataManager.carregar_paragrafos_publicos()
        for p in paragrafos:
            if p.get('id') == str(paragrafo_id):
                p.setdefault('likes', []).append(usuario_nome)
                with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
                    json.dump(paragrafos, f, indent=4, ensure_ascii=False)
                break
        
        
        likes_data[usuario_nome][chave] = True
        DataManager.salvar_likes(likes_data)
        return True

    @staticmethod
    def descurtir_paragrafo(paragrafo_id, usuario_nome):
        """Remove o like de um usuário de um parágrafo. Retorna True se removeu, False se não havia"""
        likes_data = DataManager.carregar_likes()
        if usuario_nome not in likes_data:
            return False
        
        chave = f"p:{paragrafo_id}"
        if chave not in likes_data[usuario_nome]:
            return False  
        
        
        paragrafos = DataManager.carregar_paragrafos_publicos()
        for p in paragrafos:
            if p.get('id') == str(paragrafo_id):
                if usuario_nome in p.get('likes', []):
                    p['likes'].remove(usuario_nome)
                with open(ARQUIVO_PUBLICOS, 'w', encoding='utf-8') as f:
                    json.dump(paragrafos, f, indent=4, ensure_ascii=False)
                break
        
        
        del likes_data[usuario_nome][chave]
        if not likes_data[usuario_nome]:
            del likes_data[usuario_nome]
        DataManager.salvar_likes(likes_data)
        return True

    @staticmethod
    def usuario_curtiu_paragrafo(paragrafo_id, usuario_nome):
        """Verifica se um usuário já curtiu um parágrafo"""
        likes_data = DataManager.carregar_likes()
        if usuario_nome not in likes_data:
            return False
        chave = f"p:{paragrafo_id}"
        return chave in likes_data[usuario_nome]

    @staticmethod
    def obter_likes_paragrafo(paragrafo_id):
        """Retorna lista de nomes de usuários que curtiram o parágrafo (anônimo de verdade na exibição, mas rastreado internamente)"""
        paragrafos = DataManager.carregar_paragrafos_publicos()
        for p in paragrafos:
            if p.get('id') == str(paragrafo_id):
                return len(p.get('likes', []))
        return 0

    @staticmethod
    def curtir_comentario(comentario_id, usuario_nome):
        """Adiciona um like anônimo a um comentário. comentario_id pode ser um índice ou id único"""
        likes_data = DataManager.carregar_likes()
        if usuario_nome not in likes_data:
            likes_data[usuario_nome] = {}
        
        chave = f"c:{comentario_id}"
        if chave in likes_data[usuario_nome]:
            return False  
        
        likes_data[usuario_nome][chave] = True
        DataManager.salvar_likes(likes_data)
        return True

    @staticmethod
    def descurtir_comentario(comentario_id, usuario_nome):
        """Remove o like de um usuário de um comentário"""
        likes_data = DataManager.carregar_likes()
        if usuario_nome not in likes_data:
            return False
        
        chave = f"c:{comentario_id}"
        if chave not in likes_data[usuario_nome]:
            return False
        
        del likes_data[usuario_nome][chave]
        if not likes_data[usuario_nome]:
            del likes_data[usuario_nome]
        DataManager.salvar_likes(likes_data)
        return True

    @staticmethod
    def usuario_curtiu_comentario(comentario_id, usuario_nome):
        """Verifica se um usuário já curtiu um comentário"""
        likes_data = DataManager.carregar_likes()
        if usuario_nome not in likes_data:
            return False
        chave = f"c:{comentario_id}"
        return chave in likes_data[usuario_nome]

    @staticmethod
    def obter_likes_comentario(comentario_id):
        """Retorna o número de likes de um comentário"""
        likes_data = DataManager.carregar_likes()
        count = 0
        chave = f"c:{comentario_id}"
        for user_likes in likes_data.values():
            if chave in user_likes:
                count += 1
        return count

    @staticmethod
    def mostrar_rankings_gerais():
        while True:
            util.limpar_tela()
            print('=' * 50)
            print('      🏆 RANKINGS - GERAL e POR IDIOMA')
            print('=' * 50)
            print(' 1 - Ranking Geral (XP total)')
            print(' 2 - Ranking Inglês')
            print(' 3 - Ranking Francês')
            print(' 4 - Ranking Espanhol')
            print(' 5 - Ranking de Textos por Salvamentos (parágrafos públicos)')
            print(' 0 - Voltar')
            print('=' * 50)

            escolha = input('Opção: ').strip()
            if escolha == '0':
                return

            usuarios_data = usuario.Usuario.carregar_usuarios()
            if not usuarios_data:
                print('\033[33mNenhum usuário cadastrado ainda.\033[m')
                input('Pressione ENTER para voltar...')
                return

            
            usuarios_norm = []
            for u in usuarios_data:
                try:
                    nome = u[0] if len(u) > 0 else 'Anon'
                except Exception:
                    nome = 'Anon'
                
                xp = 0
                try:
                    if len(u) > 4 and (isinstance(u[4], int) or (isinstance(u[4], str) and str(u[4]).isdigit())):
                        xp = int(u[4])
                except Exception:
                    xp = 0
                
                xp_por_idioma = {'english': 0, 'french': 0, 'spanish': 0}
                try:
                    if len(u) > 5 and isinstance(u[5], dict):
                        for k in xp_por_idioma.keys():
                            xp_por_idioma[k] = int(u[5].get(k, 0)) if isinstance(u[5].get(k, 0), int) or (isinstance(u[5].get(k, 0), str) and str(u[5].get(k, 0)).isdigit()) else 0
                except Exception:
                    pass
                usuarios_norm.append({'raw': u, 'nome': nome, 'xp': xp, 'xp_por_idioma': xp_por_idioma})

            if escolha == '1':
                rankings = sorted(usuarios_norm, key=lambda x: x['xp'], reverse=True)
                util.limpar_tela()
                print('=' * 50)
                print('      🏆 RANKING GERAL DE XP')
                print('=' * 50)
                for i, user in enumerate(rankings):
                    nome = user['nome']
                    xp = user['xp']
                    nivel = usuario.Usuario.calcular_nivel(xp)
                    emoji = usuario.Usuario.obter_emoji_nivel(nivel)
                    print(f" {i+1}º | {nome}: \033[33m{nivel} {emoji}\033[m ({xp} XP)")
                print('=' * 50)
                input('Pressione ENTER para voltar...')

            elif escolha in ['2', '3', '4']:
                idioma_map = {'2': 'english', '3': 'french', '4': 'spanish'}
                idioma = idioma_map[escolha]
                rankings = sorted(usuarios_norm, key=lambda x: x['xp_por_idioma'].get(idioma, 0), reverse=True)
                util.limpar_tela()
                print('=' * 50)
                print(f'      🏁 RANKING - {idioma.capitalize()}')
                print('=' * 50)
                for i, user in enumerate(rankings):
                    nome = user['nome']
                    xp_idioma = user['xp_por_idioma'].get(idioma, 0)
                    nivel = usuario.Usuario.calcular_nivel(xp_idioma)
                    emoji = usuario.Usuario.obter_emoji_nivel(nivel, tipo='idioma')
                    print(f" {i+1}º | {nome}: \033[33m{nivel} {emoji}\033[m ({xp_idioma} XP - {idioma})")
                print('=' * 50)
                input('Pressione ENTER para voltar...')
            elif escolha == '5':
                DataManager.mostrar_rank_textos_por_salvamentos()
            else:
                print('\033[31mOpção inválida.\033[m')
                sleep(1.5)

    @staticmethod
    def mostrar_rank_textos_por_salvamentos():
        usuarios_data = usuario.Usuario.carregar_usuarios()
        parag_counts = {}
        for u in usuarios_data:
            try:
                ids = u[3]
            except Exception:
                ids = []
            for pid in ids:
                parag_counts[pid] = parag_counts.get(pid, 0) + 1

        paragrafos = DataManager.carregar_paragrafos_publicos()
        textos_map = {}
        for p in paragrafos:
            pid = p.get('id')
            tid = p.get('texto_id')
            saves = parag_counts.get(pid, 0)
            if tid:
                entry = textos_map.setdefault(tid, {'titulo': None, 'total': 0, 'paragrafos': []})
                entry['total'] += saves
                entry['paragrafos'].append({'id': pid, 'titulo': p.get('titulo'), 'paragrafo_numero': p.get('paragrafo_numero'), 'saves': saves})
            else:
                textos_map.setdefault('__soltos__', {'titulo': 'Parágrafos Soltos', 'total': 0, 'paragrafos': []})
                textos_map['__soltos__']['paragrafos'].append({'id': pid, 'titulo': p.get('titulo'), 'paragrafo_numero': p.get('paragrafo_numero'), 'saves': saves})

        ranking = sorted([(tid, v) for tid, v in textos_map.items()], key=lambda x: x[1]['total'], reverse=True)

        util.limpar_tela()
        print('=' * 50)
        print('      🏷️  RANKING DE TEXTOS POR SALVAMENTOS')
        print('=' * 50)

        for i, (tid, info) in enumerate(ranking[:10]):
            titulo = info.get('titulo')
            if not titulo and tid != '__soltos__':
                t = DataManager.buscar_texto_por_id(tid)
                titulo = t.get('Titulo') if t else '[Título desconhecido]'
            print(f"{i+1} - {titulo} : {info.get('total',0)} salvamentos")
            par_sorted = sorted(info['paragrafos'], key=lambda x: x['saves'], reverse=True)
            for p in par_sorted[:10]:
                ref = f"Parágrafo {p.get('paragrafo_numero')} - " if p.get('paragrafo_numero') else ''
                print(f"    - {ref}{p.get('titulo') or '[sem título]'} : {p.get('saves',0)} salvamentos (id:{p.get('id')})")
        print('=' * 50)
        input('Pressione ENTER para voltar...')