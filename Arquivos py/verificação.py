import json
from os import system
from time import sleep
import re
import menu_principal1

ARQUIVO_USUARIOS = 'usuarios.json'

def carregar_usuarios():
    try:
        with open(ARQUIVO_USUARIOS, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Aviso: Arquivo de usuários JSON corrompido ou vazio. Iniciando com lista vazia.")
        return []

def salvar_usuarios(lista_usuarios):
    try:
        with open(ARQUIVO_USUARIOS, 'w') as arquivo:
            json.dump(lista_usuarios, arquivo, indent=4) 
    except Exception as e:
        print(f"ERRO ao salvar usuários: {e}")

usuarios = carregar_usuarios() 

def validar_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.fullmatch(regex, email):
        return True
    else:
        return False

def verificar_senha(senha):
    cla_especiais = ['!', '@', '#', '$', '%', '¨', '&', '*', '(', ')',
    '-', '_', '=', '+', '[', ']', '{', '}', '\\', '|',
    ';', ':', "'", '"', ',', '<', '.', '>', '/', '?', '§', '°', '¬', '¢', '£', '³', '²', '¹', '¶', '÷', '×', '¤', '~', '`', '´', '^', '¸']
    maiuscula = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    minusculas = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    senhas_faceis = ["123456", "qwerty123", "qwerty1", "123456789", "12345678", "12345", "102030", "admin", "Brasil", "Qwerty123", "1234567", "Qwerty1!", "Qwerty123!", "password", "1234", "baseball", "dragon", "football", "monkey", "letmein", "abc123", "111111", "mustang", "access", "shadow", "master", "michael", "superman", "696969", "123123", "batmanQwerty12", "Qwerty1234", "Qwerty1?", "1234567890", "Qwerty123?", "Qwerty1"]
    
    if len(senha) < 8:
        print('senha com poucas letras, ela deve ter mais de 8 caracteres')
        sleep(2)
        return False 
    elif len(senha) > 12:
        print('senha muito grande, ela deve ter menos de 12 caracteris')
        sleep(2)
        return False
    elif senha in senhas_faceis:
        print('senha considerada facil, tente outra')
        sleep(2)
        return False
    elif not any(c in cla_especiais for c in senha):
        print('senha sem caracteres especiais, por favor os coloque.')
        sleep(2)
        return False
    elif not any(c in maiuscula for c in senha):
        print('senha sem letras maiusculas, por favor adicione.')
        sleep(2)
        return False
    elif not any(c in minusculas for c in senha):
        print('senha sem letras minusculas, por favor adicione.')
        sleep(2)
        return False
    elif not any(c in numeros for c in senha):
        print('senha sem numeros, por favor adicione.')
        sleep(2)
        return False
    else:
        print('Senha forte e aceita.')
        sleep(2)
        return True
    
def cadastrar_usuario(lista_usuarios):
    system('cls') 
    print("\n--- Cadastro ---")
    novo_usuario = input("Escolha um nome de usuário: ")

    for u in lista_usuarios:
        if u[0] == novo_usuario:
            print(f"ERRO: O usuário '{novo_usuario}' já existe.")
            sleep(2) 
            return 
            
    while True:
        novo_email = input("Digite seu email: ").lower()
        if validar_email(novo_email):
            break
        else:
            print("ERRO: Formato de email inválido. Tente novamente.")
            sleep(2)
            
    for u in lista_usuarios:
        if len(u) > 2 and u[2].lower() == novo_email:
            print(f"ERRO: O email '{novo_email}' já está em uso.")
            sleep(2) 
            return
            
    nova_senha = input("Escolha uma senha: ")
    senha2 = input('Escreva a senha novamente:')
    
    if nova_senha != senha2:
        print('Senhas não são iguais')
        sleep(2)
        return

    senha_valida = verificar_senha(nova_senha)

    if not senha_valida: 
        print("Não foi possível cadastrar. Tente novamente.")
        sleep(2)
        return
    
    lista_usuarios.append([novo_usuario, nova_senha, novo_email])
    salvar_usuarios(lista_usuarios) 

    print(f"Usuário '{novo_usuario}' cadastrado com sucesso!")
    sleep(2)


def fazer_login(lista_usuarios):
    system('cls') 
    print("\n--- Login ---")
    
    identificador_digitado = input("Nome de usuário ou Email: ").lower() 
    senha_digitada = input("Senha: ")
    
    for usuario in lista_usuarios:
        
        nome_usuario_salvo = usuario[0].lower()
        senha_salva = usuario[1]
        email_salvo = usuario[2].lower() if len(usuario) > 2 else None
        
        if (identificador_digitado == nome_usuario_salvo or 
            identificador_digitado == email_salvo) and \
           senha_digitada == senha_salva:
            
            system('cls')
            print(f"\nLogin bem-sucedido! Bem-vindo(a), {usuario[0]}!") 
            sleep(3)
            menu_principal1.orbitext() 
            return True 
    
    system('cls')
    print("\nErro: Nome de usuário/Email ou senha incorretos.")
    sleep(3)
    return False