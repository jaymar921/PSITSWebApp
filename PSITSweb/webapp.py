import datetime
import os
import socket

import flask
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory

from Database import getAnnouncements, getAccount, getAccountByID, postAnnouncement, removeAnnouncement, \
    removeEvent, registerAccountDB, getAllAccounts, updateAccount, removeAccount,\
    getEvent, getOrderAccount, createOrder, updateOrder, getAllOrders, getOrderById, \
    databaseInit, databaseLog, CREATEEvent, SEARCHEvent, UPDATEEvent, GETAllEvent, CREATEMerchandise, \
    getLatestAnnouncement, DELETEEvent
from EmailAPI import pushEmail
from Models import Event, Account, Email, OrderAccount, Merchandise
from Util import hashData, isAdmin, contentVerifier
from waitress import serve

UPLOAD_FOLDER = 'SERVER_FILES/'
ALLOWED_EXTENSION = {'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'PSITS2022BYABEJAR'

"""
      ____  ____ ___ _____ ____  
     |  _ \/ ___|_ _|_   _/ ___| 
     | |_) \___ \| |  | | \___ \ 
     |  __/ ___) | |  | |  ___) |
     |_|   |____/___| |_| |____/ 
    A web application that handles announcements and events
    for UC CCS Students developed by Jayharron Mar Abejar and 
    this private project is open for collaboration to students
    who are willing to collaborate.
    
    - Collaborators: [Please indicate your names below]
        - Rey Vincent de los Reyes
        - Harold Cuico
        - Nathaniel Tiempo
        - Ferrer Mariella
"""


@app.route("/")
def webpage():
    return redirect(url_for("landing_page"))


@app.route("/PSITS")
def landing_page():
    events: list = GETAllEvent()
    announcements: list = getAnnouncements()

    # Load the Photos if exist
    for announcement in announcements:
        if checkImageExist(str(announcement.uid)+announcement.title + ".png"):
            announcement.image_location = f"{str(announcement.uid)+announcement.title}.png"

    # show the latest 10 announcement
    temp = announcements.copy()
    if len(announcements) > 10:
        announcements: list = []
        for i in range(0, 10):
            announcements.append(temp[i])
        temp.clear()

    if "username" in session:
        if isAdmin(session['username']):
            return render_template("Homepage.html",
                                   title="PSITS ADMIN",
                                   ANNOUNCEMENTS=announcements,
                                   login="none",
                                   logout="block",
                                   account=session['username'],
                                   admin="block",
                                   events=events,
                                   account_data=getAccountByID(session['username']))
        else:
            return render_template("Homepage.html",
                                   title="PSITS ANNOUNCEMENTS",
                                   ANNOUNCEMENTS=announcements,
                                   login="none", logout="block",
                                   account=session['username'],
                                   admin="none",
                                   events=events,
                                   account_data=getAccountByID(session['username']))
    return render_template("Homepage.html",
                           title="PSITS ANNOUNCEMENTS",
                           ANNOUNCEMENTS=announcements,
                           login="block",
                           logout="none", admin="none", events=events)


@app.route("/PSITS@Login")
def login_page():
    if 'username' in session:
        return redirect(url_for("landing_page"))
    return render_template("Login.html",
                           title="PSITS login",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="none",
                           logout="none")


@app.route("/PSITS@announce", methods=['POST'])
def post_announcement():
    date_time = datetime.datetime.now()

    title: str = contentVerifier(request.form['title'])
    content: str = request.form['content']

    if "username" in session:
        if isAdmin(session['username']):
            postAnnouncement(title, date_time.strftime("%Y-%m-%d"), contentVerifier(content))
            ID = getLatestAnnouncement()
            databaseLog(f"Account ID [{session['username']}] posted an announcement [{title}]")
            if 'file' in request.files:
                file = request.files['file']
                if file is not None:
                    if file.filename != '':
                        ext = file.filename.split(".")[1]
                        if ext in ALLOWED_EXTENSION:
                            file.filename = str(ID) + title + "." + ext
                            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                            file.save(path)
                            databaseLog(f"Announcement [{title}] comes with an image")
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")

    return redirect(url_for("landing_page"))


@app.route("/announcement_removal/<uid>")
def remove_announcement(uid):
    if "username" in session:
        if isAdmin(session['username']):
            removeAnnouncement(uid)
            databaseLog(f"Removed announcement [{uid}]")
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))


