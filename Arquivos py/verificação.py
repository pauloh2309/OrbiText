import util
from time import sleep
import re

class Verificar_dados:
    
    DOMINIOS_VALIDOS = {
        'gmail.com',
        'hotmail.com',
        'outlook.com',
        'ufrpe.br',
        'yahoo.com', 
    }
    
    @staticmethod
    def verificar_senha(senha):
        cla_especiais = ['!', '@', '#', '$', '%', '¨', '&', '*', '(', ')',
        '-', '_', '=', '+', '[', ']', '{', '}', '\\', '|',
        ';', ':', "'", '"', ',', '<', '.', '>', '/', '?', '§', '°', '¬', '¢', '£', '³', '²', '¹', '¶', '÷', '×', '¤', '~', '`', '´', '^', '¸']
        maiuscula = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        minusculas = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        senhas_faceis = ['12345678', 'qwertyui', 'password'] 

        if not (8 <= len(senha) <= 12):
            print('\033[31mErro: A senha deve ter entre 8 e 12 caracteres.\033[m')
            sleep(2)
            return False
        elif senha in senhas_faceis:
            print('\033[31mErro: Senha considerada fácil, tente outra.\033[m')
            sleep(2)
            return False
        elif not any(c in cla_especiais for c in senha):
            print('\033[31mErro: Senha sem caracteres especiais. Por favor, adicione.\033[m')
            sleep(2)
            return False
        elif not any(c in maiuscula for c in senha):
            print('\033[31mErro: Senha sem letras maiúsculas. Por favor, adicione.\033[m')
            sleep(2)
            return False
        elif not any(c in minusculas for c in senha):
            print('\033[31mErro: Senha sem letras minúsculas. Por favor, adicione.\033[m')
            sleep(2)
            return False
        elif not any(c in numeros for c in senha):
            print('\033[31mErro: Senha sem números. Por favor, adicione.\033[m')
            sleep(2)
            return False
        else:
            print('\033[32mSenha forte e aceita.\033[m')
            return True
    
    @staticmethod
    def validar_email(email):
        email = email.strip().lower()
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.fullmatch(regex, email):
            return False
        
        try:
            dominio = email.split('@')[1]
            
            if dominio in Verificar_dados.DOMINIOS_VALIDOS:
                return True
            else:
                return False
        except IndexError:
            return False