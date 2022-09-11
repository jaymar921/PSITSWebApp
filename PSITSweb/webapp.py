import datetime
import os
import socket

import flask
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory

from Database import getAnnouncements, getAccount, getAccountByID, postAnnouncement, removeAnnouncement, \
    removeEvent, registerAccountDB, getAllAccounts, updateAccount, removeAccount, \
    getEvent, getOrderAccount, createOrder, updateOrder, getAllOrders, getOrderById, \
    databaseInit, databaseLog, CREATEEvent, SEARCHEvent, UPDATEEvent, GETAllEvent, CREATEMerchandise, \
    getLatestAnnouncement, DELETEEvent, SEARCHMerchandise, UPDATEMerchandise, GETAllMerchandise, DELETEMerchandise, \
    SEARCHPSITSOfficer, \
    CREATEPSITSOfficer, UPDATEPSITSOfficer, GETAllPSITSOfficer, GETAllFacultyMember, CREATEFacultyMember, \
    UPDATEFacultyMember, \
    SEARCHFacultyMember, SEARCHMerchOrder, CREATEMerchOrder, UPDATEMerchOrder, DELETEMerchOrder, DELETEPSITSOfficer
from EmailAPI import pushEmail
from Models import Event, Account, Email, OrderAccount, Merchandise, PSITSOfficer, FacultyMember, ORDER_STATUS, \
    MerchOrder, AccountOrders
from Util import deprecated, rankOfficers
from Util import hashData, isAdmin, contentVerifier, PriceParseRef, GetPriceRef, GetReference
from waitress import serve
import messages

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
                            file.close()
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


@app.route("/PSITS@CSVdata/<fn>/<search>")
def showCSVData(fn, search):
    if "username" in session:
        if isAdmin(session['username']):
            if fn is not None:
                if fn == "students":
                    students = getAllAccounts(search)
                    return render_template("CSVTemplate.html", students=students)

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
        if has_redirection():
            REDIRECTION = get_redirection()
            print(REDIRECTION)
            if 'psits_merchandise_product' in REDIRECTION:
                return redirect(url_for(REDIRECTION,uid=get_redirection_extra()))
            elif REDIRECTION != '':
                return redirect(url_for(REDIRECTION))
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
        CHECK: Account = getAccountByID(idno)
        if CHECK.uid is not None:
            return render_template("Login.html",
                           title="Login PSITS",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="none",
                           logout="none",
                           message=f'Account {idno} was already registed!')
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


@app.route("/PSITS@NewOfficer", methods=['POST','GET'])
def register_officer():
    if session is not None:
        if 'username' in session:
                if not isAdmin(session['username']):
                    return redirect(url_for('cant_find_link'))
        if flask.request.method == 'GET':
            account = session['username']
            return render_template("NewOfficerForm.html", login='none', logout='block', account=account, account_data=getAccountByID(account), message="")
        else:
            # POST, GET THE FIELDS FROM THE FORM
            idno = request.form['uid']
            position = request.form['position']
            birthday = request.form['birthday']

            account = getAccountByID(idno)
            if account.uid is None:
                return render_template("NewOfficerForm.html", login='none', logout='block', account=account, account_data=getAccountByID(account), message="Account not found! Make sure that the ID is registered!")

            officer = PSITSOfficer(account, position, birthday)
            
            # REGISTER PSITS OFFICER
            CREATEPSITSOfficer(officer)
            databaseLog(f"Added new officer [{officer.lastname}]")
            if 'officer_image' in request.files:
                file = request.files['officer_image']
                if file is not None:
                    if file.filename != '':
                        ext = file.filename.split(".")[1]
                        if ext in ALLOWED_EXTENSION:
                            file.filename = "officer" + str(officer.uid) + "." + ext
                            officer.image_src = "officer" + str(officer.uid) + "." + ext
                            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                            file.save(path)
                            file.close()
                            databaseLog(f"Officer [{officer.lastname}] comes with an image")
            UPDATEPSITSOfficer(officer)
            return redirect(url_for('psits_officer_list'))
            
    return redirect(url_for('cant_find_link'))


