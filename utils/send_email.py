


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os



from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


from_email = os.getenv('SENDER_EMAIL')
to_email = os.getenv('RECEIVER_EMAIL')
email_password = os.getenv('EMAIL_PASS')

def func_send_email(file_path):
    # Email configuration
    from_email = from_email
    from_password = email_password  # Use an app password if you have 2FA enabled

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "jobs_testing"

    # Attach the email body
    body = "Please find attached the jobs listing."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    try:
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
            msg.attach(part)
    except Exception as e:
        print(f"Could not attach file: {str(e)}")
        return False  # File attachment failed

    try:
        # Connect to the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(from_email, from_password)

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")
        return True  # Email sent successfully

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False  # Failed to send email

    finally:
        server.quit()






