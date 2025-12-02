import unicodedata
import re
from os import system, name
import webbrowser

def limpar_tela():
    system('cls' if name == 'nt' else 'clear')

def redirecionador():
    webbrowser.open()

def normalize_text(text):
    """Normaliza o texto (lower, sem acentos, sem espaços) para ser usado como chave de dicionário."""
    text = text.lower().strip()
 
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
   
    text = re.sub(r'[^a-z0-9]', '', text)
    return text