@app.route("/PSITS@NewEvent", methods=['GET', 'POST'])
def EventHandlerPSITS():
    if flask.request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('cant_find_link'))
        account = session['username']
        if isAdmin(account):
            return render_template("NewEventForm.html", login='none', logout='block', account=account, account_data=getAccountByID(account))
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
                        file.close()
                        databaseLog(f"Event [{event.title}] comes with an image")
        UPDATEEvent(event)
        return redirect(url_for("landing_page"))



@app.route("/PSITS@Faculty", methods=['GET','POST'])
def psits_faculty_members():
    if flask.request.method == 'GET':
        save_redirection('psits_faculty_members')
        if 'username' not in session:
            return render_template("Faculty.html",
                                   title="Faculty Members",
                                   MEMBERS=GETAllFacultyMember(),
                                   login="block",
                                   logout="none",
                                   admin="none",
                                   events=GETAllEvent())
        else:
            if isAdmin(session['username']):
                return render_template("Faculty.html",
                                   title="Faculty Members ADMIN",
                                   MEMBERS=GETAllFacultyMember(),
                                   login="none",
                                   logout="block",
                                   account=session['username'],
                                   admin="block",
                                   events=GETAllEvent(),
                                   account_data=getAccountByID(session['username']))
            else:
                return render_template("Faculty.html",
                                   title="Faculty Members",
                                   MEMBERS=GETAllFacultyMember(),
                                   login="none",
                                   logout="block",
                                   account=session['username'],
                                   admin="none",
                                   events=GETAllEvent(),
                                   account_data=getAccountByID(session['username']))
    else:
        # POST
        if 'username' not in session:
            return redirect(url_for('cant_find_link'))
        if isAdmin(session['username']):
            member = FacultyMember(
                None,
                request.form['name'],
                request.form['position'],
                request.form['description'],
                request.form['job']
            )
            CREATEFacultyMember(member)
            databaseLog(f"Added new faculty member [{member.name}]")
            member: FacultyMember = SEARCHFacultyMember(member.name)[0]
            if 'photo' in request.files:
                file = request.files['photo']
                if file is not None:
                    if file.filename != '':
                        ext = file.filename.split(".")[1]
                        if ext in ALLOWED_EXTENSION:
                            file.filename = "faculty" + str(member.uid) + "." + ext
                            member.image_src = "faculty" + str(member.uid) + "." + ext
                            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                            file.save(path)
                            file.close()
                            databaseLog(f"Faculty member [{member.name}] comes with an image")
            UPDATEFacultyMember(member)
            return redirect(url_for('psits_faculty_members'))


@app.route("/PSITS@OfficerList", methods=['POST','GET'])
def psits_officer_list():
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    if isAdmin(session['username']):
        if flask.request.method == 'GET':
            # Get the search
            search: str = flask.request.values.get('search')
            if search is None:
                search = 'ALL'
            return render_template("PSITSOfficerList.html",
                                logout='block', login='none', account_data=getAccountByID(session['username']),
                                admin='block', title='OFFICERS LIST',
                                accounts=GETAllPSITSOfficer(), search=search)
        else: # POST
            search: str = flask.request.values.get('search')
            OFFICER_ACCOUNT = SEARCHPSITSOfficer(request.form['idnum'])[0]
            if OFFICER_ACCOUNT is not None:
                OFFICER_ACCOUNT.position = request.form['position']
                OFFICER_ACCOUNT.birthday = request.form['birthday']
                UPDATEPSITSOfficer(OFFICER_ACCOUNT)
                databaseLog(f"Updated Officer data [{OFFICER_ACCOUNT.lastname}]")
            return render_template("PSITSOfficerList.html",
                                logout='block', login='none', account_data=getAccountByID(session['username']),
                                admin='block', title='OFFICERS LIST',
                                accounts=GETAllPSITSOfficer(), search=search)

    return redirect(url_for('cant_find_link'))


