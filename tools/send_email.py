import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace these with your actual SMTP credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = ""
SENDER_PASSWORD = ""  # Use App Password for Gmail


def send_email(to_email: str, subject: str, body: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False
    
def escalate_ticket_with_email(issue: str) -> dict:
    subject = "Escalation: Unresolved IT Issue"
    body = f"""
    Hello IT Support Team,

    The following issue reported by a user could not be resolved by the AI Assistant:

    "{issue}"

    Please investigate and take further action.

    Regards,
    AI Notification Agent
    """

    success = send_email(to_email="kartikvadhwana7@gmail.com", subject=subject, body=body)
    return {"content": "📧 Email sent to IT support." if success else "⚠️ Failed to send email."}

