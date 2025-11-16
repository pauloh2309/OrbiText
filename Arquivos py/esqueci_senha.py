import smtplib
import email.message
import secrets
from util import limpar_tela
from time import sleep

num_secreto = secrets.token_hex(3)

limpar_tela()

sleep(5)
limpar_tela()
def esqueci_senha(usuarios, user, email_user):
    
    if  len(email_user) <= 0:
        print('\033[31mA área está vazia, favor preencher\033[m\n')
        limpar_tela()
        sleep(5)
        return 
    else:
        print('\033[32mEmail cadastrado, iremos enviar um email para a redefiniçao da senha\033[m\n')
        limpar_tela()
        sleep(5)

    corpo_email = """
    <p>Olá, {},</p>
    <p>Recebemos uma solicitação de redefinição de senha da sua conta no ORBITEXT.</p>
    <p>Para completar o processo e criar uma nova senha, utilize o código ou siga as instruções fornecidas no sistema</p>
    <b>{}</b>
    <p>Se não foi você quem solicitou essa redefinição, ignore este e-mail. A sua senha atual permanecerá a mesma e a sua conta continuará segura.</p>
    <p>Atenciosamente,</p>
    <p> Grupo ORBITEXT.</p>
    """.format(user, num_secreto)

    msg = email.message.Message()
    msg['Subject'] = 'Solicitação de redefinição de senha'
    msg['From'] = 'grupoorbitext@gmail.com'
    msg['To'] = email_user
    password = 'xugajwuhlpqqacrx'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('\033[32mEmail enviado com sucesso!\033[m\n')
    print('\033[33mCaso não encontre na caixa principal, verifique a caixa de spam.\033[m')


    