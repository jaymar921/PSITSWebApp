import datetime
import os
from __main__ import app

import flask
import json
from flask import session, redirect, url_for, render_template, request, jsonify

from Database import SEARCHMerchandise, getAccountByID, UPDATEMerchandise, databaseLog, \
    SEARCHMerchOrder, CREATEMerchandise, GETAllMerchandise, GETAllEvent, DELETEMerchandise, AddPromo, GetAllPromo, DeletePromo
from Models import Merchandise, ORDER_STATUS, STATIC_DATA
from Util import isAdmin, GetReference, contentVerifier
from webApp_utility import save_redirection, checkImageExist
from webapp import ALLOWED_EXTENSION


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
                                admin='block', title='Merchandise List',
                                Merchandise=SEARCHMerchandise(search), search=search, Promos=GetAllPromo())
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
                                admin='block', title='Merchandise List',
                                Merchandise=SEARCHMerchandise(search), search=search, Promos=GetAllPromo())

    return redirect(url_for('cant_find_link'))


@app.route("/PSITS@MerchandiseProduct/<uid>", methods=['POST','GET'])
def psits_merchandise_product(uid):
    if 'username' not in session:
        save_redirection('psits_merchandise_product',uid)
        return redirect(url_for('login_page'))
    if flask.request.method == 'GET':
        product: Merchandise = SEARCHMerchandise(str(uid))[0]
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
                    stat = order.getStatus()
                    order_id = GetReference(order.reference)
                    continue
        if checkImageExist("merch" + str(product.uid) + ".png"):
            product.image_file = f"merch{str(product.uid)}.png"
            for num in range(0,5):
                if checkImageExist("merch" + str(product.uid) + f"_{num}" + ".png"):
                    product.image_file_extras.append(f"merch{str(product.uid)}_{num}.png")
        return render_template('MerchandiseProduct.html', title=uid, product =  product, img_extras = product.image_file_extras, logout='block', login='none',
                               account_data=getAccountByID(session['username']), status=stat, cancel_days=cancel_days,order_id=order_id)


@app.route("/PSITS@AddMerch", methods=['POST', 'GET'])
def addMerch():
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    account = session['username']
    if flask.request.method == 'GET':
        if isAdmin(account):
            return render_template("MerchForm.html", title='New Merchandise!', login='none', logout='block', account=account,
                                   account_data=getAccountByID(account))
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
        if len(SEARCHMerchandise(merchName)) == 0:
            CREATEMerchandise(merch)
            databaseLog(f"Merch [{merchName}] added")
            merch = SEARCHMerchandise(merchName)[0]
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
        else:
            return render_template("MerchForm.html", login='none', logout='block', account=account,
                                   account_data=getAccountByID(account),
                                   message="Merch Name already exist")
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
            return render_template("Merchandise.html", title='PSITS Merch!', all_merch=MERCH, events=events, login='none', logout='block',
                                   account=account, account_data=getAccountByID(account), admin="block",
                                   STATIC_DATA=STATIC_DATA())
        else:
            return render_template("Merchandise.html", title='PSITS Merch!', all_merch=MERCH, events=events, login='none', logout='block',
                                   account=account, account_data=getAccountByID(account), admin="none",
                                   STATIC_DATA=STATIC_DATA())
    return render_template("Merchandise.html", title='PSITS Merch!', all_merch=MERCH, events=events, login='block', logout='none',
                           admin="none", STATIC_DATA=STATIC_DATA())


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


@app.route("/PSITS@AddPromo", methods=['POST'])
def add_promo():
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    
    if 'username' in session:
        account = session['username']
        if not isAdmin(account):
            return redirect(url_for('cant_find_link'))

    # grab the info from the form
    promo_code: str = request.form['promocode']
    merch_id: int = request.form['applicable']
    discount: float = request.form['discount']
    slot: int = request.form['slot']

    databaseLog(f"Promo code [{promo_code}] was created by ID[{session['username']}]")
    AddPromo(promo_code, merch_id, discount, slot)
    return redirect(url_for('psits_merchandise_list'))

@app.route("/PSITS@RemovePromo", methods=['POST'])
def remove_promo():
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    
    if 'username' in session:
        account = session['username']
        if not isAdmin(account):
            return redirect(url_for('cant_find_link'))

    # grab the info from the form
    #promo_code: str = request.data.replace('\'','')
    json_data = request.json
    databaseLog(f"Promo [{str(json_data)}] was removed")
    DeletePromo(str(json_data))

    return redirect(url_for('psits_merchandise_list'))