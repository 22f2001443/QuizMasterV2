import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os

# SMTP configuration
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT" ,1025)  # Change to 587 for real SMTP servers
FROM_EMAIL = 'admin@quizpilot.com'

# Jinja environment setup
template_dir = os.path.join(os.path.dirname(__file__), '../../controller/tasks/send_emails/html_templates')
env = Environment(loader=FileSystemLoader(template_dir))


def render_template(template_name, context):
    """
    Renders a Jinja2 HTML template with context data.
    """
    template = env.get_template(template_name)
    return template.render(context)


def send_email(to, subject, template_name, context):
    """
    Sends an email using a Jinja2-rendered HTML template.
    """
    # Render HTML from template
    html_content = render_template(template_name, context)

    # Create MIME message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to

    msg.attach(MIMEText(html_content, 'html'))

    # Send the email
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.connect(SMTP_HOST, SMTP_PORT)  # <-- Explicit connection
            server.ehlo()
            server.send_message(msg)
            print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email to {to}: {e}")