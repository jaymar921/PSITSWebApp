from mysql import connector
from PSITSweb.Models import Announcement, Account, Events, OrderAccount, Order

DATABASE_NAME = "psitswebapp"


def databaseInit():
    mysqldb = connector.connect(
        host="127.0.0.1",
        user="root",
        password=""
    )
    cursor = mysqldb.cursor()
    cursor.execute("SHOW DATABASES")
    has_psits_db: bool = False
    if cursor is not None:
        for x in cursor:
            if DATABASE_NAME in x:
                has_psits_db = True
    if not has_psits_db:
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
        cursor.execute(f"USE {DATABASE_NAME}")
        cursor.execute("""
                    create table announcements(
                        id int not null auto_increment,
                        title varchar(100) not null,
                        date_published date not null,
                        content varchar(9999) not null,
                        primary key(id)
                    ) engine = innodb;
                    """)
        cursor.execute("""
                    create table accounts(
                        idno int(11) not null primary key,
                        rfid varchar(100),
                        firstname varchar(100) not null,
                        lastname varchar(100) not null,
                        course varchar(5) not null,
                        year int(1) not null,
                        email varchar(100) not null,
                        password varchar(32) not null
                    ) engine = innodb;
                    """)
        cursor.execute("""
                    create table events (
                        uid int primary key,
                        title varchar(50) not null,
                        date_held date,
                        info varchar(100) not null,
                        required_payment varchar(3) not null,
                        item_to_be_paid varchar(30),
                        amount decimal(10,2)
                    ) engine = innodb;
                """)
        cursor.execute("""
                    create table order_account(
                        uid int not null auto_increment primary key,
                        event_uid int not null,
                        account_id int not null,
                        account_status varchar(50) not null,
                        quantity int not null,
                        payment_reference varchar(50) not null,
                        foreign key(event_uid) references events(uid),
                        foreign key(account_id) references accounts(idno)
                    ) engine = innodb;
                """)
        print(f"PSITS Webapp successfully created a database [{DATABASE_NAME}]")
        print(f"PSITS Webapp successfully created a tables [announcements,accounts,events,order_account]")
    print(f"All is set... ")


def ConnectDB():
    return connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database=DATABASE_NAME
    )


def executeQueryReturn(query: str) -> dict:
    db = ConnectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    data: dict = cursor.fetchall()
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
    data: dict = executeQueryReturn(query)

    contents: list = []
    for content in data:
        c = Announcement(
            uid=content.get('ID'),
            title=content.get('TITLE'),
            date=content.get('DATE_PUBLISHED'),
            content=content.get('CONTENT')
        )
        contents.append(c)

    return sorted(contents, key=lambda x: x.uid, reverse=True)


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
            data[0]['year'],
            data[0]['email']
        )
        return account
    return Account(None, None, None, None, None, None, None)


def getAllAccounts(search: str):
    query: str = f"SELECT * FROM ACCOUNTS where idno like '%{search}%' or rfid like '%{search}%' or lastname like" \
                 f" '%{search}%' "
    if search is None:
        query = "SELECT * FROM ACCOUNTS"
    data = executeQueryReturn(query)
    accounts: list = []
    for acc in data:
        account = Account(
            acc['idno'],
            acc['rfid'],
            acc['firstname'],
            acc['lastname'],
            acc['course'],
            acc['year'],
            acc['email']
        )
        accounts.append(account)
    return accounts


def updateAccount(account: Account):
    query: str = f"UPDATE `accounts` SET rfid='{account.rfid}',firstname='{account.firstname}'," \
                 f"lastname='{account.lastname}',course='{account.course}',year={account.year}" \
                 f", email='{account.email}' where idno={account.uid}"
    executeQueryCommit(query)


def removeAccount(uid):
    query: str = f"DELETE FROM `accounts` where idno={uid}"
    executeQueryCommit(query)


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
            data[0]['year'],
            data[0]['email']
        )
        return account
    return Account(None, None, None, None, None, None, None)


def registerAccountDB(account: Account, password: str):
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
    query: str = f"INSERT INTO `accounts` (`idno`,`rfid`,`firstname`,`lastname`,`course`,`year`,`email`,`password`)" \
                 f" values ({account.uid},'{account.rfid}','{account.firstname}'" \
                 f",'{account.lastname}','{account.course}',{account.year},'{account.email}','{password}');"
    executeQueryCommit(query)


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


def addEvent(event: Events):
    """"
        addEvent will save the data to `events` table in `psitswebapp` database
        table: events
            uid - int
            title - varchar
            date_held - date
            info - varchar
            required_payment - varchar
            item_to_be_paid - varchar
            amount - decimal(10,2)
        """
    query: str = f"INSERT INTO `events` values ({int(event.uid)}, '{event.title}', '{event.date_held}', '{event.info}'" \
                 f", '{event.required_payment}', '{event.item}', {float(int(event.amount))},'{event.open_for_payment}')"
    executeQueryCommit(query)


def removeEvent(uid):
    """"
         removeEvent will remove the data from `events` table in `psitswebapp` database
            table: events
                uid - int
                title - varchar
                date_held - date
                info - varchar
                required_payment - varchar
                item_to_be_paid - varchar
                amount - decimal(10,2)
    """
    query: str = f"DELETE FROM `events` where uid={uid}"
    executeQueryCommit(query)


