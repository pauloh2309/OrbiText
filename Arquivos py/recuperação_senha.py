import smtplib
from email.message import EmailMessage
import secrets
from os import path
from util import limpar_tela
from verificação import Verificar_dados
import usuario
from time import sleep
import socket
import maskpass

ARQUIVO_USUARIOS = 'usuarios.json'

class EmailSender:
    
    @staticmethod
    def enviar_codigo_recuperacao(user, email_user):
        num_secreto = secrets.token_hex(3)
        
        if not email_user:
            return None, None

        corpo_email = """
        <p>Olá, {},</p>
        <p>Recebemos uma solicitação de redefinição de senha da sua conta no ORBITEXT.</p>
        <p>Para completar o processo e criar uma nova senha, utilize o código ou siga as instruções fornecidas no sistema</p>
        <b>{}</b>
        <p>Se não foi você quem solicitou essa redefinição, ignore este e-mail. A sua senha atual permanecerá a mesma e a sua conta continuará segura.</p>
        <p>Atenciosamente,</p>
        <p> Grupo ORBITEXT.</p>
        """.format(user, num_secreto)

        msg = EmailMessage()
        msg['Subject'] = 'Solicitação de redefinição de senha'
        msg['From'] = 'grupoorbitext@gmail.com'
        msg['To'] = email_user
        password = 'xugajwuhlpqqacrx'
        
        msg.set_content(corpo_email, subtype='html')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('grupoorbitext@gmail.com', password)
                smtp.send_message(msg)
                return num_secreto, True
        
        except (socket.gaierror, smtplib.SMTPConnectError, TimeoutError):
            print('\033[31mErro: Parece que você está sem internet. Verifique sua conexão e tente novamente.\033[m')
            return num_secreto, False
            
        except smtplib.SMTPException:
            print(f"\033[31mERRO: Falha no envio do e-mail (SMTP). Verifique as credenciais ou o endereço de destino.\033[m")
            return num_secreto, False
            
        except Exception as e:
            print(f"\033[31mOcorreu um erro inesperado: {e}. Tente novamente mais tarde.\033[m")
            return num_secreto, False

class Sistema_de_recuperação:
    def __init__(self, usuarios, menu_inicial):
        self.usuarios = usuarios
        self.menu_inicial = menu_inicial
        self.iniciar_recuperacao()

    def encontrar_usuario(self, identificador):
        identificador = identificador.lower()
        for i, user in enumerate(self.usuarios):
            if len(user) > 2 and (user[0].lower() == identificador or user[2].lower() == identificador):
                return i, user[0], user[2]
        return -1, None, None

    def iniciar_recuperacao(self):
        limpar_tela()
        print("\n--- Recuperação de Senha ---")
        identificador = input("Digite seu nome de usuário ou e-mail cadastrado: ").strip()

        indice_usuario, nome_usuario, email_usuario = self.encontrar_usuario(identificador)

        if indice_usuario == -1:
            print("\033[31mUsuário ou e-mail não encontrado.\033[m")
            sleep(3)
            self.menu_inicial()
            return

        print(f"\nEnviando código de recuperação para o e-mail: {email_usuario}")
        
        codigo_secreto, enviado = EmailSender.enviar_codigo_recuperacao(nome_usuario, email_usuario)

        if not enviado:
            sleep(3)
            self.menu_inicial()
            return

        print("\nCódigo enviado. Verifique sua caixa de entrada.")
        sleep(2)
        self.validar_codigo(indice_usuario, codigo_secreto)

    def validar_codigo(self, indice_usuario, codigo_secreto):
        limpar_tela()
        print("\n--- Confirmação de Código ---")
        codigo_inserido = input("Digite o código de 6 dígitos que você recebeu por e-mail: ").strip().lower()
        
        if codigo_inserido == codigo_secreto:
            while True:
                print('Digite sua nova senha (Mínimo de 8 e máximo de 12 caracteres, com letra maiúscula, minúscula, número e caracteres especiais): ')
                nova_senha = maskpass.askpass(prompt='Nova Senha: ', mask='*').strip()
                
                senha_valida = Verificar_dados.verificar_senha(nova_senha)

                if not senha_valida:
                    print("A senha que você colocou foi considerada fraca. Por favor, escreva uma senha considerada forte.")
                    continue
                
                conf_novasenha = maskpass.askpass(prompt='Confirme sua nova senha: ', mask='*').strip()
                
                if conf_novasenha == nova_senha:
                    self.usuarios[indice_usuario][1] = nova_senha 
                    usuario.Usuario.salvar_usuarios(self.usuarios) 
                    
                    print('\033[32mSenha atualizada com sucesso!\033[m')
                    sleep(3)
                    self.menu_inicial()
                    return
                else:
                    print('\033[31mA Senha de confirmação não confere. Por favor, comece novamente o processo de seleção de senha.\033[m')
                    sleep(3)
                    self.menu_inicial()
                    return
        else:
            print('\033[31mO código inserido não corresponde ao enviado para o email\033[m')
            sleep(3)
            self.menu_inicial()
            return