# route for my order list
@app.route("/PSITS@MyOrderList", methods=['GET'])
def psits_my_orders_list():
    if 'username' in session:
        if flask.request.method == 'GET':
            # Get all ORDERS
            myOrders = SEARCHMerchOrder(session['username'])
            ALL_ORDERS: list = []
            for order in myOrders:
                ref = GetReference(order.reference)
                merchandise = SEARCHMerchandise(order.merchandise_id)[0]
                account_order = AccountOrders(
                        getAccountByID(session['username']),
                        merchandise,
                        order
                    )
                account_order.reference = ref

                if checkImageExist("merch" + str(account_order.merch.uid) + ".png"):
                    account_order.merch.image_file = f"merch{str(account_order.merch.uid)}.png"
            
                ALL_ORDERS.append(
                    account_order
                )

            
            return render_template('MyOrders.html', orders = ALL_ORDERS, title='My Orders', logout='block', 
                    login='none', account_data=getAccountByID(session['username']))
    return redirect(url_for("login_page"))


@app.route("/PSITS@MerchandiseList", methods=['POST','GET'])
def psits_merchandise_list():
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    if isAdmin(session['username']):
        if flask.request.method == 'GET':
            # Get the search
            search: str = flask.request.values.get('search')
            if search is None:
                search = 'all'
            return render_template("MerchandiseList.html",
                                logout='block', login='none', account_data=getAccountByID(session['username']),
                                admin='block', title='OFFICERS LIST',
                                Merchandise=SEARCHMerchandise(search), search=search)
        else: # POST
            search: str = flask.request.values.get('search')
            # OFFICER_ACCOUNT = SEARCHPSITSOfficer(request.form['idnum'])[0]
            # if OFFICER_ACCOUNT is not None:
            #     OFFICER_ACCOUNT.position = request.form['position']
            #     OFFICER_ACCOUNT.birthday = request.form['birthday']
            #     UPDATEPSITSOfficer(OFFICER_ACCOUNT)
            #     databaseLog(f"Updated Officer data [{OFFICER_ACCOUNT.lastname}]")
            MERCHANDISE: Merchandise = SEARCHMerchandise(request.form['idnum'])[0]
            if MERCHANDISE is not None:
                MERCHANDISE.title = request.form['title']
                MERCHANDISE.info = request.form['info']
                MERCHANDISE.price = request.form['price']
                MERCHANDISE.discount = request.form['discount']
                MERCHANDISE.stock = request.form['stock']
                UPDATEMerchandise(MERCHANDISE)
                databaseLog(f"Updated Merchandise data [{MERCHANDISE.title}]")
            return render_template("MerchandiseList.html",
                                logout='block', login='none', account_data=getAccountByID(session['username']),
                                admin='block', title='OFFICERS LIST',
                                Merchandise=SEARCHMerchandise(search), search=search)

    return redirect(url_for('cant_find_link'))


