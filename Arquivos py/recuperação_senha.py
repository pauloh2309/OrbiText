from util import limpar_tela
from time import sleep
import esqueci_senha

def recuperar_senha(usuarios, menu_inicial):
    cont = 0
    limpar_tela()
    print('=-' * 50)
    print('{:^105}'.format('\033[34mRecuperação de senha\033[m'))
    print('=-' * 50)
    print('\nPara efetuar a recuperação de senha, você deverá inserir o e-mail e o código que será enviado!\n')
    email_user = str(input('Insira o e-mail: ').strip().lower())
    for usuario in usuarios:
        if email_user == usuario['email']:
            user = usuario['nome']
            esqueci_senha.esqueci_senha(usuarios, user, email_user)
            codigo_rec = str(input('Insira o código recebido no e-mail: '))
            if codigo_rec == esqueci_senha.num_secreto:
                while cont < 1:
                    nova_senha = str(input('Insira uma nova senha: ').strip())
                    novasenha_tam = len(nova_senha)
                    if novasenha_tam < 6 or novasenha_tam > 20:
                        print('\033[31mA senha não possui a quantidade mínima de 6 caracteres ou excedeu a quantidade máxima de 20!\033[m\n')
                        sleep(5)
                        return
                    if not any(chr.isnumeric() for chr in nova_senha):
                        print('Sua senha não possui pelo menos um número')
                        sleep(5)
                        return
                    if not any(chr.isupper() for chr in nova_senha):
                        print('Sua senha não possui pelo menos uma letra maiúscula')
                        sleep(5)
                        return
                    elif ' ' in nova_senha:
                        print('\033[31mA sua senha possui espaços, remova-os!\033[m\n')
                        sleep(5)
                        return
                    conf_novasenha = str(input('Confirme sua nova senha: ').strip())
                    if conf_novasenha == nova_senha:
                        usuario['senha'] = nova_senha
                        cont = cont + 1
                        menu_inicial()
                    else:
                        cont = 0
            else:
                print('\033[31mO código inserido não corresponde ao enviado para o email\033[m')
                sleep(3)
                menu_inicial()