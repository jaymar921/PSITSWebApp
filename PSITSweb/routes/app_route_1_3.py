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


#         PROFILE FEATURE
@app.route("/PSITS/Profile")
def profile_page():
    if 'username' not in session:
        save_redirection('profile_page')
        return redirect(url_for('login_page'))
    
    account: Account = Database.getAccountByID(session['username'])

    return render_template('app_templates_1_3/profile.html', account_data=account, isAdmin=isAdmin(session['username']), logout='block', login='none', title=f'{account.lastname} | Profile')

@app.route("/PSITS/Community")
def community_page():
    accounts: list = Database.getAllAccounts('all')

    psits_devs: dict = {
        # ID : ['MOTTO','USER CSS', 'BORDER CSS', {'ICON':['css': 'link']}]
        '19889781': ['FullStack Developer','border-gradient-orange shimmer','border-cool-orange',{'icons':[{'fa-brands fa-github':'https://github.com/jaymar921','fa-brands fa-youtube':'https://www.youtube.com/@jaymar921','fa-solid fa-book':'https://jaymar921.github.io/jayharronabejar/'}]}], # Jayharron
        '613000': ['PSITS Adviser','border-gradient-purple shimmer','',{'icons':[{'fa-brands fa-github':'https://github.com/dennisdurano'}]}], #Sir DD
        '20220885': ['3rd Year Rep.','border-gradient-purple','',{}], # Jeshelle
        '21471909': ['QA Tester','border-gradient-red shimmer','border-cool-red',{'icons':[{'fa-brands fa-github':'https://github.com/MikaPikaChu921'}]}], # Pia
        '19924414': ['Frontend Developer','border-gradient-green shimmer','',{'icons':[{'fa-brands fa-github':'https://github.com/natnat1432'}]}], # Nath
        '21435474': ['Asst. Treasurer','border-gradient-purple','',{}], # Aubrey
        '19841998': ['Treasurer','border-gradient-purple','',{'icons':[{'fa-brands fa-github':'https://github.com/takiii20'}]}], # Trish
        '19895283': ['PIO','border-gradient-purple','',{}], # Kevin
        '19871367': ['Auditor','border-gradient-purple','',{}], # Belmonte
        '19889898': ['Secretary','border-gradient-purple','',{}], # Sierra
        '19880152': ['4th Year Rep.','border-gradientpurple','',{}], # Ducal
        '21496369': ['Volunteer','border-gradient-purple','',{}], # Dex
        '21540950': ['Volunteer','border-gradient-purple','',{}], # Paul
        '21400973': ['Volunteer','border-gradient-purple','',{}], # Padolina
        '19903483': ['Volunteer','border-gradient-purple','',{'icons':[{'fa-brands fa-github':'https://github.com/TheOriginalReben'}]}], # Rey
        '18725242': ['2021 President','border-gradient-purple','',{}], # Sir Roi
        '19888957': ['Backend Developer','border-gradient-green shimmer','',{'icons':[{'fa-brands fa-github':'https://github.com/ha-rold1999'}]}], # Harold
        '19884253': ['Volunteer','border-gradient-purple','',{}], # Kaiser
        '19845262': ['PRO','border-gradient-purple','',{}], # Kaye
        '22597819': ['1st Year Rep.','border-gradient-purple','',{}], # Laygan
        '21502869': ['Volunteer','border-gradient-purple','',{}], # Sumotia
        '19865369': ['2022 President','border-gradient-purple','',{}], # Amaya
    }
    if 'username' not in session:
        return render_template('app_templates_1_3/community.html', logout='none', login='block', title='PSITS Community', community = accounts, devs=psits_devs)
    
    account: Account = Database.getAccountByID(session['username'])
    return render_template('app_templates_1_3/community.html', account_data=account, logout='block', login='none', title='PSITS Community', community = accounts, devs=psits_devs)
