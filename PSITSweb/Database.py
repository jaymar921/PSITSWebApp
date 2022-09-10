import datetime

from mysql import connector
from Models import Announcement, Account, Events, OrderAccount, Order, Event, Merchandise, MerchOrder, PSITSOfficer, FacultyMember
import TestApplication
from Util import deprecated

DATABASE_NAME = "psitswebapp"
USERNAME = "root"
PASSWORD = ""
HOST = "192.168.1.168"

"""
    PSITS version 1.0
    
    This is legacy code, try not to use them,
    start using the module/functions on line
    530+ where newly updated tables where added
"""


# This module is useful for initialization
def databaseInit() -> True:
    try:
        mysqldb = connector.connect(
            host=HOST,
            user=USERNAME,
            password=PASSWORD
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
                            amount decimal(10,2),
                            open varchar(5)
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
                            foreign key(event_uid) references events(uid) on delete cascade on update cascade,
                            foreign key(account_id) references accounts(idno) on delete cascade on update cascade
                        ) engine = innodb;
                    """)
            cursor.execute("""
                           create table event(
                                uid int not null auto_increment primary key,
                                title varchar(100) not null,
                                date_published date not null,
                                information varchar(2999) not null,
                                image_file varchar(200) not null
                            ) engine = innodb;
                            """)
            cursor.execute("""
                            create table merchandise(
                                uid int not null auto_increment primary key,
                                title varchar(100) not null,
                                information varchar(2999) not null,
                                price decimal(10,2) not null,
                                discount int not null, -- can be changed, in percentage form
                                stock int not null
                            ) engine = innodb;
                             """)
            cursor.execute("""
                            create table orders(
                                uid int not null auto_increment primary key,
                                account_id int not null,
                                FOREIGN KEY (account_id) REFERENCES accounts(idno) on delete cascade on update cascade,
                                order_date date not null,
                                merch_id int not null,
                                FOREIGN KEY (merch_id) REFERENCES merchandise(uid) on delete cascade on update cascade,
                                status varchar(20) not null,
                                quantity int not null,
                                additional_info varchar(200),
                                reference varchar(100)
                            ) engine = innodb;
                             """)
            cursor.execute("""
                                create table logging(
                                    uid int not null auto_increment primary key,
                                    date datetime not null,
                                    message varchar(150) not null
                                ) engine = innodb;

                                create table faculty_personnel(
                                    uid int not null auto_increment primary key,
                                    name varchar(100) not null,
                                    position varchar(100) not null,
                                    description varchar(2999) not null,
                                    job varchar(50) not null,
                                    image_src varchar(100) not null
                                ) engine = innodb;

                                create table psits_officers(
                                    uid int not null,
                                    FOREIGN KEY (uid) REFERENCES accounts(idno) on delete cascade on update cascade,
                                    position varchar(50) not null,
                                    birthday date not null,
                                    image_src varchar(50) not null
                                ) engine = innodb;
                            """)
            cursor.execute("""
                            create table faculty_personnel(
                                    uid int not null auto_increment primary key,
                                    name varchar(100) not null,
                                    position varchar(100) not null,
                                    description varchar(2999) not null,
                                    job varchar(50) not null,
                                    image_src varchar(100) not null
                                ) engine = innodb;
                            """)
            cursor.execute("""
                                create table psits_officers(
                                    uid int not null,
                                    FOREIGN KEY (uid) REFERENCES accounts(idno) on delete cascade on update cascade,
                                    position varchar(50) not null,
                                    birthday date not null,
                                    image_src varchar(50) not null
                                ) engine = innodb;
                            """)
            print("\n")
            TestApplication.TestDatabase()
            print("\n")
            print(f"PSITS Webapp successfully created a database [{DATABASE_NAME}]")
            print(f"PSITS Webapp successfully created a legacy tables [announcements,accounts,events,order_account]")
            print(f"PSITS Webapp successfully created a v1.1 tables [merchandise, event, orders]")
        print(f"All is set... ")
    except:
        print("There was an issue connecting to database, the app will not start")
        print(f"Database.py configuration:\n\tHOST = '{HOST}'\n\tUSER = '{USERNAME}'\n\tPASS "
              f"= '{PASSWORD}'\n\tDB   = '{DATABASE_NAME}'")
        return False
    return True


def ConnectDB():
    return connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
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
            uid=content.get('id'),
            title=content.get('title'),
            date=content.get('date_published'),
            content=content.get('content')
        )
        contents.append(c)

    return sorted(contents, key=lambda x: x.uid, reverse=True)


# Get latest ID
# Hi boss Jayy HAHAHAHAHAHAHAHAHAHAHAHHA
# ===================================================
def getLatestAnnouncement() -> int:
    query = "SELECT max(id) as latest from announcements"
    data: dict = executeQueryReturn(query)
    return data[0]['latest']
# ==================================================


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
            email - varchar
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
    query: str = "SELECT * FROM ACCOUNTS"
    if search is not None:
        query: str = f"SELECT * FROM ACCOUNTS where idno like '%{search}%' or rfid like '%{search}%'" \
                     f" or lastname like '%{search}%' or course like '%{search}%' or year like '{search[-1:]}'"
        if search.lower() == 'all':
            query: str = "SELECT * FROM ACCOUNTS"
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
            email - varchar
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
            id - int (auto increment) [only call this]
    """
    query: str = f"DELETE FROM `announcements` where id={uid}"
    executeQueryCommit(query)