@app.route("/PSITS@MerchandiseOrdersList", methods=['POST','GET'])
def psits_merchandise_orders_list():
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    if isAdmin(session['username']):
        if flask.request.method == 'POST':
            ORDER_ID = request.form['order_ref']
            
            # GET THE MATCHING ORDER
            ORDER: MerchOrder = SEARCHMerchOrder(ORDER_ID)[0]
            
            # SET THE ORDER STATUS
            ORDER.setStatus(request.form['status'])
            # Update database
            UPDATEMerchOrder(ORDER)

            # Grab the necessary info of the USER
            merch_order = SEARCHMerchOrder(ORDER_ID)[0]
            merch: Merchandise = SEARCHMerchandise(merch_order.merchandise_id)[0]
            account: Account = getAccountByID(merch_order.account_id)
            account_order: AccountOrders = AccountOrders(account,merch,merch_order)
            # Email the USER if paid
            if ORDER.getStatus() == ORDER_STATUS.PAID.value:
                pushEmail(Email("PSITS Payment receipt "+GetReference(account_order.order.reference), account_order.account.email, messages.product_paid(account_order)))
            elif ORDER.getStatus() == ORDER_STATUS.CANCELLED.value:
                pushEmail(Email("PSITS Order cancellation ", account_order.account.email, messages.product_cancel(account_order)))
            

        search: str = flask.request.values.get('search')
        if search is None:
            search = 'all'
        
        if search == 'ALL':
            search = search.lower()

        merch_orders = SEARCHMerchOrder(search)

        ORDERS: list = []

        ORDERS_TALLY: float = 0
        TOTAL_TALLY: float = 0
        PAID_TALLY: float = 0

        for order in merch_orders:
            merch: Merchandise = SEARCHMerchandise(order.merchandise_id)[0]
            account: Account = getAccountByID(order.account_id)
            account_order: AccountOrders = AccountOrders(account,merch,order)
            account_order.reference = GetReference(account_order.order.reference)
            ORDERS.append(account_order)

            if account_order.getStatus() == ORDER_STATUS.ORDERED.value:
                ORDERS_TALLY += (account_order.getTotal() * account_order.order.quantity)
            elif account_order.getStatus() != ORDER_STATUS.ORDERED.value and account_order.getStatus() != ORDER_STATUS.CANCELLED.value:
                PAID_TALLY += (account_order.getTotal() * account_order.order.quantity)
            
            if account_order.getStatus() != ORDER_STATUS.CANCELLED.value:
                TOTAL_TALLY += (account_order.getTotal() * account_order.order.quantity)

        return render_template('MerchOrdersList.html',
                                logout='block', 
                                login='none', 
                                account_data=getAccountByID(session['username']),
                                admin='block', 
                                title='PSITS ORDERS',
                                reserve=ORDERS_TALLY,
                                total=TOTAL_TALLY,
                                paid=PAID_TALLY,
                                ORDERS=ORDERS, search=search)
    return redirect(url_for('cant_find_link'))


@app.route("/PSITS@MerchandiseProduct/<uid>", methods=['POST','GET'])
def psits_merchandise_product(uid):
    if 'username' not in session:
        save_redirection('psits_merchandise_product',uid)
        return redirect(url_for('login_page'))
    if flask.request.method == 'GET':
        product = SEARCHMerchandise(str(uid))[0]
        stat = "NONE"
        cancel_days = 0
        order_id = ''
        if SEARCHMerchOrder(session['username']):
            orders = SEARCHMerchOrder(session['username'])
            for order in orders:
                if order.account_id == session['username'] and (order.getStatus() == ORDER_STATUS.ORDERED.value or order.getStatus() == ORDER_STATUS.PAID.value) and str(order.merchandise_id) == str(product.uid):
                    d0 = datetime.date.today()
                    d1 = order.order_date
                    delta = d1 - d0
                    cancel_days = int(delta.days+3)
                    stat = "ORDERED"
                    order_id = order.uid
                    continue
        if checkImageExist("merch" + str(product.uid) + ".png"):
            product.image_file = f"merch{str(product.uid)}.png"
        return render_template('MerchandiseProduct.html', product =  product, logout='block', login='none',
                               account_data=getAccountByID(session['username']), status=stat, cancel_days=cancel_days,order_id=order_id)


