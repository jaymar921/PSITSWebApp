from __main__ import app
import os

from flask import request, redirect, url_for, session, render_template
import json
import threading, time
import pandas as pd


from Database import SEARCHMerchOrder, SEARCHMerchandise, getAccountByID, UPDATEMerchOrder, getAccount, DELETEMerchOrder, updateAccount, databaseLog, GETAllMerchandise\
    ,getAllAccounts, getAccountWithPassword, GetAllPromo
# from EmailAPI import pushEmail
from Models import AccountOrders, MerchOrder, Merchandise, Account, ORDER_STATUS, AccountOrdersLW
from Util import GetReference, isAdmin, ifKeyPermitted, hashData, GetPriceRef
from webApp_utility import save_redirection, is_blocked_route

# GLOBALS
merch_orders: list = [] # SEARCHMerchOrder('all')
ALL_MERCHANDISE: list = []
ACCOUNT_ORDERS: list = []

# OPTIMIZE ACCOUNT ORDERS, SENDING THE WHOLE OBJECT COST A LOT
# OF RESOURCES - JAYHARRON
LIGHTWEIGHT_ACCOUNT_ORDERS: list = []

def updateMerch(updated_list, updated_merchandise):
    global merch_orders
    global ALL_MERCHANDISE
    global ACCOUNT_ORDERS
    merch_orders = updated_list
    ALL_MERCHANDISE = updated_merchandise
    ACCOUNT_ORDERS = updateAccountOrders()
    
def updateAccountOrders():
    data: list = []
    for merch_order in merch_orders:
        merch: Merchandise
        for m in ALL_MERCHANDISE:
            if m.uid == merch_order.merchandise_id:
                merch = m
        account: Account = getAccountByID(merch_order.account_id)
        account_order: AccountOrders = AccountOrders(account, merch, merch_order)
        account_order.reference = GetReference(account_order.order.reference)
        data.append(account_order)
    return data

# My logic on saving resources
def preloadAccountOrders_LightWeight():
    # Make sure that the merch_order_updater was loaded
    global ACCOUNT_ORDERS
    for ACCOUNT_ORDER in ACCOUNT_ORDERS:
        account_order: AccountOrders = ACCOUNT_ORDER
        # parse the account orders into a lightweight version and pass it as an argument to the updateOrdersLW
        updateAccountOrdersLightWeight(AccountOrdersLW.parse(account_order))

def updateAccountOrdersLightWeight(order_param: AccountOrdersLW):
    global LIGHTWEIGHT_ACCOUNT_ORDERS
    order_found: bool = False
    # Check if the LIGHTWEIGHT_ACCOUNT_ORDERS already have the entry
    # My goal is just to update it's contents and avoid
    # Adding new entries
    for order in LIGHTWEIGHT_ACCOUNT_ORDERS:
        order: AccountOrdersLW = order
        # Update the content of the light weight account orders
        if str(order.ref_code) == str(order_param.ref_code):
            order_found = True
            # see if data is changed
            if order.equals(order_param):
                continue
            # If data was changed, update the order quantity, status and info
            order.quantity = order_param.quantity
            order.status = order_param.status
            order.info = order_param.info
            order.size = order_param.size
            print(f'Updated status -> {order.toJSON()}')
            break
    if not order_found:
        LIGHTWEIGHT_ACCOUNT_ORDERS.append(order_param)

def removeAccountOrderLightWeight(reference: str):
    global LIGHTWEIGHT_ACCOUNT_ORDERS
    found_order = None
    for order in LIGHTWEIGHT_ACCOUNT_ORDERS:

        if str(order.ref_code) == reference:
            found_order = order

    if found_order is not None:
        LIGHTWEIGHT_ACCOUNT_ORDERS.remove(found_order)

# Run thread per 50s
def merch_order_updater():
    time.sleep(5)
    while True:
        # I avoid loading SQL simultaneously
        merch = SEARCHMerchOrder('all')
        time.sleep(1)
        updateMerch(merch, GETAllMerchandise())
        preloadAccountOrders_LightWeight()
        time.sleep(50)

