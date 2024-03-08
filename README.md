# SAIGE Mailer

SAIGE Mailer is an advanced email automation tool designed to send personalized emails with attachments. It provides a command-line interface for easy use and customization.

## Features

- Send emails with personalized HTML content.
- Attach multiple files to emails.
- Load recipient list from a text file.
- Use HTML templates for email body.
- Display a summary of sent emails in a structured table.
- Colorful CLI output for better readability.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/saige-mailer.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```
python mailer.py --subject "Your Subject" --body "Your Email Body" --recipients "path/to/recipients.txt" --template "path/to/template.html" --attachments "file1.pdf" "file2.jpg"
```

## Configuration

Update the `settings.json` file with your SMTP server details and other configurations.

## Creator

**trapzzy**

- Contact: [traphubs@outlook.com](mailto:traphubs@outlook.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
