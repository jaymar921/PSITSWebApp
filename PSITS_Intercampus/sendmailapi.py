import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
# Importing library
import qrcode


def email_verification(email: str, code: str, name: str, event: str):
    # Send an HTML email with an embedded image and a plain text message for
    # email clients that don't want to display the HTML.

    # Define these once; use them twice!
    strFrom = 'psits.ccsmain@gmail.com'
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
        qr_data = qrcode.make(code);
        qr_data.save(f'./static/qr/{code}.png')
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
                    <h3>{event}</h3>
                    <p>Hello {name}!<br>You have successfully registered for the <a style="font-weight: 900;">{event}</a>.</p>
                    
                    <img style="width: 128px;height: 128px;" src="http://103.44.234.157:3000/static/qr/{code}.png">
                    <p>Registration Code: <a style="color: green; font-weight: 900;">{code}</a></p>
                    <p style="color: grey; font-size: 10px;">Scan this QR during the event registration</p>
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
        mail.login('psits.ccsmain@gmail.com','hftjwdxqhpdavufn')
        mail.sendmail(strFrom, strTo, msgRoot.as_string())
        mail.quit()
        print(f"Success : {event} email was sent to {email} | REF: {code}")
        return True
    except Exception as e:
        error_message = str(e)
        print("Error : "+error_message)
        return error_message
    
def email_raffle_winner(email: str, price: str, name: str, event: str):
    # Send an HTML email with an embedded image and a plain text message for
    # email clients that don't want to display the HTML.

    # Define these once; use them twice!
    strFrom = 'psits.ccsmain@gmail.com'
    strTo = email  # RECEIPIENT EMAIL HERE
    try:
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = f'{event} Raffle Winner'
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
                    <h3>{event} Raffle</h3>
                    <p>Hello {name}!<br>You just won a {price} during the <a style="font-weight: 900;">{event}'s</a> raffle!</p>
                    
                    <p>Raffle Price: <a style="color: green; font-weight: 900;">{price}</a></p>
                    <p style="color: grey; font-size: 10px;">Show this email to the event organizers</p>
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
        mail.login('psits.ccsmain@gmail.com','hftjwdxqhpdavufn')
        mail.sendmail(strFrom, strTo, msgRoot.as_string())
        mail.quit()
        print(f"Success : {event} email was sent to {email} | RAFFLE PRICE {price}")
        return True
    except Exception as e:
        error_message = str(e)
        print("Error : "+error_message)
        return error_message


if __name__ == '__main__':
    email_verification('ddurano@uc.edu.ph','ABC123DEF', "DURANO, DENNIS", "ICT Congress 2023")