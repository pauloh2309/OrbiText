import json
from os import system
from time import sleep
import verificação

ARQUIVO_USUARIOS = 'usuarios.json'

def limpar_tela():
    system('cls')

def perguntar_usuario():
    return input("Escolha um nome de usuário: ")

def perguntar_email():
    return input("Digite seu email: ").lower()

def perguntar_senha():
    return input("Escolha uma senha: ")

def confirmar_senha():
    return input("Confirme a senha novamente: ")

def perguntar_identificador():
    return input("Nome de usuário ou Email: ").lower()

def perguntar_senha_login():
    return input("Senha: ")

class Usuario:

    @staticmethod
    def carregar_usuarios():
        try:
            with open(ARQUIVO_USUARIOS, 'r') as arquivo:
                return json.load(arquivo)
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
    def cadastrar_usuario(lista_usuarios, nome, email, senha, senha_confirmada):

        for u in lista_usuarios:
            if u[0].lower() == nome.lower():
                return {"status": "erro", "mensagem": f"O usuário '{nome}' já existe."}

        if not verificação.Verificar_dados.validar_email(email):
            return {"status": "erro", "mensagem": "Formato de email inválido."}

        for u in lista_usuarios:
            if len(u) >= 3 and u[2].lower() == email:
                return {"status": "erro", "mensagem": f"O email '{email}' já está em uso."}

        if not verificação.Verificar_dados.verificar_senha(senha):
            return {"status": "erro", "mensagem": "Senha fraca."}

        if senha != senha_confirmada:
            return {"status": "erro", "mensagem": "As senhas não são iguais."}

        lista_usuarios.append([nome, senha, email])
        Usuario.salvar_usuarios(lista_usuarios)

        return {"status": "ok", "mensagem": f"Usuário '{nome}' cadastrado com sucesso!"}

    @staticmethod
    def fazer_login(lista_usuarios, identificador, senha):

        for usuario in lista_usuarios:

            nome_salvo = usuario[0].lower()
            senha_salva = usuario[1]
            email_salvo = usuario[2].lower() if len(usuario) > 2 else None

            if (identificador == nome_salvo or identificador == email_salvo) and senha == senha_salva:
                return {"status": "ok", "mensagem": f"Bem-vindo(a), {usuario[0]}!"}

        return {"status": "erro", "mensagem": "Usuário/Email ou senha incorretos."}

def interface_cadastro():
    limpar_tela()
    print("\n--- Cadastro ---")

    lista = Usuario.carregar_usuarios()

    nome = perguntar_usuario()
    email = perguntar_email()
    senha = perguntar_senha()
    senha2 = confirmar_senha()

    resultado = Usuario.cadastrar_usuario(lista, nome, email, senha, senha2)

    print(resultado["mensagem"])
    sleep(2)
    return resultado["status"] == "ok"

def interface_login():
    limpar_tela()
    print("\n--- Login ---")

    lista = Usuario.carregar_usuarios()

    identificador = perguntar_identificador()
    senha = perguntar_senha_login()

    resultado = Usuario.fazer_login(lista, identificador, senha)

    print(resultado["mensagem"])
    sleep(3)

    return resultado["status"] == "ok"
