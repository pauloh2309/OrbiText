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
        senhas_faceis = ["123456", "qwerty1", "senha123", "password"]
        
        if len(senha) < 8:
            print('senha com poucas letras, ela deve ter mais de 8 caracteres')
            sleep(2)
            return False 
        elif len(senha) > 12:
            print('senha muito grande, ela deve ter menos de 12 caracteres')
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