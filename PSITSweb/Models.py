class Announcement:
    def __init__(self, uid, title, date, content):
        self.uid = uid
        self.title = title
        self.date = date
        self.content = content

    def __repr__(self):
        return str(self.uid)


class Account:
    def __init__(self, uid, rfid, firstname, lastname, course, year):
        self.uid = uid
        self.rfid = rfid
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.year = year


class Events:
    def __init__(self, uid, title, date_held, info, required_payment, item, amount):
        self.uid = uid
        self.title = title
        self.date_held = date_held
        self.info = info
        self.required_payment = required_payment
        self.item = item
        self.amount = amount
