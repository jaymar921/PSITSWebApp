import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from Util import CONFIGURATION


def email_verification(email: str, code: str):
    # Send an HTML email with an embedded image and a plain text message for
    # email clients that don't want to display the HTML.

    # Define these once; use them twice!
    strFrom = CONFIGURATION()['SENDMAIL_EMAIL']
    strTo = email  # RECEIPIENT EMAIL HERE
    try:
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = 'B-Lease OTP Verification'
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
        <head></head>
        <body>

          
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
        mail.login(CONFIGURATION()['SENDMAIL_EMAIL'],
                   CONFIGURATION()['SENDMAIL_PASS'])
        mail.sendmail(strFrom, strTo, msgRoot.as_string())
        mail.quit()

        return True
    except Exception as e:
        error_message = str(e)
        print("Error : "+error_message)
        return error_message
