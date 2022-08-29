import requests

from PSITSweb.Models import Email


def pushEmail(email: Email):
    try:
        headers = {
            'X-MAGICBELL-API-SECRET': 'jxJA5ivlksSWGYeTo8Rtv8+8YBbYIPssKeuFpWNj',
            'X-MAGICBELL-API-KEY': 'c4ff39e59865e6d4807ae3d38c44975801aeb39c',
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
    finally:
        None
