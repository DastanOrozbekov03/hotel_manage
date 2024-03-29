from __future__ import absolute_import, unicode_literals
from celery import shared_task
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@shared_task
def send_email_task(subject, message, recipient_list):
    # Настройки SMTP сервера
    smtp_host = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'cluffymonkey56@gmail.com'
    smtp_password = 'alagcfzfbvhjeugw'

    # Формирование письма
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ', '.join(recipient_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Подключение к SMTP серверу и отправка письма
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_list, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