@app.route("/PSITSLogin", methods=['POST'])
def login():
    account_id: str = request.form['id_number']
    password: str = request.form['password']
    account = getAccount(int(account_id), hashData(password))
    if account.uid is not None:
        session['username'] = account.uid
        databaseLog(f"Account ID [{session['username']}] has logged in")
        return redirect(url_for("landing_page"))

    account = getAccountByID(int(account_id))
    message = "Account not found!"
    if account.uid is not None:
        message = "Invalid password"
    return render_template("Login.html",
                           title="Login PSITS",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="none",
                           logout="none",
                           message=message)


@app.route("/PSITS@Register", methods=['POST', 'GET'])
def registerAccount():
    if flask.request.method == 'GET':
        return render_template("RegisterStudent.html", title='Register', login='none', logout='none')
    else:
        idno = request.form['idnum']
        rfid = request.form['rfid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course = request.form['course']
        year = request.form['year']
        email = request.form['email']
        password = hashData(request.form['password'])
        account = Account(
            idno,
            rfid,
            firstname,
            lastname,
            course,
            year,
            email
        )
        registerAccountDB(account, password)
        content = f"""
           Dear {firstname},
           
           We are happy to know that you've signed up for PSITS!
           This email is auto generated, please do not reply :)
        """
        databaseLog(f"New account created. Account ID [{account.uid}]")
        try:
            pushEmail(Email('Welcome to PSITS', email, content))
        finally:
            return redirect(url_for("login_page"))


@app.route("/PSITS@NewEvent", methods=['GET', 'POST'])
def EventHandlerPSITS():
    if flask.request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('cant_find_link'))
        account = session['username']
        if isAdmin(account):
            return render_template("NewEventForm.html", login='none', logout='block', account=account)
        else:
            return redirect(url_for('cant_find_link'))
    else:
        event_title = contentVerifier(request.form["Title"])
        event_date = request.form["date_held"]
        event_info = contentVerifier(request.form["Information"])
        event = Event(
            None,
            event_title,
            event_date,
            event_info,
            "-"
        )
        CREATEEvent(event)
        databaseLog(f"Event [{event.title}] added")
        event = SEARCHEvent(event_title)[0]
        if 'event_image' in request.files:
            file = request.files['event_image']
            if file is not None:
                if file.filename != '':
                    ext = file.filename.split(".")[1]
                    if ext in ALLOWED_EXTENSION:
                        file.filename = "event" + str(event.uid) + "." + ext
                        event.image_file = "event" + str(event.uid) + "." + ext
                        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(path)
                        databaseLog(f"Event [{event.title}] comes with an image")
        UPDATEEvent(event)
        return redirect(url_for("landing_page"))


@app.route("/event_removal/<uid>")
def removeEventPage(uid):
    if "username" in session:
        if isAdmin(session['username']):
            removeEvent(uid)
            databaseLog(f"Removed Event ID [{uid}]")
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))


@app.route("/PSITS@Merch", methods=['POST', 'GET'])
def addMerch():
    if flask.request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('cant_find_link'))
        account = session['username']
        if isAdmin(account):
            print("is admin")
            return render_template("MerchForm.html", login='none', logout='block', account=account)
        else:
            return redirect(url_for('cant_find_link'))
    else:
        merchName = contentVerifier(request.form["Merch"])
        info = contentVerifier(request.form["Info"])
        price = request.form["Price"]
        discount = request.form["Discount"]
        stock = request.form["Stock"]

        merch = Merchandise(
            None,
            merchName,
            info,
            price,
            discount,
            stock
        )
    CREATEMerchandise(merch)
    return redirect(url_for("landing_page"))


