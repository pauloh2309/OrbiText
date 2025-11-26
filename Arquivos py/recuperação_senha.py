import smtplib
from email.message import EmailMessage
import secrets
from os import path
from util import limpar_tela
from verificação import Verificar_dados
import usuario
from time import sleep

ARQUIVO_USUARIOS = 'usuarios.json'

class EmailSender:
    """Classe auxiliar para gerenciar o envio de email de recuperação."""
    
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
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(msg['From'], password)
            s.send_message(msg)
            s.quit()
            
            print(f"\033[32mO código de recuperação foi enviado para {email_user}\033[m")
            return num_secreto, True
            
        except Exception as e:
            print(f"\033[31mERRO ao enviar email: {e}\033[m")
            print("\033[31mVerifique a senha de aplicativo ou as configurações do email remetente.\033[m")
            return None, False

class Sistema_de_recuperação:
    
    def __init__(self, usuarios, menu_inicial):
        self.usuarios = usuarios
        self.menu_inicial = menu_inicial
        self.executar_recuperacao()

    def executar_recuperacao(self):
        limpar_tela()
        print("\n--- Recuperação de Senha ---")
        email = str(input("Digite seu email de cadastro: ").strip().lower())
        
        usuario_encontrado = None
        indice_usuario = -1
        
        for i, u in enumerate(self.usuarios):
            if len(u) > 2 and u[2].lower() == email:
                usuario_encontrado = u
                indice_usuario = i
                break

        if not usuario_encontrado:
            print('\033[31mEmail não encontrado.\033[m')
            sleep(3)
            self.menu_inicial()
            return

        user_name = usuario_encontrado[0]
        email_user = usuario_encontrado[2]

        print("Aguarde... enviando código de recuperação.")
        num_secreto, envio_sucesso = EmailSender.enviar_codigo_recuperacao(user_name, email_user)
        
        if envio_sucesso:
            self.verificar_codigo(indice_usuario, num_secreto)
        else:
            print("Não foi possível enviar o código de recuperação. Tente novamente mais tarde.")
            sleep(3)
            self.menu_inicial()
    
    def verificar_codigo(self, indice_usuario, codigo_secreto):
        limpar_tela()
        
        if codigo_secreto is None:
            return 
            
        while True:
            codigo_digitado = input("Digite o código de recuperação que você recebeu por email: ").strip()

            if codigo_digitado == codigo_secreto:
                print('\033[32mCódigo correto!\033[m')
                while True:
                    nova_senha = str(input('Digite sua nova senha (Mínimo de 8 e máximo de 12 caracteres, com letra maiúscula, minúscula, número e caracteres especiais): ').strip())
                    
                    senha_valida = Verificar_dados.verificar_senha(nova_senha)

                    if not senha_valida:
                        print("A senha que você colocou foi considerada fraca. Por favor, escreva uma senha considerada forte.")
                        continue
                    
                    conf_novasenha = str(input('Confirme sua nova senha: ').strip())
                    
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