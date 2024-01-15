import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'YOUR EMAIL'
sender_password = 'YOUR EMAIL TOKEN'


def send_email(receiver_email, subject, content, sender_email=sender_email, sender_password=sender_password):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)

        # Define the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        message.attach(MIMEText(content, 'html'))

        # Send the email
        smtp.send_message(message)
    print('Mail Sent!!')