@app.route("/PSITS@Students", methods=['POST', 'GET'])
def psits_students_list():
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))

    if request.method == 'GET':
        # Get the search
        search: str = flask.request.values.get('search')
        return render_template("StudentsList.html",
                               logout='block', login='none', account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS STUDENTS LIST', accounts=getAllAccounts(search))
    else:
        search: str = flask.request.values.get('search')
        updated_account = Account(
            request.form['idnum'],
            request.form['rfid'],
            request.form['firstname'],
            request.form['lastname'],
            request.form['course'],
            request.form['year'],
            request.form['email']
        )
        updateAccount(updated_account)
        databaseLog(f"Updated account ID [{updated_account.uid}]")
        return render_template("StudentsList.html",
                               logout='block', login='none', account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS STUDENTS LIST', accounts=getAllAccounts(search))


@app.route("/PSITS@StudentRemove/<uid>")
def psits_remove_student(uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))
    removeAccount(uid)
    databaseLog(f"Removed account ID [{uid}]")
    return redirect(url_for("psits_students_list"))


@app.route("/PSITS@Events", methods=['POST', 'GET'])
def psits_events_list():
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))

    if request.method == 'GET':
        # Get the search
        search: str = flask.request.values.get('search')
        return render_template("EventList.html",
                               logout='block', login='none', account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS EVENTS LIST', events=SEARCHEvent(search))
    else:
        search: str = flask.request.values.get('search')
        event: Event = Event(
            request.form['idnum'],
            request.form['title'],
            request.form['date_published'],
            request.form['information'],
            request.form['image_file']
        )
        UPDATEEvent(event)
        # if request.form['open'] == 'YES':
        # Email Request
        #    orders: list = getOrder(event.uid, 'RESERVED')
        #    for order in orders:
        #        user_message = f"Hello {getAccountByID(order.account_uid).firstname}!\n\n" \
        #                       f"Our {event.title} is now available for an order! The {event.item} is " \
        #                       f"priced at P{event.amount}. Login to PSITS page to order now!"
        #        if getAccountByID(order.account_uid).email is not None or "":
        #            pushEmail(Email("PSITS - " + event.title, getAccountByID(order.account_uid).email, user_message))
        # updateEvent(event)
        databaseLog(f"Updated event ID [{event.uid}] by [{session['username']}] -- {event.title}")
        return render_template("EventList.html",
                               logout='block', login='none', account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS EVENTS LIST', events=SEARCHEvent(search))


@app.route("/PSITS@EventRemove/<uid>")
def psits_remove_event(uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))
    DELETEEvent(uid)
    databaseLog(f"Removed event ID [{uid}]")
    return redirect(url_for("psits_events_list"))


@app.route("/PSITS@OrderForm/<event_uid>")
def psits_order_form_uid(event_uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    session['order_message'] = event_uid
    return redirect(url_for('psits_order_form'))


@app.route("/PSITSOrderForm")
def psits_order_form():
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    event_uid = session['order_message']
    order_account = getOrderAccount(event_uid, session['username'])
    event = getEvent(event_uid)
    user_message: str = ""
    account_status = ""
    # if user is not yet reserved, ask for reservation
    if order_account.status is None:
        user_message = f"Hello {getAccountByID(session['username']).firstname}!\n\n" \
                       f"{event.title} is now available for reservations! You can " \
                       f"request for a reservation for faster process and we'll email " \
                       f"you once we're ready. Make sure that your email address is active."
        account_status = "NOT-RESERVED"
    elif order_account.status == 'RESERVED':
        if event.open_for_payment == 'YES':
            account_status = "ORDER"
            user_message = f"Hello {getAccountByID(session['username']).firstname}!\n\n" \
                           f"Our {event.title} is now available for a  pre-order! The {event.item} is " \
                           f"priced at P{event.amount}. You can enter the amount of item you want " \
                           f"to purchase."
        else:
            user_message = f"Hello {getAccountByID(session['username']).firstname}!\n\n" \
                           f"We are currently not ready for a pre-ordering of {event.item}s, " \
                           f"however you already have reserved a slot for pre-order which is great! " \
                           f"Just come back soon or wait for the announcements from " \
                           f"PSITS page, " \
                           f"we will also notify you by email."
    elif order_account.status == 'ORDERED':
        user_message = f"Hello {getAccountByID(session['username']).firstname}!\n\n" \
                       f"You have ordered {order_account.quantity} {event.item}" \
                       f"{'s' if int(order_account.quantity) > 1 else ''} which totals to " \
                       f"P{int(order_account.quantity) * int(event.amount)}, if you have time, you can" \
                       f" visit the PSITS office at 5th floor UC Main bldg. located near room 539 for the payment."
    elif order_account.status == 'PAID':
        user_message = f"Hello {getAccountByID(session['username']).firstname}!\n\n" \
                       f"You already paid the {order_account.quantity} {event.item}" \
                       f"{'s' if int(order_account.quantity) > 1 else ''} that you have ordered " \
                       f"and your reference code is: {order_account.reference}. Please wait for the" \
                       f" announcement of the claiming schedule at the PSITS page. Thank you :D"
    return render_template('OrderForm.html',
                           title='PSITS Order',
                           logout='none',
                           login='none',
                           event=event,
                           user_message=user_message,
                           account_status=account_status)


@app.route("/PSITSOrderHandler", methods=['POST'])
def order_handler():
    """
        status return
            NOT-RESERVED (creates order reservation)
            RESERVED
            ORDERED
            PAID
            CLAIMED
    """
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    event_uid = session['order_message']
    status = request.form['status']
    if status == 'NOT-RESERVED':
        createOrder(OrderAccount(None, event_uid, session['username'], 'RESERVED', 0, ''))
        databaseLog(f"Order request | Account ID [{session['username']}] - status: RESERVATION")
    elif status == 'ORDER':
        order = getOrderAccount(event_uid, session['username'])
        order.status = 'ORDERED'
        order.quantity = request.form['quantity']
        updateOrder(order)
        order_account = getOrderAccount(event_uid, session['username'])
        event = getEvent(event_uid)
        user_message = f"Hello {getAccountByID(session['username']).firstname}!\n\n" \
                       f"You have ordered {order_account.quantity} {event.item}" \
                       f"{'s' if int(order_account.quantity) > 1 else ''} which totals to " \
                       f"P{int(order_account.quantity) * int(event.amount)}, if you have time, you can" \
                       f" visit the PSITS office at 5th floor UC Main bldg. located near room 539 for the payment."
        pushEmail(Email("PSITS - " + event.title, getAccountByID(order.account_uid).email, user_message))
        databaseLog(f"Order request | Account ID [{session['username']}] - status: ORDERED "
                    f"{request.form['quantity']} {event.item}{'s' if int(order_account.quantity) > 1 else ''}")
    return redirect(url_for('landing_page'))


@app.route("/PSITS@Orders", methods=['GET', 'POST'])
def psits_orders_list():
    if "username" not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))

    search: str = flask.request.values.get('search')
    orders = getAllOrders(search)
    total = 0.0
    paid = 0.0
    ordered = 0.0
    for order in orders:
        total += order.total
        if order.order_account.status is not None:
            if order.order_account.status == 'PAID' or order.order_account.status == 'CLAIMED':
                paid += order.total
            if order.order_account.status == 'ORDERED':
                ordered += order.total
    """"
        temp = orders.copy()
        
        new_order = []
        if len(orders) > 100:
            for i in range(0, 100):
                new_order.append(temp[i])
            orders = new_order
    """
    if request.method == 'GET':

        return render_template("OrderList.html", logout='block', login='none',
                               account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS ORDERS LIST', orders=orders, total=total,
                               reserve=ordered, paid=paid)
    else:
        order_id = request.form['order_id']
        status = request.form['status']
        if status == 'PAID':
            order = getOrderById(order_id)
            if order is not None:
                if order.status != status:
                    order.status = status
                    order.reference = request.form['reference']
                    updateOrder(order)
        elif status == 'CLAIMED':
            order = getOrderById(order_id)
            if order is not None:
                if order.status != status:
                    order.status = status
                    updateOrder(order)
        return redirect(url_for('psits_orders_list'))


