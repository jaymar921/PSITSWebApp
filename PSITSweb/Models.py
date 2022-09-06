from warnings import warn

from Util import deprecated


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


@deprecated("Events class is deprecated, use Event")
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


@deprecated("OrderAccount class is deprecated, use Orders")
class OrderAccount:
    def __init__(self, uid, event_uid, account_uid, status, quantity, reference):
        warn("This class is deprecated", DeprecationWarning, stacklevel=2)
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


@deprecated("Order class is deprecated, use Orders")
class Order:
    def __init__(self, event: Events, account: Account, order_account: OrderAccount):
        self.event = event
        self.account = account
        self.order_account = order_account
        self.total = float(event.amount)*int(order_account.quantity)


"""
    Version 1.1
    Classes Order, OrderAccount and Events are deprecated
    
    use Event, Merchandise and Orders
"""


class Event:
    def __init__(self, uid, title, date_published, information, image_file):
        self.uid = uid
        self.title = title
        self.date_published = date_published
        self.information = information
        self.image_file = image_file


class Merchandise:
    def __init__(self, uid, title, info, price, discount, stock):
        self.uid = uid
        self.title = title
        self.info = info
        self.price = price
        self.discount = discount
        self.stock = stock
        self.image_file = ""


class MerchOrder:
    def __init__(self, uid, acc_id, order_date, merch_id, status, quantity, add_info, reference):
        self.uid = uid
        self.account_id = acc_id
        self.order_date = order_date
        self.merchandise_id = merch_id
        self.status = status
        self.quantity = quantity
        self.additional_info = add_info
        self.reference = reference
