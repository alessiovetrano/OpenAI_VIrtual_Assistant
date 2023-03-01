import smtplib
from email.mime.text import MIMEText


class MailManager:

    def send_email(self):
        # Configura i dati del server SMTP
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'tua mail'
        smtp_password = 'tua pass'

        # Configura i dati dell'email
        email_from = 'tua mail'
        email_to = 'alessio.vetrano001@studenti.uniparthenope.it'
        email_subject = 'Test email'
        email_body = 'Questo è un test di invio email tramite SMTP.'

        # Crea un oggetto MIMEText per l'email
        msg = MIMEText(email_body)
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = email_subject

        # Crea un oggetto SMTP e connettiti al server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print(smtp_username,smtp_password)
        server.login(smtp_username, smtp_password)

        # Invia l'email
        server.sendmail(email_from, email_to, msg.as_string())

        # Chiudi la connessione SMTP
        server.quit()