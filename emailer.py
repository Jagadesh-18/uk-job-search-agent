import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

def send_digest_email(subject, body):
    sender=os.getenv("EMAIL_ADDRESS")
    password=os.getenv("EMAIL_APP_PASSWORD")
    
    if not sender or not password:
        print("Email credentials not set, skipping email.")
        return False
    
    msg = EmailMessage()
    msg["Subject"]=subject
    msg["From"]=sender
    msg["To"]=sender
    msg.set_content(body)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender,password)
        server.send_message(msg)
    return True