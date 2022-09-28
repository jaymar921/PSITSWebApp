import os
from __main__ import app

import flask
from flask import render_template, request, redirect, url_for, session

from Database import getAccountByID, getAnnouncements, registerAccountDB, databaseLog, \
    CREATEPSITSOfficer, UPDATEPSITSOfficer, GETAllPSITSOfficer, SEARCHPSITSOfficer, getAllAccounts, SEARCHMerchOrder, \
    DELETEPSITSOfficer, updateAccount, removeAccount
from EmailAPI import pushEmail
from Models import Account, Email, PSITSOfficer
from Util import hashData, isAdmin
from webapp import ALLOWED_EXTENSION


# register account
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
                    orders = SEARCHMerchOrder(search)
                    return render_template("CSVTemplate.html", orders=orders)

        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))


# See all registered account
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
            search = ''
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


# Delete account
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



# register new officer
@app.route("/PSITS@NewOfficer", methods=['POST', 'GET'])
def register_officer():
    if session is not None:
        if 'username' in session:
            if not isAdmin(session['username']):
                return redirect(url_for('cant_find_link'))
        if flask.request.method == 'GET':
            account = session['username']
            return render_template("NewOfficerForm.html", login='none', logout='block', account=account,
                                   account_data=getAccountByID(account), message="")
        else:
            # POST, GET THE FIELDS FROM THE FORM
            idno = request.form['uid']
            position = request.form['position']
            birthday = request.form['birthday']

            account = getAccountByID(idno)
            if account.uid is None:
                return render_template("NewOfficerForm.html", login='none', logout='block', account=account,
                                       account_data=getAccountByID(account),
                                       message="Account not found! Make sure that the ID is registered!")

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


# See Officer List
@app.route("/PSITS@OfficerList", methods=['POST', 'GET'])
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
        else:  # POST
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


# Remove Officer
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
