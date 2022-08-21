from mysql import connector
from Models import Announcement, Account


def ConnectDB():
    return connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="psitswebapp"
    )


def getAnnouncements() -> list:
    query: str = "SELECT * FROM ANNOUNCEMENTS"
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    contents: list = []
    for content in data:
        c = Announcement(
            uid=content.get('ID'),
            title=content.get('TITLE'),
            date=content.get('DATE_PUBLISHED'),
            content=content.get('CONTENT')
        )
        contents.append(c)

    return sorted(contents, key=lambda x: x.date, reverse=True)


def getAccount(uid: int, password: str) -> Account:
    """
        getAccount will get the data from `account` table in `psitswebapp` database
        table: accounts
        attributes:
            idno - int
            rfid - varchar
            firstname - varchar
            lastname - varchar
            course - varchar
            year - int
            password - varchar
        """
    query: str = "SELECT * FROM ACCOUNTS where idno=%s and password=%s"
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (uid, password))
    data: dict = cursor.fetchall()
    cursor.close()
    db.close()

    if len(data) > 0:
        account = Account(
            data[0]['idno'],
            data[0]['rfid'],
            data[0]['firstname'],
            data[0]['lastname'],
            data[0]['course'],
            data[0]['year']
        )
        return account
    return Account(None, None, None, None, None, None)


def getAccountByID(uid: int) -> Account:
    """
        getAccount will get the data from `account` table in `psitswebapp` database
        table: accounts
        attributes:
            idno - int
            rfid - varchar
            firstname - varchar
            lastname - varchar
            course - varchar
            year - int
            password - varchar
        """
    query: str = f"SELECT * FROM ACCOUNTS where idno='{uid}'"
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data: dict = cursor.fetchall()
    cursor.close()
    db.close()

    if len(data) > 0:
        account = Account(
            data[0]['idno'],
            data[0]['rfid'],
            data[0]['firstname'],
            data[0]['lastname'],
            data[0]['course'],
            data[0]['year']
        )
        return account
    return Account(None, None, None, None, None, None)


def postAnnouncement(title: str, date, content: str):
    query: str = f"INSERT INTO `announcements` (`title`,`date_published`,`content`) values ('{title}','{date}','{content}') "
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    return None


def removeAnnouncement(uid):
    query: str = f"DELETE FROM `announcements` where id={uid}"
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
