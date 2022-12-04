from __main__ import app
import datetime

import flask
from flask import session, render_template, redirect, url_for, request

import messages
from Database import SEARCHMerchOrder, SEARCHMerchandise, getAccountByID, UPDATEMerchOrder, \
    CREATEMerchOrder, databaseLog, DELETEMerchOrder, SEARCHMerchOrderTABLE, getOrderAccount, getEvent, createOrder, \
    updateOrder, getOrderById, getAllOrders, DeductPromoSlot, GetPromo
from EmailAPI import pushEmail
from Models import AccountOrders, MerchOrder, Merchandise, Account, ORDER_STATUS, Email, \
    OrderAccount, PROMO
from Util import GetReference, isAdmin, PriceParseRef, deprecated, hashData, CONFIGURATION
from webApp_utility import checkImageExist


API_LINK: str = CONFIGURATION()['API_LINK'] if (
    'true' in CONFIGURATION()['API_ALLOW_HOOK'].lower()) else ''


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

            return render_template('MyOrders.html', orders=ALL_ORDERS, title='My Orders', logout='block',
                                   login='none', account_data=getAccountByID(session['username']))
    return redirect(url_for("login_page"))


@app.route("/PSITS@MerchandiseOrdersList", methods=['POST', 'GET'])
def psits_merchandise_orders_list():
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    if isAdmin(session['username']):
        # if flask.request.method == 'POST':

        # # print(request.get_json())
        # ORDER_ID = request.form['order_ref']

        # # GET THE MATCHING ORDER
        # ORDER: MerchOrder = SEARCHMerchOrder(ORDER_ID)[0]

        # # SET THE ORDER STATUS
        # ORDER.setStatus(request.form['status'])
        # # Update database
        # UPDATEMerchOrder(ORDER)

        # # Grab the necessary info of the USER
        # merch_order = SEARCHMerchOrder(ORDER_ID)[0]
        # merch: Merchandise = SEARCHMerchandise(merch_order.merchandise_id)[0]
        # account: Account = getAccountByID(merch_order.account_id)
        # account_order: AccountOrders = AccountOrders(account, merch, merch_order)
        # # Email the USER if paid
        # if ORDER.getStatus() == ORDER_STATUS.PAID.value:
        #     pushEmail(Email("PSITS Payment receipt " + GetReference(account_order.order.reference),
        #                     account_order.account.email, messages.product_paid(account_order)))
        # elif ORDER.getStatus() == ORDER_STATUS.CANCELLED.value:
        #     pushEmail(Email("PSITS Order cancellation ", account_order.account.email,
        #                     messages.product_cancel(account_order)))

        search: str = flask.request.values.get('search')
        if search is None:
            search = 'all'

        if search == 'ALL':
            search = search.lower()
        print(API_LINK)
        return render_template('MerchOrdersList.html',
                               logout='block',
                               login='none',
                               account_data=getAccountByID(
                                   session['username']),
                               admin='block',
                               title='PSITS ORDERS',
                               #                       reserve=ORDERS_TALLY,
                               #                       total=TOTAL_TALLY,
                               #                       paid=PAID_TALLY,
                               #                       ORDERS=ORDERS,
                               search=search,
                               key="API_SECRET-" + \
                                   hashData(
                                       str((int(session['username'])*250))),
                               api_link=API_LINK)
    return redirect(url_for('cant_find_link'))


@app.route("/PSITS@Order", methods=['POST'])
def psits_order_product():
    merch_uid = 0
    if "username" in session:
        if flask.request.method == "POST":
            merch_uid = request.form['merch_id']
            account_id = session['username']
            order_date = datetime.datetime.now()
            status = ORDER_STATUS.ORDERED.value
            quantity = request.form['quantity']
            additional_info = request.form['additional_info']
            promocode = request.form['promocode']

            # Get the price and the discount
            merch: Merchandise = SEARCHMerchandise(merch_uid)[0]
            PRICE: int = int(merch.price)
            DISCOUNT: float = float(merch.discount)

            DISCOUNTED_PRICE: float = PRICE - (PRICE * (DISCOUNT/100))

            # get the promo
            promo: PROMO = GetPromo(promocode)

            if promo is not None:
                if promo.slot > 0 and promo.merch == int(merch_uid):
                    # calculate the percentage
                    total = PRICE * int(quantity)
                    percentage = promo.discount/total
                    DISCOUNTED_PRICE = DISCOUNTED_PRICE - \
                        (DISCOUNTED_PRICE * percentage)
                    DeductPromoSlot(promo.code)

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
            # pushEmail(Email("PSITS Orders", accountOrder.account.email,messages.product_ordered(accountOrder, promo)))

            # Log the order
            databaseLog(f"Order [{str(order)}] was created")
            return redirect(url_for("psits_receipt_generator", uid=GetReference(REF_CODE)))

    else:
        return redirect(url_for('login_page'))
    return redirect(url_for("psits_merchandise_product", uid=merch_uid))


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


@app.route("/PSITS@RequestCancel/<ref>")
def psits_order_remove_request(ref):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="You must be logged on to access the page!")
    ORDERS = SEARCHMerchOrderTABLE(ref)
    if len(ORDERS) > 0:
        for ORDER in ORDERS:
            if ORDER.getStatus() == ORDER_STATUS.CANCELLED.value:
                continue
            ORDER_TO_CANCEL: MerchOrder = ORDER
            # Grab the necessary info of the USER
            # merch_order: MerchOrder = SEARCHMerchOrderTABLE(ORDER_TO_CANCEL.uid)[0]
            # merch: Merchandise = SEARCHMerchandise(merch_order.merchandise_id)[0]
            # account: Account = getAccountByID(merch_order.account_id)
            # account_order: AccountOrders = AccountOrders(account,merch,merch_order)
            # Email the USER if paid
            # pushEmail(Email("PSITS Order cancellation ", account_order.account.email, messages.product_cancel(account_order)))

            databaseLog(
                f"User [{session['username']}] has cancelled an order -> id[{ref}]")
            ORDER_TO_CANCEL.setStatus('CANCELLED')
            UPDATEMerchOrder(ORDER_TO_CANCEL)
            break

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
        createOrder(OrderAccount(None, event_uid,
                    session['username'], 'RESERVED', 0, ''))
        databaseLog(
            f"Order request | Account ID [{session['username']}] - status: RESERVATION")
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
        pushEmail(Email("PSITS - " + event.title,
                  getAccountByID(order.account_uid).email, user_message))
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
                               account_data=getAccountByID(
                                   session['username']),
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
