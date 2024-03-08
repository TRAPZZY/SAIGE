import click
import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.theme import Theme

# Define a custom theme with mixed colors
custom_theme = Theme({
    "info": "cyan",
    "success": "green",
    "error": "bold red",
    "warning": "yellow",
    "recipient": "magenta",
    "subject": "blue",
    "attachments": "bold italic"
})

console = Console(theme=custom_theme)

def display_header():
    saige_art = """
S A I G E
 _    _    ___    _____    _____    ___   
/ |  / |  / _ \  | ____|  | ____|  / _ \  
| |  | | | | | | |  _|    |  _|   | | | | 
| |  | | | |_| | | |___   | |___  | |_| | 
|_|  |_|  \___/  |_____|  |_____|  \___/  
    """
    header_text = Text(saige_art, style="bold magenta")
    header_text.append("\nCreated by trapzzy\n", style="bold blue")
    header_text.append("Contact: traphubs@outlook.com", style="bold green")

    panel = Panel(header_text, expand=False, border_style="bright_yellow", title="[bold cyan]SAIGE Mailer[/bold cyan]", subtitle="[bold yellow]Email Automation Tool[/bold yellow]")
    console.print(panel)

def load_config():
    with open('settings.json', 'r') as config_file:
        return json.load(config_file)

def load_recipients(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def render_template(template_path, context):
    with open(template_path, 'r') as file:
        template = file.read()
    for placeholder, content in context.items():
        template = template.replace(f"{{{{ {placeholder} }}}}", content)
    return template

def create_email(subject, sender_email, receiver_email, body_html):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message.attach(MIMEText(body_html, 'html'))
    return message

def add_attachments_to_email(message, attachments):
    for attachment in attachments:
        part = MIMEBase('application', "octet-stream")
        with open(attachment, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
        message.attach(part)

def send_email(config, message, receiver_email):
    try:
        with smtplib.SMTP(config['smtp']['host'], config['smtp']['port']) as server:
            if config['smtp']['secure']:
                server.starttls()
            server.login(config['smtp']['user'], config['smtp']['pass'])
            server.sendmail(message['From'], receiver_email, message.as_string())
            return "Sent", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error: {e}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def display_summary_table(summary_data):
    display_header()
    print('====================================================================  ')
    print('====================================================================  ')
    table = Table(title="Email Summary", title_style="bold underline")
    table.add_column("Recipient", justify="left", style="recipient")
    table.add_column("Subject", justify="left", style="subject")
    table.add_column("Attachments", justify="left", style="attachments")
    table.add_column("Status", justify="left", style="info")
    table.add_column("Time Sent", justify="left", style="info")

    for data in summary_data:
        recipient, subject, attachments, status, time_sent = data
        table.add_row(recipient, subject, ', '.join(attachments) if attachments else 'None', status, time_sent)

    console.print(table)

@click.command()
@click.option('--subject', help='The subject of the email')
@click.option('--body', help='The body of the email (HTML allowed)')
@click.option('--recipients', help='Path to the file containing recipient email addresses')
@click.option('--template', help='Path to the HTML template file')
@click.option('--attachments', multiple=True, help='List of files to attach to the email')
def main(subject, body, recipients, template, attachments):
    config = load_config()
    recipient_list = load_recipients(recipients) if recipients else load_recipients('recipients.txt')
    summary_data = []

    for recipient in recipient_list:
        # Set a default email body if neither template nor body is provided
        if template:
            with open('email_template.html', 'r') as file:
                body_html = file.read()
            body_html = render_template(body_html, {'name': recipient.split('@')[0]})
        elif body:
            body_html = body
        else:
            body_html = "This is a default email body. Please provide a template or body content."

        email_subject = subject if subject else config['email']['subject']
        email_message = create_email(email_subject, config['email']['from'], recipient, body_html)
        add_attachments_to_email(email_message, attachments)
        status, time_sent = send_email(config, email_message, recipient)
        summary_data.append((recipient, email_subject, attachments, status, time_sent))

    display_summary_table(summary_data)


if __name__ == '__main__':
    main()