# HAROLD TASK
@app.route("/PSITS@Order", methods=['POST'])
def psits_order_product():
    """
        Task, receive order from the MerchandiseProduct(form)

        Create the object MerchOrder from Models.py
        - before initializing the object, you must know if the 
          user is logged in, then get the id from session['username']

          also get the merchandise ID, you can submit the merch id from
          the form

        - Usually when the user is ordering a product, his data is null or empty

        MerchOrder(
            None --->  uid
            account_id ---> session
            order_date ---> must be the date of ordering the product
            merchandise_id ---> from form
            status ---> ORDER_STATUS.ORDERED (Enum)
            quantity ---> grab from form
            additional_info ---> from from
            reference ---> '' (empty string)
        )

        Store the data to the database, use
        CREATEMerchOrder(order: MerchOrder) module from Database.py

        - Block the user from ordering again once they have an ongoing
          order, unless if it's status is claimed

        - When user has ordered or paid status, they must not order but
          can use the 'My Orders' webpage so they will know their orders

        - Create a simple webpage for 'My Orders'

        - Use the SEARCHMerchOrder(search: str) from the Database.py
    """
    merch_uid = 0
    if "username" in session:
        if flask.request.method == "POST":
            merch_uid = request.form['merch_id']
            account_id = session['username']
            order_date = datetime.datetime.now()
            status = ORDER_STATUS.ORDERED.value
            quantity = request.form['quantity']
            additional_info = request.form['additional_info']

            # Get the price and the discount
            merch: Merchandise = SEARCHMerchandise(merch_uid)[0]
            PRICE: int = int(merch.price)
            DISCOUNT: float = float(merch.discount)

            DISCOUNTED_PRICE: float = PRICE - (PRICE* (DISCOUNT/100))

            # Generate a reference Code
            REF_CODE: str = PriceParseRef(DISCOUNTED_PRICE)

            order = MerchOrder(
                None,
                account_id,
                order_date,
                merch_uid,
                status,
                quantity,
                additional_info,
                REF_CODE
            )
            CREATEMerchOrder(order)

            # create the AccountOrders, get the active order status
            accountOrder = AccountOrders(
                getAccountByID(session['username']),
                merch,
                SEARCHMerchOrder(order.reference)[0]
            )

            # Send email to user
            pushEmail(Email("PSITS Orders", accountOrder.account.email,messages.product_ordered(accountOrder)))

    else:
        return redirect(url_for('login_page'))
    return redirect(url_for("psits_merchandise_product",uid=merch_uid))

        
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


@app.route("/PSITS@AddMerch", methods=['POST', 'GET'])
def addMerch():
    if flask.request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('cant_find_link'))
        account = session['username']
        if isAdmin(account):
            return render_template("MerchForm.html", login='none', logout='block', account=account, account_data=getAccountByID(account))
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
        databaseLog(f"Merch [{merch.title}] added")
        merch = SEARCHMerchandise(merch.info)[0]
        if merch is not None:
            if 'merch_image' in request.files:
                file = request.files['merch_image']
                if file is not None:
                    if file.filename != '':
                        ext = file.filename.split(".")[1]
                        if ext in ALLOWED_EXTENSION:
                            file.filename = "merch" + str(merch.uid) + "." + ext
                            merch.image_file = "merch" + str(merch.uid) + "." + ext
                            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                            file.save(path)
                            file.close()
                            databaseLog(f"Merch [{merch.title}] comes with an image")
    return redirect(url_for("psits_merchandise"))


@app.route("/PSITS@Merchandise")
def psits_merchandise():
    save_redirection('psits_merchandise')
    MERCH = GETAllMerchandise()
    events: list = GETAllEvent()
    # check if merch has photo
    for merch in MERCH:
        if checkImageExist("merch" + str(merch.uid) + ".png"):
            merch.image_file = f"merch{str(merch.uid)}.png"

    

    if 'username' in session:
        account = session['username']
        if isAdmin(account):
            return render_template("Merchandise.html", all_merch=MERCH, events=events, login='none', logout='block', account=account, account_data=getAccountByID(account), admin="block")
        else:
            return render_template("Merchandise.html", all_merch=MERCH, events=events, login='none', logout='block', account=account, account_data=getAccountByID(account), admin="none")
    return render_template("Merchandise.html", all_merch=MERCH, events=events, login='block', logout='none', admin="none")


