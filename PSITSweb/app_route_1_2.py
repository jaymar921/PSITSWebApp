from __main__ import app
from flask import render_template, session, redirect, url_for, request
import flask
import Database
from Util import isAdmin, hashData

@app.route('/PSITS@PasswordReset/<uid>', methods=['POST','GET'])
def reset_password(uid):
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    
    # The the user account
    user = Database.getAccountByID(uid)
    admin_account = Database.getAccountByID(session['username'])
    if flask.request.method == 'GET':
        
        message = f"Reset password for '{user.firstname} {user.lastname}'?"
        return render_template('app_templates_1_2/ResetPassword.html',idnum=uid,logout='block',login='none',account_data=admin_account, message=message)
    
    Database.databaseLog(f"Admin [{admin_account.lastname}] reset the password for [{user.lastname}] account")
    Database.ResetPassword(user.uid, hashData('@password_reset'))
    

    return redirect(url_for('psits_students_list'))


@app.route('/PSITS@ResetPassword/<uid>', methods=['POST', 'GET'])
def reset_account_password(uid):
    if flask.request.method == 'GET':
        if int(session['username']) == int(uid):
            msg = f"Time to reset your password {Database.getAccountByID(uid).firstname}!"
            return render_template('app_templates_1_2/ResetPasswordForm.html',idnum=uid,logout='block',login='none',message=msg)
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")

    password = request.form['password']
    Database.ResetPassword(uid, hashData(password))
    Database.databaseLog(f'Password reset on account [{uid}]')
    return redirect(url_for('landing_page'))