from mysql import connector
from Models import Announcement, Account


def ConnectDB():
    return connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="psitswebapp"
    )


def executeQueryReturn(query: str):
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def executeQueryReturnParam(query: str, param: tuple):
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, param)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def executeQueryCommit(query: str):
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    return None


def getAnnouncements() -> list:
    """"
        getAnnouncements will get the data from `announcements` table in `psitswebapp` database
        table: announcements
            id - int (auto increment)
            title - varchar
            date_published - date
            content - varchar
    """
    query: str = "SELECT * FROM ANNOUNCEMENTS"
    data = executeQueryReturn(query)

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
    data: dict = executeQueryReturnParam(query, (uid, password))

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
    data = executeQueryReturn(query)

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
    """"
        postAnnouncement will insert the data to `announcements` table from `psitswebapp` database
        table: announcements
            id - int (auto increment) [NO NEED TO CALL]
            title - varchar
            date_published - date
            content - varchar
    """
    query: str = f"INSERT INTO `announcements` (`title`,`date_published`,`content`) values ('{title}','{date}','{content}') "
    executeQueryCommit(query)
    return None


def removeAnnouncement(uid):
    """"
        removeAnnouncement will remove the data from `announcements` table in `psitswebapp` database
        table: announcements
            id - int (auto increment) [only call this]
            title - varchar
            date_published - date
            content - varchar
    """
    query: str = f"DELETE FROM `announcements` where id={uid}"
    executeQueryCommit(query)
