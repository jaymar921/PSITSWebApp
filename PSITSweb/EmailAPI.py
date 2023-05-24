import requests

from Models import Email
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def pushEmail(email: Email):
    try:
        # DO NOT SHARE THIS API KEY AND API SECRET
        headers = {
            'X-MAGICBELL-API-SECRET': '',
            'X-MAGICBELL-API-KEY': '',
        }
        data = {
            "notification": {
                "title": email.title,
                "content": email.content,
                "category": "new_message",
                # "action_url": "https://developer.magicbell.com",
                "recipients": [{
                    "email": email.recipient
                }],
                "custom_attributes": {
                    "order": {
                        "id": "1202983",
                        "title": "A title you can use in your templates"
                    }
                }
            }
        }

        response = requests.post('https://api.magicbell.com/notifications', headers=headers, json=data)
        print(f'An email was sent to {email.recipient}')
    except:
        print(f'There was an error sending email to {email.recipient}')
        None

def email_verification(email: Email):
    # Send an HTML email with an embedded image and a plain text message for
    # email clients that don't want to display the HTML.

    # Define these once; use them twice!
    strFrom = '----------------------'
    strTo = email.recipient  # RECEIPIENT EMAIL HERE
    try:
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = email.title
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)
        # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText(
            f"""
            <html>
            <body style="background-color: #074873;padding: 25px;">
                <div style="position: absolute;width: 250px;left: 50%;top: 50%;transform: translate(-50%,-50%);text-align: center;border: 1px solid white;background-color: white;padding: 20px;border-radius: 15px;">
                    <div style="width: 100%;">
                        <img style="width: 64px;height: 64px;" src="http://103.44.234.157:5000/static/images/uc.png">
                        <img style="width: 64px;height: 64px;" src="http://103.44.234.157:5000/static/images/PSITS_LOGO.png">
                        <img style="width: 64px;height: 64px;" src="http://103.44.234.157:5000/static/images/CCS_LOGO.png">
                    </div>
                    <h3>{email.title}</h3>
                    <p>{email.content}</p>
                </div>
            </body>
            </html>
            """, 'html'
        )
        msgAlternative.attach(msgText)

        # Send the email (this example assumes SMTP authentication is required)
        import smtplib

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('----------------------','----------------------')
        mail.sendmail(strFrom, strTo, msgRoot.as_string())
        mail.quit()
        print(f"Success : Registration email was sent to {email.recipient}")
        return True
    except Exception as e:
        error_message = str(e)
        print("Error : "+error_message)
        return error_message
