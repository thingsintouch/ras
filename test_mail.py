import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Email configuration
EMAIL_PROVIDER_SMTP_ADDRESS = 'smtp.gmail.com'
#smtp_port = 587  # Use 587 for TLS or 465 for SSL
#smtp_username = 'ras2logs@thingsintouch.com'
MY_PASSWORD = 'ikgk owvu ldvk mqse'
MY_EMAIL = 'logsras@gmail.com'
receiver_email = 'lu.bu.sax@gmail.com'

def send_email(email, subject, message_text, attachment_filename):

    # Create the email message
    message = MIMEMultipart()
    message['From'] = MY_EMAIL
    message['To'] = email
    message['Subject'] = 'Test Email'

    # Attach the file if provided
    if attachment_filename:
        with open(attachment_filename, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=attachment_filename)

        part['Content-Disposition'] = f'attachment; filename={attachment_filename}'
        message.attach(part)
    
    # Attach the plain text message
    message.attach(MIMEText(message_text, 'plain'))

    with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=email,
            msg=f"Subject:{subject}\n\n{message}".encode('utf-8')
        )

email_text = 'This is a test'
attachment_filename = 'example.txt'
subject = "testing"

send_email(receiver_email, subject, email_text, attachment_filename)