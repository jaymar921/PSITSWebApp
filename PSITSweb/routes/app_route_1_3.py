from __main__ import app
from datetime import datetime
import os
from flask import render_template, session, redirect, url_for, request, flash
import flask
import Database
import json  
from Models import STATIC_DATA, Account, MerchOrder, ORDER_STATUS, Merchandise
from Util import isAdmin, hashData, allowed_file, directoryExist, createDir, getNumberOfFiles, fileExist, removeFile, GetPriceRef
from webApp_utility import save_redirection, checkImageExist, block_route, is_blocked_route, unblock_route, has_redirection, get_redirection, get_redirection_extra

@app.route("/PSITS@DataAnalytics/", methods = ['GET'])
def psits_data_analytics():
    if 'username' not in session:
        save_redirection('psits_data_analytics')
        return redirect(url_for('login_page'))
    ADMIN_ACCOUNT: Account = Database.getAccountByID(session['username'])
    if not isAdmin(session['username']):
        return redirect(url_for('landing_page'))

    # get all merch order
    dataset = Database.GETAllMerchOrder()
    merchandise_data = Database.GETAllMerchandise()
    account_data = Database.getAllAccounts('all')

    monthly_revenue: dict = {}
    department_sales: dict = {}
    student_levels: dict = {}
    student_courses: dict = {}

    montly_orders: dict = {}
    department_orders: dict = {}

    for data in dataset:
        order: MerchOrder = data
        date_fragment = str(order.order_date).split('-')
        key_format = date_fragment[0] + " " + date_fragment[1]
        # check if monthly_orders has a key, format 'YYYY MM'
        if order.getStatus() == ORDER_STATUS.ORDERED.value:
            # MONTLY ORDERS AND DEPARTMENT ORDERS
            if key_format in montly_orders:
                # get the value
                orders = montly_orders[key_format]
                # update the monthly orders
                montly_orders[key_format] = orders + (GetPriceRef(order.reference) * order.quantity)
            else:
                # add a new entry to the monthly orders
                montly_orders[key_format] = (GetPriceRef(order.reference) * order.quantity)
            
            
            merch_item = ''
            for item in merchandise_data:
                if int(item.uid) == int(order.merchandise_id):
                    merch_item = item.title
                    break

            # check if department sales has the key, format 'STRING'
            if merch_item in department_orders:
                # get the value
                _orderVal = department_orders[merch_item]
                # update the sales
                department_orders[merch_item] = _orderVal + int(order.quantity)
            else:
                # add a new entry to the department sales
                department_orders[merch_item] = int(order.quantity)
        elif order.getStatus() == ORDER_STATUS.CANCELLED.value:
            continue
        else:
            # MONTHLY SALES AND DEPARTMENT SALES
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
                department_sales[merch_item] = sold + int(order.quantity)
            else:
                # add a new entry to the department sales
                department_sales[merch_item] = int(order.quantity)
        
    # grab all accounts data
    for data in account_data:
        account: Account = data

        if account.course in student_courses:
            # get the value
            population = student_courses[account.course]
            # update the population
            student_courses[account.course] = population + 1
        else:
            # add a new course population
            student_courses[account.course] = 1
        
        year = account.year 
        if str(year) == '5':
            year = 'ALUMNI'
        if year in student_levels:
            # get the value
            population = student_levels[year]
            # update the population
            student_levels[year] = population + 1
        else:
            # add a new entry to the level population
            student_levels[year] = 1
    return render_template('app_templates_1_3/DataAnalytics.html', title = 'PSITS Data Analytic',
                                logout='block', login='none', account_data=ADMIN_ACCOUNT,
                                admin='block',monthly_revenue = json.dumps(monthly_revenue), department_sales = json.dumps(department_sales),
                                student_courses = json.dumps(student_courses), student_levels = json.dumps(student_levels), montly_orders = json.dumps(montly_orders), department_orders = json.dumps(department_orders))


@app.route('/PSITS@Routes', methods = ['GET', 'POST'])
def psits_routes_controller():
    if 'username' not in session:
        save_redirection('psits_routes_controller')
        return redirect(url_for('login_page'))
    ADMIN_ACCOUNT: Account = Database.getAccountByID(session['username'])
    if not isAdmin(session['username']):
        return redirect(url_for('landing_page'))
    
    form_fields: list = ['merch_route', 'announcement_route', 'about_page', 'faculty_route', 'receipt_route']
    form_map: dict = {
        'merch_route':'checked' if not is_blocked_route('psits_merchandise') else '',
        'announcement_route':'checked' if not is_blocked_route('landing_page') else '',
        'about_page':'checked' if not is_blocked_route('about_us') else '',
        'faculty_route':'checked' if not is_blocked_route('psits_faculty_members') else '',
        'receipt_route':'checked' if not is_blocked_route('psits_receipt_generator') else ''
        }
    
    if flask.request.method == 'POST':
        for field in form_fields:
            if request.form.get(field):
                form_map[field] = 'checked'
                print(f"ADMIN [{ADMIN_ACCOUNT.firstname} {ADMIN_ACCOUNT.lastname}] has set {field} route available")
            else: 
                form_map[field] = ''
                print(f"ADMIN [{ADMIN_ACCOUNT.firstname} {ADMIN_ACCOUNT.lastname}] has set {field} route on maintenance")
            


    unblock_route('psits_merchandise') if 'checked' in form_map['merch_route'] else block_route('psits_merchandise')
    unblock_route('landing_page') if 'checked' in form_map['announcement_route'] else block_route('landing_page')
    unblock_route('about_us') if 'checked' in form_map['about_page'] else block_route('about_us')
    unblock_route('psits_faculty_members') if 'checked' in form_map['faculty_route'] else block_route('psits_faculty_members')
    unblock_route('psits_receipt_generator') if 'checked' in form_map['receipt_route'] else block_route('psits_receipt_generator')

    # get request
    return render_template('app_templates_1_3/RouteController.html', title = 'Route Controller', logout = 'block', login ='none', account_data = ADMIN_ACCOUNT, admin='block',
                        merch_route=form_map['merch_route'], announcement_route=form_map['announcement_route'], about_page=form_map['about_page'], faculty_route=form_map['faculty_route'], receipt_route=form_map['receipt_route'])


@app.route("/PSITS@Maintenance")
def maintenance_page():
    return render_template('app_templates_1_3/Maintenance.html')


@app.route("/PSITS@Redirect")
def maintenance_after_redirect():
    if has_redirection():
            REDIRECTION = get_redirection()
            if 'psits_merchandise_product' in REDIRECTION or 'psits_receipt_generator' in REDIRECTION:
                return redirect(url_for(REDIRECTION,uid=get_redirection_extra()))
            elif REDIRECTION != '':
                return redirect(url_for(REDIRECTION))
    return render_template('app_templates_1_3/Maintenance.html')