merch_order_thread = threading.Thread(target=merch_order_updater)
merch_order_thread.start()

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
    
    ORDERS: list = []
    ORDERS_TALLY: float = 0
    TOTAL_TALLY: float = 0
    PAID_TALLY: float = 0
    #counter: int = 0

    # Prepare the searching
    product_to_search = ''
    status_to_search = ''
    student_to_search = ''
    size_to_search = ''

    if search.lower().startswith('merch:'):
        item_to_search_in_merch = search.split(":")

        if len(item_to_search_in_merch) > 1: # Product
            product_to_search = item_to_search_in_merch[1].lower()
            if len(item_to_search_in_merch)>2: # STATUS
                status_to_search = item_to_search_in_merch[2].lower()
    if search.lower().startswith('student:'):
        item_to_search_in_student = search.split(":")
        if len(item_to_search_in_student) > 1: # ID/LNAME/FNAME
            student_to_search = item_to_search_in_student[1].lower()
    if search.lower().startswith('all:'):
        item_to_search_in_merch = search.split(":")
        if len(item_to_search_in_merch) > 1: # STATUS
            status_to_search = item_to_search_in_merch[1].lower()
    if 'size:' in search.lower():
        item_to_search_in_all = search.lower().split("size:")
        if len(item_to_search_in_all) > 1: # SIZE
            size_to_search = item_to_search_in_all[1].lower().strip()
    
    global LIGHTWEIGHT_ACCOUNT_ORDERS
    for a in LIGHTWEIGHT_ACCOUNT_ORDERS:
        account_order: AccountOrdersLW = a

        # Do the search
        if product_to_search != '':
            if product_to_search.strip() not in account_order.product.lower():
                continue
        if status_to_search != '':
            if '!' in status_to_search.strip():
                stat: str = status_to_search.replace('!','').strip()
                if stat in account_order.status.lower():
                    continue
            elif status_to_search.strip() not in account_order.status.lower():
                continue
        if student_to_search != '':
            found_name: bool = False
            if student_to_search.strip() in account_order.fullname.lower():
                found_name = True
            if not found_name:
                continue
        reference_found: bool = False
        if search in account_order.ref_code:
            reference_found = True 
        if size_to_search != '':
            if str(size_to_search) not in str(account_order.size).lower():
                continue
        
        if reference_found or student_to_search or status_to_search or product_to_search or (search == 'all'):
            ORDERS.append(account_order)
            if account_order.status == ORDER_STATUS.ORDERED.value:
                ORDERS_TALLY += (account_order.discounted_price *
                                account_order.quantity)
            elif account_order.status != ORDER_STATUS.ORDERED.value and account_order.status != ORDER_STATUS.CANCELLED.value:
                PAID_TALLY += (account_order.discounted_price *
                            account_order.quantity)
            if account_order.status != ORDER_STATUS.CANCELLED.value:
                TOTAL_TALLY += (account_order.discounted_price *
                                account_order.quantity)

    ORDERS_JSON: list = []
    for ORDER_DATA in ORDERS:
        ORDERS_JSON.append(ORDER_DATA.toJSON())

    response_data: dict = {
        'reserve': ORDERS_TALLY,
        'total': TOTAL_TALLY,
        'paid': PAID_TALLY,
        'ORDERS': ORDERS_JSON,
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
    account_order.reference = GetReference(account_order.order.reference)
    # Email the USER if paid
    # if ORDER.getStatus() == ORDER_STATUS.PAID.value:
    #    pushEmail(Email("PSITS Payment receipt " + GetReference(account_order.order.reference),
    #                    account_order.account.email, messages.product_paid(account_order)))
    # elif ORDER.getStatus() == ORDER_STATUS.CANCELLED.value:
    #    pushEmail(Email("PSITS Order cancellation ", account_order.account.email,
    #                    messages.product_cancel(account_order)))

    # Update the lightweight list
    updateAccountOrdersLightWeight(AccountOrdersLW.parse(account_order))
    databaseLog(
        f'API[PUT] - Remote {request.remote_addr} - Updated Transaction record [{merch_order.reference}]')
    return {
        "status": 201,
        "message": f"RECORD UPDATED FOR {account_order.reference}"
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
    removeAccountOrderLightWeight(GetReference(ORDER.reference))
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




# create a CSV list for students and orders list
@app.route("/PSITS@CSVdata/<fn>/<search>")
def showCSVData(fn, search):
    if "username" in session:
        if isAdmin(session['username']):
            if fn is not None:
                if fn == "students":
                    students = getAllAccounts(search)
                    return render_template("CSVTemplate.html", students=students)
                elif fn == 'orders':
                    if search is None:
                        search = 'all'
                    if search == 'ALL':
                        search = search.lower()
                    data: list = []

                    data.append("\"REF #\",\"NAME\",\"PRODUCT\",\"ORDER DATE\",\"QUANTITY\",\"ADDITIONAL INFO\",\"SIZE\",\"STATUS\"\n")

                    # Prepare the searching
                    product_to_search = ''
                    status_to_search = ''
                    student_to_search = ''
                    size_to_search = ''

                    if search.lower().startswith('merch:'):
                        item_to_search_in_merch = search.split(":")

                        if len(item_to_search_in_merch) > 1: # Product
                            product_to_search = item_to_search_in_merch[1].lower()
                            if len(item_to_search_in_merch)>2: # STATUS
                                status_to_search = item_to_search_in_merch[2].lower()
                    if search.lower().startswith('student:'):
                        item_to_search_in_student = search.split(":")
                        if len(item_to_search_in_student) > 1: # ID/LNAME/FNAME
                            student_to_search = item_to_search_in_student[1].lower()
                    if search.lower().startswith('all:'):
                        item_to_search_in_merch = search.split(":")
                        if len(item_to_search_in_merch) > 1: # STATUS
                            status_to_search = item_to_search_in_merch[1].lower()
                    if 'size:' in search.lower():
                        item_to_search_in_all = search.lower().split("size:")
                        if len(item_to_search_in_all) > 1: # SIZE
                            size_to_search = item_to_search_in_all[1].lower().strip()

                    for order in LIGHTWEIGHT_ACCOUNT_ORDERS:
                        account_order: AccountOrdersLW = order
                         # Do the search
                        if product_to_search != '':
                            if product_to_search.strip() not in account_order.product.lower():
                                continue
                        if status_to_search != '':
                            if '!' in status_to_search.strip():
                                stat: str = status_to_search.replace('!','').strip()
                                if stat in account_order.status.lower():
                                    continue
                            elif status_to_search.strip() not in account_order.status.lower():
                                continue
                        if student_to_search != '':
                            found_name: bool = False
                            if student_to_search.strip() in account_order.fullname.lower():
                                found_name = True
                            if not found_name:
                                continue
                        reference_found: bool = False
                        if search in account_order.ref_code:
                            reference_found = True 
                        if size_to_search != '':
                            if str(size_to_search) not in str(account_order.size).lower():
                                continue

                        # Determine the sizes
                        size: str = ''
                        for item in account_order.info.split('\n'):
                            if 'size' in item.lower():
                                if len(item.split(':')) > 1:
                                    size = size + item.split(':')[1].strip() + ', '

                        val = f"\"{account_order.ref_code}\",\"{account_order.fullname}\",\"{account_order.product}\",\"{account_order.order_date}\",\"{account_order.quantity}\",\"{account_order.info}\",\"{size[:-2]}\",\"{account_order.status}\"\n"
                        data.append(val)

                    CSVtoExl(data)
                    
                    
                    #return render_template("CSVTemplate.html", orders=data)
                    return redirect(url_for('download_file',filename='GENERATED.csv'))

        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))

