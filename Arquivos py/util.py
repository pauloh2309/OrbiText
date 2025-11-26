from os import system, name
import webbrowser

def limpar_tela():
    system('cls' if name == 'nt' else 'clear')

def redirecionador():
    webbrowser.open()