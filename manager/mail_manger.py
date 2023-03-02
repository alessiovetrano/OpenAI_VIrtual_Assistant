import re
import smtplib
from email.mime.text import MIMEText


class MailManager:
    def __init__(self, gpt_manager):
        self.gpt_manager = gpt_manager

    def send_email(self, data):
        # Configura i dati del server SMTP
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'tua email'
        smtp_password = 'tua password'

        # Configura i dati dell'email
        source_name = "nome mittente"
        email_from = smtp_username
        email_to = 'email destinazione'

        email_body = str(self.gpt_manager.ask(data))
        email_body = re.sub("\[.*\]", source_name, email_body)
        email_body += "\n\nQuesta email è stata generata automaticamente da un'intelligenza artificiale."
        email_subject = str(self.gpt_manager.ask("Dammi un oggetto per questa email"))
        email_subject = re.sub("\[.*\]", source_name, email_subject)
        self.gpt_manager.clear_history(4)

        # Crea un oggetto MIMEText per l'email
        msg = MIMEText(email_body)
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = email_subject

        # Crea un oggetto SMTP e connettiti al server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print(smtp_username, smtp_password)
        server.login(smtp_username, smtp_password)

        # Invia l'email
        server.sendmail(email_from, email_to, msg.as_string())

        # Chiudi la connessione SMTP
        server.quit()
