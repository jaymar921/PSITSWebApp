import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def email_verification(email: str, code: str, name: str, event: str):
    # Send an HTML email with an embedded image and a plain text message for
    # email clients that don't want to display the HTML.

    # Define these once; use them twice!
    strFrom = '---@EMAIL'
    strTo = email  # RECEIPIENT EMAIL HERE
    try:
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = f'{event} Registration'
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
                    <img style="width: 64px;height: 64px;" src="http://119.92.196.92/static/images/PSITS_LOGO.png">
                    <h3>{event}</h3>
                    <p>Hello {name}!<br>You have successfully registered for the <a style="font-weight: 900;">{event}</a>.</p>
                    <p>Registration Code: <a style="color: green; font-weight: 900;">{code}</a></p>
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
        mail.login('---@EMAIL','---@EMAIL-PASS')
        mail.sendmail(strFrom, strTo, msgRoot.as_string())
        mail.quit()
        print(f"Success : Registration email was sent to {email}")
        return True
    except Exception as e:
        error_message = str(e)
        print("Error : "+error_message)
        return error_message


if __name__ == '__main__':
    email_verification('---@EMAIL','ABC123DEF', "---@NAME", "ICT Congress 2023")