def getEvents() -> list:
    """"
        getEvents will get the data from `events` table in `psitswebapp` database
        table: events
            uid - int
            title - varchar
            date_held - date
            info - varchar
            required_payment - varchar
            item_to_be_paid - varchar
            amount - decimal(10,2)
    """
    query: str = "SELECT * FROM EVENTS ORDER BY date_held ASC"
    data: dict = executeQueryReturn(query)

    events: list = []
    for e in data:
        event = Events(
            e.get('uid'),
            e.get('title'),
            e.get('date_held'),
            e.get('info'),
            e.get('required_payment'),
            e.get('item_to_be_paid'),
            e.get('amount'),
            e.get('open')
        )
        events.append(event)
    return events


def getEvent(uid):
    for event in getEvents():
        if int(event.uid) == int(uid):
            return event
    return None


def getSearchEvents(search) -> list:
    """"
        getEvents will get the data from `events` table in `psitswebapp` database
        table: events
            uid - int
            title - varchar
            date_held - date
            info - varchar
            required_payment - varchar
            item_to_be_paid - varchar
            amount - decimal(10,2)
    """
    query: str = f"SELECT * FROM EVENTS where uid like '%{search}%' or title like '%{search}%' ORDER BY date_held ASC"
    if search is None:
        query = "SELECT * FROM EVENTS ORDER BY date_held ASC"
    data: dict = executeQueryReturn(query)

    events: list = []
    for e in data:
        event = Events(
            e.get('uid'),
            e.get('title'),
            e.get('date_held'),
            e.get('info'),
            e.get('required_payment'),
            e.get('item_to_be_paid'),
            e.get('amount'),
            e.get('open'),
        )
        events.append(event)
    return events


def updateEvent(event: Events):
    query: str = f"UPDATE `events` SET title='{event.title}',date_held='{event.date_held}'," \
                 f"info='{event.info}',required_payment='{event.required_payment}'," \
                 f"item_to_be_paid='{event.item}',amount={event.amount}, open='{event.open_for_payment}' " \
                 f"where uid={event.uid}"
    executeQueryCommit(query)


def getOrderAccount(event_uid, account_uid):
    query: str = f"SELECT * FROM `order_account` where account_id={account_uid} and event_uid={event_uid} " \
                 f"and account_status!='CLAIMED'"
    data: dict = executeQueryReturn(query)

    for d in data:
        order = OrderAccount(
            d.get('uid'),
            d.get('event_uid'),
            d.get('account_id'),
            d.get('account_status'),
            d.get('quantity'),
            d.get('payment_reference')
        )
        return order
    return OrderAccount(None, None, None, None, None, None)


def getOrder(event_uid, status):
    query: str = f"SELECT * FROM `order_account` where event_uid={event_uid} and account_status='{status}'"
    data: dict = executeQueryReturn(query)
    orders: list = []
    for d in data:
        order = OrderAccount(
            d.get('uid'),
            d.get('event_uid'),
            d.get('account_id'),
            d.get('account_status'),
            d.get('quantity'),
            d.get('payment_reference')
        )
        orders.append(order)
    return orders


def getOrderById(uid):
    query: str = f"SELECT * FROM `order_account` where uid={uid}"
    data: dict = executeQueryReturn(query)
    if len(data) > 0:
        order = OrderAccount(
            data[0]['uid'],
            data[0]['event_uid'],
            data[0]['account_id'],
            data[0]['account_status'],
            data[0]['quantity'],
            data[0]['payment_reference']
        )
        return order
    return None


def updateOrder(order: OrderAccount):
    query: str = f"UPDATE `order_account` SET account_status='{order.status}', quantity={order.quantity}, " \
                 f"payment_reference='{order.reference}' where uid={order.uid}"
    executeQueryCommit(query)


def createOrder(order: OrderAccount):
    query: str = f"INSERT INTO `order_account`(event_uid,account_id,account_status,quantity,payment_reference) " \
                 f"values({order.event_uid},{order.account_uid},'{order.status}',{order.quantity},'{order.reference}')"
    executeQueryCommit(query)


def getAllOrders(search: str):
    if search is None:
        search = ''
    if search != '':  # if there is an input
        if search.lower() == 'all':
            search = ""
        elif len(getSearchEvents(search)) > 0:
            search = f" where event_uid like {getSearchEvents(search)[0].uid}"
        elif len(getAllAccounts(search)) > 0:
            search = f" where account_id like {getAllAccounts(search)[0].uid}"
        else:
            search = f" where account_status like '%{search}%'"

    query: str = f"SELECT * FROM `order_account` {search}"
    data: dict = executeQueryReturn(query)
    orders: list = []

    for d in data:
        order_account = OrderAccount(
            d.get('uid'),
            d.get('event_uid'),
            d.get('account_id'),
            d.get('account_status'),
            d.get('quantity'),
            d.get('payment_reference')
        )
        order = Order(
            getEvent(order_account.event_uid),
            getAccountByID(order_account.account_uid),
            order_account
        )
        orders.append(order)
    return orders
