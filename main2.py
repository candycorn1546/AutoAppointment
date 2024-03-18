import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "sendfrompysms@outlook.com"
receiver_email = "vyfrommo@gmail.com"
password = "RandomPasswordForMail1."

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Test Email"
msg['X-Priority'] = '1'

body = "This is a test email sent from Python through Outlook."
msg.attach(MIMEText(body, 'plain'))

smtp_server = "smtp.office365.com"
smtp_port = 587

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print("Email sent successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
