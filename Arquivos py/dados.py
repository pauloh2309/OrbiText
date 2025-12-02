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
        data = DataManager.carregar_comentarios()
        paragrafo_id_str = str(paragrafo_id)
        
        if paragrafo_id_str not in data:
            data[paragrafo_id_str] = {'publicos': [], 'privados': {}}
            
        comentario = {'autor': autor, 'texto': texto}
        
        if tipo == 'publico':
            data[paragrafo_id_str]['publicos'].append(comentario)
        elif tipo == 'privado':
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
    def mostrar_rankings_gerais():
        usuarios_data = usuario.Usuario.carregar_usuarios()
        
        rankings = sorted(usuarios_data, key=lambda x: x[4], reverse=True)
        
        util.limpar_tela()
        print('=' * 50)
        print("      🏆 RANKING GERAL DE XP")
        print('=' * 50)
        
        for i, user in enumerate(rankings):
            nome = user[0]
            xp = user[4]
            nivel = usuario.Usuario.calcular_nivel(xp)
            emoji = usuario.Usuario.obter_emoji_nivel(nivel)
            
            print(f" {i+1}º | {nome}: \033[33m{nivel} {emoji}\033[m ({xp} XP)")
            
        print('=' * 50)
        input("Pressione ENTER para voltar ao Menu Principal...")