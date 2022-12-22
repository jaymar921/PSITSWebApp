from __main__ import app
from flask import render_template, session, redirect, url_for, request
from Database import getAccountByID
from Util import isAdmin
from webApp_utility import save_redirection, checkImageExist, is_blocked_route


@app.route('/PSITS/Administration')
def psits_admin_page():
    save_redirection('landing_page')
    if 'username' not in session:
        return redirect(url_for('cant_find_link'))
    if not isAdmin(session['username']):
        return render_template("404Page.html", logout="none", login="none",
                                   message="Sorry but this page is only for authorized personnel")
    return render_template(
        "app_templates_1_4/AdminPage.html",
        title="PSITS ADMIN",
        login="none",
        logout="block",
        account=session['username'],
        admin="block",
        account_data=getAccountByID(session['username'])
    )