@app.route("/PSITS@AboutUs")
def about_us():
    if "username" in session:
        if isAdmin(session['username']):
            return render_template("aboutUs.html",
                                   title="About Us PSITS",
                                   login="none",
                                   logout="block",
                                   account=session['username'],
                                   admin="block",
                                   account_data=getAccountByID(session['username']))
        else:
            return render_template("aboutUs.html",
                                   title="About Us PSITS",
                                   login="none", logout="block",
                                   account=session['username'],
                                   admin="none",
                                   account_data=getAccountByID(session['username']))
    return render_template("aboutUs.html",
                           title="About Us PSITS",
                           login="block",
                           logout="none", admin="none")


@app.route("/PSITS@Logout")
def logout():
    databaseLog(f"Account ID [{session['username']}] has logged out")
    session.clear()
    return redirect(url_for("landing_page"))


@app.route("/CannotFindLink")
def cant_find_link():
    return render_template("404Page.html", logout="none", login="none", title="PSITS I'm lost :<")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404Page.html", logout="none", login="none", title="PSITS I'm lost!", message=e), 404


@app.after_request
def after_request(response):
    response.headers.add('Cache-Control', 'no-store,no-cache,must-revalidate,post-check=0,pre-check=0')
    return response


def checkImageExist(name: str):
    return os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], name))


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    hostname = socket.gethostname()
    IPAddress = socket.gethostbyname(hostname)
    if databaseInit():
        databaseLog(f"Server Started, running on {IPAddress}:5000")
        # use this if you are debugging the app
        app.run(host="0.0.0.0", port=5000, debug=True)
        #
        # Production
        # serve(app, host="0.0.0.0", port=5000)