@deprecated("addEvent() is deprecated")
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
            open - varchar(3)
        """
    query: str = f"INSERT INTO `events` values ({int(event.uid)}, '{event.title}', '{event.date_held}', '{event.info}'" \
                 f", '{event.required_payment}', '{event.item}', {float(int(event.amount))},'{event.open_for_payment}')"
    executeQueryCommit(query)


@deprecated("removeEvent() is deprecated")
def removeEvent(uid):
    query: str = f"DELETE FROM `events` where uid={uid}"
    executeQueryCommit(query)


@deprecated("getEvents() is deprecated")
def getEvents() -> list:
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


@deprecated("getEvent(uid) is deprecated")
def getEvent(uid):
    for event in getEvents():
        if int(event.uid) == int(uid):
            return event
    return None


@deprecated("getSearchEvents(search) is deprecated")
def getSearchEvents(search) -> list:
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


@deprecated("updateEvent(event: Event) is deprecated")
def updateEvent(event: Events):
    query: str = f"UPDATE `events` SET title='{event.title}',date_held='{event.date_held}'," \
                 f"info='{event.info}',required_payment='{event.required_payment}'," \
                 f"item_to_be_paid='{event.item}',amount={event.amount}, open='{event.open_for_payment}' " \
                 f"where uid={event.uid}"
    executeQueryCommit(query)


@deprecated("getOrderAccount(event_id, account_id) is deprecated")
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


@deprecated("getOrder(event_id, status) is deprecated")
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


@deprecated("getOrderById(uid) is deprecated")
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


@deprecated("updateOrder(OrderAccount) is deprecated")
def updateOrder(order: OrderAccount):
    query: str = f"UPDATE `order_account` SET account_status='{order.status}', quantity={order.quantity}, " \
                 f"payment_reference='{order.reference}' where uid={order.uid}"
    executeQueryCommit(query)


@deprecated("createOrder(OrderAccount) is deprecated")
def createOrder(order: OrderAccount):
    query: str = f"INSERT INTO `order_account`(event_uid,account_id,account_status,quantity,payment_reference) " \
                 f"values({order.event_uid},{order.account_uid},'{order.status}',{order.quantity},'{order.reference}')"
    executeQueryCommit(query)


@deprecated("getAllOrders(search) is deprecated")
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


def getTime():
    return f"[{datetime.datetime.now()}] "


def databaseLog(message):
    print(f"{getTime()}: {message}")
    query = f"INSERT INTO `logging` (date, message) values ('{datetime.datetime.now()}','{message}')"
    executeQueryCommit(query)


"""
    PSITS version 1.1
    Prepared by Jayharron Mar Abejar (back-end developer),
    New tables where added into the database and new
    functions are created
    
    Events, OrderAccount and Order table have been
    set to deprecated so please avoid using them
    
    The reason why I did not remove the code because the
    old PSITS webapp system is still using the legacy code
