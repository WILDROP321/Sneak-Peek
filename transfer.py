from mailjet_rest import Client
from premailer import transform
import time


def articleNum():
    filename = 'TEXT/articleNum.txt'
    try:
        with open(filename, 'r') as file:
            number_str = file.read().strip()
        return number_str
    
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
        return '000'
    except ValueError:
        print("The file does not contain a valid integer.")
        return '000'


def send_mailjet_email(api_key, api_secret, to_emails, subject, html_content):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                'From': {
                    'Email': 'tosneakpeekinsider@gmail.com',
                    'Name': 'Sneak Peek'
                },
                'To': [{'Email': email} for email in to_emails],
                'Subject': subject,
                'HTMLPart': html_content
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result

def preProcess():
    # Read the HTML content from the file
    with open("HTML/output.html", "r") as file:
        html_content = file.read()

    # Convert the HTML to email-friendly format using Premailer
    email_html = html_content

    # Save the converted HTML to a new file
    with open("HTML/FINAL.html", "w") as file:
        file.write(email_html)
        
        number_str = articleNum()

    time.sleep(2)
    print("Email HTML conversion is complete.")

def Transfer():
    filename = 'TEXT/articleNum.txt'
    with open(filename, 'r') as file:
        number_str = file.read().strip()

    api_key = 'd5ef60491c599b36b27f98772ee6a03e'
    api_secret = '2f834b23972186b7985020734ae00977'
    
    # Load email addresses from the 'emails.txt' file
    with open('TEXT/emails.txt', 'r') as file:
        to_emails = [line.strip() for line in file.readlines()]

    subject = 'Sneak Peek Issue: ' + number_str

    preProcess()

    # Load HTML content from a file
    with open('HTML/FINAL.html', 'r') as file:
        html_content = file.read()

    response = send_mailjet_email(api_key, api_secret, to_emails, subject, html_content)
    print(response.status_code)
    print(response.json())

# Run the Transfer function to send the email
#Transfer()