def CSVtoExl(data):
    GenerateCSVFile(data)
    read_file = pd.read_csv (app.config['UPLOAD_FOLDER'] + 'GENERATED.csv', sep='|', encoding = "ISO-8859-1")
    read_file.to_excel (app.config['UPLOAD_FOLDER'] +'GENERATED.xlsx', index = None, header=True)


def GenerateCSVFile(data):
    with open(app.config['UPLOAD_FOLDER'] + 'GENERATED.csv', 'w') as file:
        for line in data:
            file.write(line)

@app.route("/PSITS/Orders/Receipt/<uid>", methods = ['GET'])
def psits_receipt_generator(uid):
    save_redirection('psits_receipt_generator', uid)
    if is_blocked_route('psits_receipt_generator'):
        return redirect(url_for('maintenance_page'))
    try:
        order: MerchOrder = SEARCHMerchOrder(uid)[0]
        account: Account = getAccountByID(order.account_id)
        merch: Merchandise = SEARCHMerchandise(order.merchandise_id)[0]
        accountOrder: AccountOrders = AccountOrders(account, merch, order)
        total ="{:.2f}".format(int(accountOrder.order.quantity) * GetPriceRef(accountOrder.order.reference)) 
        price = '{:.2f}'.format(float(GetPriceRef(accountOrder.order.reference)))
        
        
        _addInfo = order.additional_info.split(' ')
        promocode: str = ''
        try:
            stop = False
            for fragment in _addInfo:
                if 'promocode' in fragment.lower():
                    stop = True
                    continue
                if stop:
                    promocode = fragment
                    break
        except: pass
    except:
        return redirect(url_for('cant_find_link'))
    
    promo_valid = False
    for promo in GetAllPromo():
        if promocode.strip() in promo.code:
            promo_valid = True
    if 'print' in request.args:
        try:
            if bool(request.args['print']) == True:
                accountOrder.order.additional_info = accountOrder.order.additional_info.replace('Promocode:','')
                return render_template('app_templates_1_3/PrintReceipt.html',  
                ORDER = accountOrder, 
                ref = uid, 
                total = total, 
                price = price,
                promocode=promocode,
                promocode_valid=promo_valid)
        except:
            pass
    return render_template('app_templates_1_3/Receipt.html', 
    login='none', 
    logout='none', 
    title=f'Receipt {uid}', 
    ORDER = accountOrder, 
    ref = uid, 
    total = total, 
    price = price,
    promocode=promocode,
    promocode_valid=promo_valid)