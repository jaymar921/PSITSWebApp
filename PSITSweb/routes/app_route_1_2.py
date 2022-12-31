from __main__ import app
import os
from flask import render_template, session, redirect, url_for, request, flash
import flask
import Database
from Models import STATIC_DATA
from Util import isAdmin, hashData, allowed_file, directoryExist, createDir, getNumberOfFiles, fileExist, removeFile
from webapp import save_redirection


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
        if 'username' not in session:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but there was an error at the server side, please try again")
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


@app.route('/PSITS/PrintingService')
def psits_printing_service():
    return render_template("app_templates_1_2/PrintingRequest.html", title='Printing Service', logout="none", login="none", STATIC_DATA=STATIC_DATA)


@app.route('/PSITS/PrintingService/Request', methods=['POST'])
def psits_printing_request():
    student_id = request.form['idnum']

    # check if the files are sent
    if 'files[]' in request.files:
        files = request.files.getlist('files[]')
        
        directory = app.config['UPLOAD_FOLDER']+f"Printing/{student_id}/"

        #if directoryExist(directory):
        #    if getNumberOfFiles(directory) > 0:
        #        return redirect(url_for('printing_service_files', title='Printing Service',uid=student_id,msg='You have pending documents for printing, you cannot upload unless you\'ve cleared this directory'))
        for file in files:
            if file and allowed_file(file.filename):
                filenmame = file.filename

                
                
                if not directoryExist(directory):
                    createDir(directory)
                file.save(os.path.join(directory, filenmame))
        
        Database.databaseLog(f"[Printing Service] student [{student_id}] has sent {len(files)} file(s) to print")
        return redirect(url_for('printing_service_files', title='Printing Service',uid=student_id,msg='ok'))
    return redirect('/')


@app.route('/PSITS/PrintingService/files/<uid>/<msg>')
def printing_service_files(uid,msg):
    directory = app.config['UPLOAD_FOLDER']+f"Printing/{uid}/"
    if not directoryExist(directory):
        if 'username' in session:
            return render_template("app_templates_1_2/PrintingRequestFiles.html", title='Printing Service',account_data=Database.getAccountByID(session['username']),logout="block", login="none",uid=0, FILES=[], message=msg, admin=True)
        return render_template("app_templates_1_2/PrintingRequestFiles.html", title='Printing Service', logout="none", login="none",uid=0, FILES=[], message='ok', admin=False)

    files = []
    for file in os.listdir(directory):
        files.append(file)
    
    if 'username' in session:
        if isAdmin(session['username']):
            return render_template("app_templates_1_2/PrintingRequestFiles.html", title='Printing Service',account_data=Database.getAccountByID(session['username']),logout="block", login="none",uid=uid, FILES=files, message=msg, admin=True)

    return render_template("app_templates_1_2/PrintingRequestFiles.html", title='Printing Service', logout="none", login="none",uid=uid, FILES=files, message=msg, admin=False)


@app.route('/PSITS/PrintingService/Remove/<uid>/<filename>')
def printing_service_remove_files(uid, filename):
    directory = app.config['UPLOAD_FOLDER']+f"Printing/{uid}/"
    if fileExist(directory+filename):
        removeFile(directory+filename)

    return redirect(url_for('printing_service_files',uid=uid,msg='ok'))


@app.route('/PSITS@PrintingServiceAdmin', methods = ['GET', 'POST'])
def printing_service_admin():
    if 'username' not in session:
        save_redirection('printing_service_admin')
        return redirect(url_for('login_page'))
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))
    
    ACCOUNTS = os.listdir(app.config['UPLOAD_FOLDER']+f"Printing/")
    PENDING_ACCOUNTS = []
    for account in ACCOUNTS:
        if getNumberOfFiles(app.config['UPLOAD_FOLDER']+f"Printing/{account}/") > 0:
            PENDING_ACCOUNTS.append(account)
    # if is post
    if flask.request.method == 'POST':
        search = request.form['search']
        if search == '':
            return redirect(url_for('printing_service_admin'))
        return redirect(url_for('printing_service_files',uid=search,msg='ok'))
    return render_template("app_templates_1_2/PrintingRequestFiles.html", title='[ADMIN] Printing Service',account_data=Database.getAccountByID(session['username']), logout="block", login="none",uid=0, FILES=[], message='ok', admin=True,PENDING_ACCOUNTS=PENDING_ACCOUNTS)
