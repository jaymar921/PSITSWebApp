from __main__ import app
import datetime
import os

import flask
from flask import session, render_template, redirect, url_for, request, jsonify
import json

import messages
from Database import SEARCHMerchOrder, SEARCHMerchandise, getAccountByID, UPDATEMerchOrder, getAccount, DELETEMerchOrder, updateAccount, databaseLog, GETAllMerchandise\
    ,getAllAccounts, getAccountWithPassword
from EmailAPI import pushEmail
from Models import AccountOrders, MerchOrder, Merchandise, Account, ORDER_STATUS, Email, \
    OrderAccount, PROMO
from Util import GetReference, isAdmin, ifKeyPermitted, hashData


@app.route("/PSITS/api/transactions/<search>", methods=['GET'])
def api_transactions_get(search):

    request_key = request.args.get('key')

    if not request_key:
        databaseLog(
            f'API[GET] - Remote {request.remote_addr} - Tried to access Transactions ["{search}"] with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[GET] - Remote {request.remote_addr} - Tried to access Transactions ["{search}"] with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }

    if search is None:
        search = 'all'
    if search == 'ALL':
        search = search.lower()
    merch_orders = SEARCHMerchOrder(search)
    ORDERS: list = []
    ORDERS_TALLY: float = 0
    TOTAL_TALLY: float = 0
    PAID_TALLY: float = 0
    #counter: int = 0
    for order in merch_orders:
        #counter += 1
        # if counter == 100:
        #    break
        merch: Merchandise = SEARCHMerchandise(order.merchandise_id)[0]
        account: Account = getAccountByID(order.account_id)
        account_order: AccountOrders = AccountOrders(account, merch, order)
        account_order.reference = GetReference(account_order.order.reference)
        ORDERS.append(account_order)
        if account_order.getStatus() == ORDER_STATUS.ORDERED.value:
            ORDERS_TALLY += (account_order.getTotal() *
                             account_order.order.quantity)
        elif account_order.getStatus() != ORDER_STATUS.ORDERED.value and account_order.getStatus() != ORDER_STATUS.CANCELLED.value:
            PAID_TALLY += (account_order.getTotal() *
                           account_order.order.quantity)
        if account_order.getStatus() != ORDER_STATUS.CANCELLED.value:
            TOTAL_TALLY += (account_order.getTotal() *
                            account_order.order.quantity)

    ORDERS_JSON: list = []
    for ORDER_DATA in ORDERS:
        ORDERS_JSON.append(ORDER_DATA.toJSON())

    MERCH_JSON: list = []
    for MERCHANDISE in GETAllMerchandise():
        MERCH_JSON.append(MERCHANDISE.toJSON())

    response_data: dict = {
        'reserve': ORDERS_TALLY,
        'total': TOTAL_TALLY,
        'paid': PAID_TALLY,
        'ORDERS': ORDERS_JSON,
        'merchandise': MERCH_JSON,
        'search': search,
        'status': 200
    }
    databaseLog(
        f'API[GET] - Remote {request.remote_addr} - Permitted to access Transactions ["{search}"]')
    response = app.response_class(
        response=json.dumps(response_data, indent=4,
                            sort_keys=False, default=str),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/PSITS/api/transactions", methods=['PUT'])
def api_transactions_update():

    request_key = request.args.get('key')
    if not request_key:
        databaseLog(
            f'API[PUT] - Remote {request.remote_addr} - Tried to access Update Transactions with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[PUT] - Remote {request.remote_addr} - Tried to access Update Transactions with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }

    try:
        ORDER_ID = request.get_json()['reference']
    except:
        return {
            "status": 500,
            "message": f"There was an error on the server side on updating the order."
        }
    if not ORDER_ID:
        return {
            "status": 404,
            "message": f"EMPTY REFERENCE"
        }

    # GET THE MATCHING ORDER
    ORDER: MerchOrder = SEARCHMerchOrder(ORDER_ID)[0]
    if not ORDER:
        return {
            "status": 404,
            "message": f"ORDER NOT FOUND"
        }
    # SET THE ORDER STATUS
    ORDER.setStatus(request.get_json()['stat'])

    # Setting other attributes
    try:
        if request.get_json()['info']:
            ORDER.additional_info = request.get_json()['info']
        if request.get_json()['qty']:
            ORDER.quantity = request.get_json()['qty']
    except:
        pass

    # Update database
    UPDATEMerchOrder(ORDER)

    # Grab the necessary info of the USER
    merch_order = SEARCHMerchOrder(ORDER.reference)[0]
    merch: Merchandise = SEARCHMerchandise(merch_order.merchandise_id)[0]
    account: Account = getAccountByID(merch_order.account_id)
    account_order: AccountOrders = AccountOrders(account, merch, merch_order)
    # Email the USER if paid
    # if ORDER.getStatus() == ORDER_STATUS.PAID.value:
    #    pushEmail(Email("PSITS Payment receipt " + GetReference(account_order.order.reference),
    #                    account_order.account.email, messages.product_paid(account_order)))
    # elif ORDER.getStatus() == ORDER_STATUS.CANCELLED.value:
    #    pushEmail(Email("PSITS Order cancellation ", account_order.account.email,
    #                    messages.product_cancel(account_order)))

    databaseLog(
        f'API[PUT] - Remote {request.remote_addr} - Updated Transaction record [{merch_order.reference}]')
    return {
        "status": 201,
        "message": "RECORD UPDATED"
    }


@app.route("/PSITS/api/transactions/<ref>", methods=['DELETE'])
def api_transactions_delete(ref):
    request_key = request.args.get('key')
    if not request_key:
        databaseLog(
            f'API[DELETE] - Remote {request.remote_addr} - Tried to access Delete Transactions [{ref}] with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[DELETE] - Remote {request.remote_addr} - Tried to access Delete Transactions [{ref}] with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }

    ORDER_ID = ref

    if not ref:
        return {
            "status": 404,
            "message": f"REFERENCE EMPTY"
        }

    # get the password
    try:
        PASSWORD = request.get_json()['password']
        USERID = request.get_json()['userid']
        ACCOUNT: Account = getAccount(USERID, f"{hashData(PASSWORD)}")
        if ACCOUNT.uid is None:
            ACCOUNT_ATTEMPT: Account = getAccountByID(USERID)
            if ACCOUNT_ATTEMPT.uid is not None:
                databaseLog(
                    f'API[DELETE] - Remote {request.remote_addr} - Tried to access Delete Transactions [{ref}] with invalid Admin account password')
                return {
                    "status": 403,
                    "message": f"ACCESS DENIED: ACCOUNT INVALID PASSWORD"
                }
            databaseLog(
                f'API[DELETE] - Remote {request.remote_addr} - Tried to access Delete Transactions [{ref}] with invalid Admin account')
            return {
                "status": 403,
                "message": f"ACCESS DENIED: ACCOUNT NOT FOUND"
            }
        if not isAdmin(ACCOUNT.uid):
            databaseLog(
                f'API[DELETE] - Remote {request.remote_addr} - Tried to access Delete Transactions [{ref}] with invalid Admin account')
            return {
                "status": 403,
                "message": f"ACCESS DENIED: NO ADMIN CREDENTIAL"
            }
    except:
        return {
            "status": 500,
            "message": f"There was an error on the server side on updating the order."
        }
    if not ORDER_ID:
        return {
            "status": 404,
            "message": f"EMPTY PASSWORD"
        }

    # GET THE MATCHING ORDER
    ORDER: MerchOrder = SEARCHMerchOrder(ORDER_ID)[0]
    if not ORDER:
        databaseLog(
            f'API[DELETE] - Remote {request.remote_addr} - Tried to access Delete Transactions [{ref}]: Reference code not found')
        return {
            "status": 404,
            "message": f"ORDER NOT FOUND"
        }
    # DELETE THE ORDER

    DELETEMerchOrder(ORDER.uid)
    databaseLog(
        f'API[DELETE] - Remote {request.remote_addr} - Permitted to delete Transaction Ref: [{ref}]')
    return {
        "status": 200,
        "message": "RECORD DELETED"
    }


@app.route("/PSITS/api/accounts", methods=['POST'])
def api_account_update():

    try:
        student_id = request.form['stud_id']
        rfid = request.form['rfid']
        lname = request.form['lname']
        fname = request.form['fname']
        course = request.form['course']
        year = request.form['year']

        student_data: Account = getAccountByID(student_id)

        student_data.rfid = rfid
        student_data.lastname = lname
        student_data.firstname = fname
        student_data.course = course
        student_data.year = year

        updateAccount(student_data)
        # SAVE IMAGE
        if 'image' in request.files:
            file = request.files['image']
            if file is not None:
                if file.filename != '':
                    ext = file.filename.split(".")[1]

                    file.filename = "user" + str(student_id) + "." + ext
                    path = os.path.join(
                        app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(path)
                    file.close()
        databaseLog(
            f"API[PUT] Profile [{student_data.firstname} {student_data.lastname}] was updated")

    except:
        return {
            "status": 500,
            "message": "Invalid data format received"
        }
    return {
        "status": 200,
        "message": "ACCOUNT UPDATED"
    }


@app.route('/PSITS/api/accounts/<search>', methods=['GET'])
def api_account_search(search):
    request_key = request.args.get('key')

    if not request_key:
        databaseLog(
            f'API[GET] - Remote {request.remote_addr} - Tried to access accounts ["{search}"] with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[GET] - Remote {request.remote_addr} - Tried to access accounts ["{search}"] with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }
    if search is None:
        search = 'all'
    if search == 'ALL':
        search = search.lower()
    
    ACCOUNTS: list = []
    db_data = getAllAccounts(search)

    for a in db_data:
        ACCOUNTS.append(a.toJSON())
    databaseLog(
        f'API[GET] - Remote {request.remote_addr} - Permitted to access accounts ["{search}"]')
    response = app.response_class(
        response=json.dumps(ACCOUNTS, indent=4,
                            sort_keys=False, default=str),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/PSITS/api/accounts_p/<search>', methods=['GET'])
def api_account_p_search(search):
    request_key = request.args.get('key')

    if not request_key:
        databaseLog(
            f'API[GET] - Remote {request.remote_addr} - Tried to access accounts ["{search}"] with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[GET] - Remote {request.remote_addr} - Tried to access accounts ["{search}"] with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }
    if search is None:
        search = 0
    try:
        if int(search) > 0:
            pass
    except:
        return {
            "status": 500,
            "message": f"Invalid ID number, should be a number not a string"
        }
    account: Account = getAccountWithPassword(search)
    databaseLog(
        f'API[GET] - Remote {request.remote_addr} - Permitted to access accounts ["{search}"]')
    response = app.response_class(
        response=json.dumps(account.toJSON(), indent=4,
                            sort_keys=False, default=str),
        status=200,
        mimetype='application/json'
    )
    return response