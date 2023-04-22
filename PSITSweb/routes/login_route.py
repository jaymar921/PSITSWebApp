from __main__ import app

from flask import session, redirect, url_for, render_template, request

from Database import getAnnouncements, databaseLog, getAccountByID, getAccount
import Database
from Util import hashData
import EmailAPI
import Models
from webApp_utility import has_redirection, get_redirection, get_redirection_extra, is_blocked_route
from Util import CONFIGURATION
import socket

keys: list = []

@app.route("/PSITS@Login")
def login_page():
    if is_blocked_route('landing_page'):
        return redirect(url_for('maintenance_page'))
    if 'username' in session:
        return redirect(url_for("landing_page"))
    return render_template("Login.html",
                           title="PSITS login",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="none",
                           logout="none")


@app.route("/PSITS@Logout")
def logout():
    if 'username' not in session:
        return redirect(url_for("landing_page"))
    databaseLog(f"Account ID [{session['username']}] has logged out")
    session.clear()
    return redirect(url_for("landing_page"))


# Entry point
@app.route("/PSITSLogin", methods=['POST'])
def login():
    if is_blocked_route('landing_page'):
        return redirect(url_for('maintenance_page'))
    account_id: str = request.form['id_number']
    password: str = request.form['password']
    account = getAccount(int(account_id), hashData(password))
    if account.uid is not None:
        session['username'] = account.uid
        databaseLog(f"Account [{account.lastname}, {account.firstname} - ID: {account.uid}] has logged in")
        if has_redirection():
            REDIRECTION = get_redirection()
            if 'psits_merchandise_product' in REDIRECTION or 'psits_receipt_generator' in REDIRECTION or 'gcash_payment' in REDIRECTION or 'quiz_session' in REDIRECTION or 'psits_survey_session' in REDIRECTION:
                return redirect(url_for(REDIRECTION,uid=get_redirection_extra()))
            elif REDIRECTION != '':
                return redirect(url_for(REDIRECTION))
        return redirect(url_for("landing_page"))

    account = getAccountByID(int(account_id))
    message = "Account not found!"
    if account.uid is not None:
        if getAccount(int(account_id),hashData('@password_reset')).uid is not None:
            session['username'] = account.uid
            return redirect(url_for('reset_account_password',uid=account.uid))
        message = "Invalid password"

    return render_template("Login.html",
                           title="Login PSITS",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="none",
                           logout="none",
                           message=message)


@app.route('/PSITS/ResetPassword', methods=['GET', 'POST'])
def reset_password_html():
    if request.method.lower() == 'get':
        return render_template('app_templates_1_3/password_reset.html', title='Password Reset', login='block', logout='none', message = '')
    
    # Get the USER ID
    uid = request.form['id_number']

    user = Database.getAccountByID(uid)

    if user.uid is None:
        return render_template('app_templates_1_3/password_reset.html', title='Password Reset', login='block', logout='none', message = 'Account not found')
    global keys
    key: str = hashData(f'@password_reset{uid}')
    keys.append(key)

    hostname = socket.gethostname()
    IPAddress = socket.gethostbyname(hostname)

    EmailAPI.email_verification(Models.Email(
        'Password Reset', 
        user.email, 
        f'''
        
            Hello {user.firstname} {user.lastname}, <br>
            you have requested a password reset, <br>
            click this link: <a style='font-weight:200;color:aqua;' href='http://{CONFIGURATION()['APP_HOST']}:{CONFIGURATION()['PORT']}/PSITS/ResetPassword/{user.uid}/{key}'>PASSWORD-RESET</a> <br><br>
                
            If you have not requested this. Just ignore this email.
            <br><br>
            <a style='font-weight:999;font-size:9px'>Contact the developers for any concerns</a>
        '''
        ))

    return render_template('app_templates_1_3/password_reset.html', title='Password Reset', login='block', logout='none', message = f'An Email was sent to {user.email}')


@app.route('/PSITS/ResetPassword/<uid>/<key>')
def reset_password_email_click(uid, key):
    # The the user account
    user = Database.getAccountByID(uid)
    
    Database.databaseLog(f"[{user.lastname}] requested for a password reset. An email was sent to the user.")
    Database.ResetPassword(user.uid, hashData('@password_reset'))
    global keys

    if key not in keys:
        return redirect(url_for('cant_find_link'))

    if user.uid is not None:
        session['username'] = user.uid
        databaseLog(f"Account [{user.lastname}, {user.firstname} - ID: {user.uid}] has logged in from password reset")
        return redirect(url_for('reset_account_password',uid=user.uid))
    return redirect(url_for('login_page'))
