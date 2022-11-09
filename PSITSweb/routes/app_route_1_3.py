from __main__ import app
from datetime import datetime
import os
from flask import render_template, session, redirect, url_for, request, flash
import flask
import Database
import json  
from Models import STATIC_DATA, Account, MerchOrder, ORDER_STATUS, Merchandise
from Util import isAdmin, hashData, allowed_file, directoryExist, createDir, getNumberOfFiles, fileExist, removeFile, GetPriceRef
from webApp_utility import save_redirection, checkImageExist

@app.route("/PSITS@DataAnalytics/", methods = ['GET'])
def psits_data_analytics():
    if 'username' not in session:
        save_redirection('psits_data_analytics')
        return redirect(url_for('login_page'))
    account: Account = Database.getAccountByID(session['username'])
    if not isAdmin(session['username']):
        return redirect(url_for('landing_page'))

    # get all merch order
    dataset = Database.GETAllMerchOrder()
    merchandise_data = Database.GETAllMerchandise()

    monthly_revenue: dict = {}
    department_sales: dict = {}

    for data in dataset:
        order: MerchOrder = data

        if order.getStatus() == ORDER_STATUS.CANCELLED.value or order.getStatus() == ORDER_STATUS.ORDERED.value:
            continue
        
        date_fragment = str(order.order_date).split('-')
        # check if monthly_revenue has a key, format 'YYYY MM'
        key_format = date_fragment[0] + " " + date_fragment[1]
        if key_format in monthly_revenue:
            # get the value
            revenue = monthly_revenue[key_format]
            # update the monthly revenue
            monthly_revenue[key_format] = revenue + (GetPriceRef(order.reference) * order.quantity)
        else:
            # add a new entry to the monthly revenue
            monthly_revenue[key_format] = (GetPriceRef(order.reference) * order.quantity)
        
        
        merch_item = ''
        for item in merchandise_data:
            if int(item.uid) == int(order.merchandise_id):
                merch_item = item.title
                break

        # check if department sales has the key, format 'STRING'
        if merch_item in department_sales:
            # get the value
            sold = department_sales[merch_item]
            # update the sales
            department_sales[merch_item] = sold + 1
        else:
            # add a new entry to the department sales
            department_sales[merch_item] = 1
        
    return render_template('app_templates_1_3/DataAnalytics.html',
                                logout='block', login='none', account_data=account,
                                admin='block',monthly_revenue = json.dumps(monthly_revenue), department_sales = json.dumps(department_sales))