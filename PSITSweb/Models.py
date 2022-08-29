class Announcement:
    def __init__(self, uid, title, date, content):
        self.uid = uid
        self.title = title
        self.date = date
        self.content = content
        self.image_location = ''

    def __repr__(self):
        return str(self.uid)


class Account:
    def __init__(self, uid, rfid, firstname, lastname, course, year, email):
        self.uid = uid
        self.rfid = rfid
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.year = year
        self.email = email


class Events:
    def __init__(self, uid, title, date_held, info, required_payment, item, amount, open):
        self.uid = uid
        self.title = title
        self.date_held = date_held
        self.info = info
        self.required_payment = required_payment
        self.item = item
        self.amount = amount
        self.open_for_payment = open
        if not self.requirePayment():
            self.open_for_payment = 'NO'

    def requirePayment(self) -> bool:
        return self.required_payment == "YES"


class OrderAccount:
    def __init__(self, uid, event_uid, account_uid, status, quantity, reference):
        self.uid = uid
        self.event_uid = event_uid
        self.account_uid = account_uid
        self.status = status
        self.quantity = quantity
        self.reference = reference


class Email:
    def __init__(self, title, recipient, content):
        self.title: str = title
        self.recipient: str = recipient
        self.content: str = content


class Order:
    def __init__(self, event: Events, account: Account, order_account: OrderAccount):
        self.event = event
        self.account = account
        self.order_account = order_account
        self.total = float(event.amount)*int(order_account.quantity)