"""


# This function will insert a new Event into the database
# requires a Event object as argument
# @returns nothing
def CREATEEvent(event: Event):
    query: str = f"insert into `event`(title,date_published,information,image_file) values ('{event.title}'," \
                 f"'{event.date_published}','{event.information}','{event.image_file}')"
    executeQueryCommit(query)


# This function will retrieve all the Event from the the database
# @returns a list of 'Event'
def GETAllEvent() -> list:
    return SEARCHEvent("all")


# This function will retrieve all the Event from the the database
# with a condition
# @returns a list of 'Event'
def SEARCHEvent(search: str) -> list:
    query: str = f"select * from `event`"
    if search is not None:
        if search != "" and search.lower() != "all":
            query = f"select * from `event` where title like '%{search}%' or information like '%{search}%'"
    data: dict = executeQueryReturn(query)
    events = []
    for event in data:
        events.append(
            Event(
                event['uid'],
                event['title'],
                event['date_published'],
                event['information'],
                event['image_file']
            )
        )
    return events


# This function will delete an Event from the database given
# given the UID of the Event,
# @returns nothing
def DELETEEvent(uid):
    executeQueryCommit(f"delete from `event` where uid = {uid}")


# This function will update an event from the Event uid argument
# @returns nothing
def UPDATEEvent(event: Event):
    query: str = f"update `event` set title='{event.title}',date_published='{event.date_published}'," \
                 f"information='{event.information}',image_file='{event.image_file}' where uid={event.uid}"
    executeQueryCommit(query)


# This function will insert a new Merchandise into the table
# @requires a Merchandise object as argument
def CREATEMerchandise(merch: Merchandise):
    query: str = f"insert into `merchandise`(title,information,price,discount,stock) values " \
                 f"('{merch.title}','{merch.info}'," \
                 f"{merch.price},{merch.discount},{merch.stock})"
    executeQueryCommit(query)


# This function will retrieve all the Merchandise data from the database
# @returns a list of Merchandise
def GETAllMerchandise() -> list:
    return SEARCHMerchandise("all")


# This function will retrieve all the Merchandise data from the database
# that matches with the search argument
# @returns a list of Merchandise
def SEARCHMerchandise(search: str) -> list:
    query: str = "select * from `merchandise`"
    if search is not None:
        if search != '' and search.lower() != 'all':
            query = f"select * from `merchandise` where uid like '%{search}%' or title like '%{search}%'"
    data: dict = executeQueryReturn(query)
    merchandise = []
    for merch in data:
        merchandise.append(
            Merchandise(
                merch['uid'],
                merch['title'],
                merch['information'],
                merch['price'],
                merch['discount'],
                merch['stock']
            )
        )
    return merchandise


# This function will update the Merchandise table from Merchandise uid argument
# @returns nothing
def UPDATEMerchandise(merch: Merchandise):
    query: str = f"update `merchandise` set title='{merch.title}',information='{merch.info}'," \
                 f"price={merch.price},discount={merch.discount},stock={merch.stock} where uid={merch.uid}"
    executeQueryCommit(query)


# This function will delete a merchandise from the merchandise table given
# a uid argument
# @returns nothing
def DELETEMerchandise(uid):
    executeQueryCommit(f"delete from `merchandise` where uid = {uid}")


# This function will add a new MerchOrder into the Order table in the database
# requires MerchOrder data as argument
# @returns nothing
def CREATEMerchOrder(order: MerchOrder):
    query: str = f"insert into `orders`(account_id,order_date,merch_id,status,quantity,additional_info,reference)" \
                 f" values ({order.account_id},'{order.order_date}',{order.merchandise_id}," \
                 f"'{order.status}',{order.quantity},'{order.additional_info}','{order.reference}')"
    executeQueryCommit(query)


# This function will retrieve all the MerchOrder data from the database
# @returns a list of MerchOrder
def GETAllMerchOrder() -> list:
    return SEARCHMerchOrder("all")


# This function will retrieve all the MerchOrder data from the database
# that matches with the search argument
# @returns a list of MerchOrder
def SEARCHMerchOrder(search: str) -> list:
    query: str = "select * from `orders`"
    if search is not None:
        if search != '' and search != 'all':
            query = f"select * from `orders` where account_id like '%{search}%' or merch_id like '%{search}%'  or status like '%{search}%' or reference like '%{search}%'"
    data: dict = executeQueryReturn(query)
    orders = []
    for order in data:
        orders.append(
            MerchOrder(
                order['uid'],
                order['account_id'],
                order['order_date'],
                order['merch_id'],
                order['status'],
                order['quantity'],
                order['additional_info'],
                order['reference']
            )
        )
    return orders


# This function will update the orders table from MerchOrder uid argument
# @returns nothing
def UPDATEMerchOrder(merch: MerchOrder):
    query: str = f"update `orders` set account_id={merch.account_id},order_date='{merch.order_date}'," \
                 f"merch_id={merch.merchandise_id},status='{merch.status}',quantity={merch.quantity}," \
                 f"additional_info='{merch.additional_info}'," \
                 f"reference='{merch.reference}' where uid={merch.uid}"
    executeQueryCommit(query)


# This function will delete a MerchOrder from the orders table given
# a uid argument
# @returns nothing
def DELETEMerchOrder(uid):
    executeQueryCommit(f"delete from `orders` where uid = {uid}")


# This function will create a new PSITS officer
# required PSITSOfficer as argument
def CREATEPSITSOfficer(account: PSITSOfficer):
    query: str = f"INSERT INTO `psits_officers` values ({account.uid}, '{account.position}', "\
                 f"'{account.birthday}', '{account.image_src}')"
    executeQueryCommit(query)


# This function will retrieve all PSITSOfficers from the psitswebapp database
# @returns a list of PSITSOfficer
def GETAllPSITSOfficer() -> list:
    return SEARCHPSITSOfficer("ALL")


# This function will search for PSITSOfficers
# @returns a list of PSITSOfficer
def SEARCHPSITSOfficer(search: str) -> list:
    accounts: list = getAllAccounts(search)
    officers: list = []

    for account in accounts:
        officer_data = executeQueryReturn(f"select * from `psits_officers` where uid={account.uid}")
        if officer_data is not None:
            for officer_d in officer_data:
                officer = PSITSOfficer(
                    getAccountByID(officer_d['uid']),
                    officer_d['position'],
                    officer_d['birthday']
                )
                officer.image_src = officer_d['image_src']
                officers.append(officer)
    return officers


# This function will update PSITSOfficer given
# an updated PSITSOfficer argument, make sure that the UID has not been changed
def UPDATEPSITSOfficer(account: PSITSOfficer):
    query: str = f"UPDATE `psits_officers` SET position='{account.position}', birthday='{account.birthday}',"\
                 f"image_src='{account.image_src}' where uid={account.uid}"
    executeQueryCommit(query)


# This function will remove a psits officer, given a UID
def DELETEPSITSOfficer(uid):
    executeQueryCommit(f"DELETE FROM `psits_officers` where uid={uid}")



# This function will add new Faculty Member
def CREATEFacultyMember(member: FacultyMember):
    query = f"INSERT INTO `faculty_personnel` (name,position,description,job,image_src) values ('{member.name}','{member.position}','{member.description}','{member.job}','{member.image_src}')"
    executeQueryCommit(query)


# This function will get all faculty member
# return a list of faculty personnel
def GETAllFacultyMember()-> list:
    return SEARCHFacultyMember("all")


# This function will get a faculty member given a string to search
# returns a list of faculty personnel
def SEARCHFacultyMember(search: str):
    query: str = "select * from `faculty_personnel`"
    if search is not None:
        if search != '' and search.lower() != 'all':
            query = f"select * from `faculty_personnel` where name like '%{search}%' or position like '%{search}%'"
    data: dict = executeQueryReturn(query)
    member: list = []
    
    for m_d in data:
        faculty_member = FacultyMember(
                m_d['uid'],
                m_d['name'],
                m_d['position'],
                m_d['description'],
                m_d['job']
            )
        faculty_member.image_src = m_d['image_src']
        member.append(faculty_member )
    return member


# This function will update the Faculty Member
def UPDATEFacultyMember(m: FacultyMember):
    query = f"UPDATE `faculty_personnel` set name='{m.name}', position='{m.position}', description='{m.description}', job='{m.job}', image_src='{m.image_src}' where uid={m.uid}"
    executeQueryCommit(query)