@app.route("/PSITS@RemoveMerch/<uid>")
def psits_remove_merchandise(uid):
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    account = session['username']
    if isAdmin(account):
        DELETEMerchandise(uid)
        databaseLog(f"Merch ID [{uid}] was removed by Account ID [{account}]")
        return redirect(url_for("psits_merchandise_list"))
    else:
        return redirect(url_for('cant_find_link'))
    

@app.route("/PSITS@RemoveOfficer/<uid>")
def psits_remove_officer(uid):
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    account = session['username']
    if isAdmin(account):
        DELETEPSITSOfficer(uid)
        databaseLog(f"Officer ID [{uid}] was removed by Account ID [{account}]")
        return redirect(url_for("psits_officer_list"))
    else:
         return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")


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
        if search is None:
            search = 'ALL'
        return render_template("StudentsList.html",
                               logout='block', login='none', account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS STUDENTS LIST',
                               accounts=getAllAccounts(search), search=search)
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
                               admin='block', title='PSITS STUDENTS LIST',
                               accounts=getAllAccounts(search), search=search)


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


@deprecated("Order form is deprecated")
@app.route("/PSITS@OrderForm/<event_uid>")
def psits_order_form_uid(event_uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    session['order_message'] = event_uid
    return redirect(url_for('psits_order_form'))


@app.route("/PSITS@RemoveOrder/<uid>")
def psits_order_remove(uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    databaseLog(f"User [{session['username']}] has deleted order id[{uid}]")
    DELETEMerchOrder(uid)
    return redirect(url_for('psits_merchandise_orders_list'))


@app.route("/PSITS@RequestCancel/<uid>")
def psits_order_remove_request(uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="You must be logged on to access the page!")
    ORDERS = SEARCHMerchOrder(uid)
    if len(ORDERS) > 0:
        ORDER_TO_CANCEL: MerchOrder = ORDERS[0]
        # Grab the necessary info of the USER
        merch_order = SEARCHMerchOrder(ORDER_TO_CANCEL.uid)[0]
        merch: Merchandise = SEARCHMerchandise(merch_order.merchandise_id)[0]
        account: Account = getAccountByID(merch_order.account_id)
        account_order: AccountOrders = AccountOrders(account,merch,merch_order)
        # Email the USER if paid
        pushEmail(Email("PSITS Order cancellation ", account_order.account.email, messages.product_cancel(account_order)))

        databaseLog(f"User [{session['username']}] has cancelled an order -> id[{uid}]")
        DELETEMerchOrder(uid)

    return redirect(url_for('psits_merchandise'))


@deprecated("psits order form is deprecated")
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


@deprecated("orders is deprecated")
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
    save_redirection('about_us')
    officers = GETAllPSITSOfficer()
    officers = rankOfficers(officers)
    if "username" in session:
        if isAdmin(session['username']):
            return render_template("aboutUs.html",
                                   title="About Us PSITS",
                                   login="none",
                                   logout="block",
                                   account=session['username'],
                                   admin="block",
                                   account_data=getAccountByID(session['username']),
                                   officers=officers)
        else:
            return render_template("aboutUs.html",
                                   title="About Us PSITS",
                                   login="none", logout="block",
                                   account=session['username'],
                                   admin="none",
                                   account_data=getAccountByID(session['username']),
                                   officers=officers)
    return render_template("aboutUs.html",
                            title="About Us PSITS",
                            login="block",
                            logout="none", admin="none",
                            officers=officers)


@app.route("/PSITS@Logout")
def logout():
    if 'username' not in session:
        return redirect(url_for("landing_page"))
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


def has_redirection() -> bool:
    if 'redirect' in session:
        if session['redirect'] != '':
            return True
    return False


def save_redirection(url: str, *args):
    session['redirect'] = url
    for ar in args:
        session['redirect_extra'] = ar


def get_redirection() -> str:
    url = session['redirect']
    session['redirect'] = ''
    return str(url)


def get_redirection_extra():
    if 'redirect_extra' in session:
        return session['redirect_extra']
    return ''


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
