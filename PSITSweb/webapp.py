import random

import flask
from flask import Flask, render_template, request, redirect, url_for, session
from Database import getAnnouncements, getAccount, getAccountByID, postAnnouncement, removeAnnouncement, getEvents, \
    addEvent, removeEvent, registerAccountDB
from PSITSweb.Models import Events, Account
from Util import hashData, isAdmin
import datetime

app = Flask(__name__)
app.secret_key = 'PSITS2022BYABEJAR'


@app.route("/PSITS")
def landing_page():
    events: list = getEvents()
    if "username" in session:
        if isAdmin(session['username']):
            return render_template("Homepage.html",
                                   title="PSITS ANNOUNCEMENTS",
                                   ANNOUNCEMENTS=getAnnouncements(),
                                   login="none",
                                   logout="block",
                                   account=session['username'],
                                   admin="block",
                                   events=events)
        else:
            return render_template("Homepage.html",
                                   title="PSITS ANNOUNCEMENTS",
                                   ANNOUNCEMENTS=getAnnouncements(),
                                   login="none", logout="block",
                                   account=session['username'],
                                   admin="none",
                                   events=events)
    return render_template("Homepage.html",
                           title="PSITS ANNOUNCEMENTS",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="block",
                           logout="none", admin="none", events=events)


@app.route("/PSITS@Login")
def login_page():
    return render_template("Login.html",
                           title="PSITS ANNOUNCEMENTS",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="none",
                           logout="none")


@app.route("/PSITS@announce", methods=['POST'])
def post_announcement():
    date_time = datetime.datetime.now()

    title: str = request.form['title']
    content: str = request.form['content']

    if "username" in session:
        if isAdmin(session['username']):
            postAnnouncement(title, date_time.strftime("%Y-%m-%d"), content)
        else:
            return render_template("404Page.html", logout="none", login="none", message="Don't try to break the page :<")

    return redirect(url_for("landing_page"))


@app.route("/announcement_removal/<uid>")
def remove_announcement(uid):
    if "username" in session:
        if isAdmin(session['username']):
            removeAnnouncement(uid)
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))


@app.route("/PSITSLogin", methods=['POST'])
def login():
    account_id: str = request.form['id_number']
    password: str = request.form['password']
    account = getAccount(account_id, hashData(password))
    if account.uid is not None:
        session['username'] = account.uid
        return redirect(url_for("landing_page"))

    account = getAccountByID(account_id)
    message = "Account not found!"
    if account.uid is not None:
        message = "Invalid password"
    return render_template("Login.html",
                           title="Login PSITS",
                           ANNOUNCEMENTS=getAnnouncements(),
                           login="none",
                           logout="none",
                           message=message)


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
        password = hashData(request.form['password'])
        account = Account(
            idno,
            rfid,
            firstname,
            lastname,
            course,
            year
        )
        registerAccountDB(account, password)
        return redirect(url_for("login_page"))


@app.route("/PSITS@NewEvent", methods=['GET', 'POST'])
def EventHandlerPSITS():
    if flask.request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('cant_find_link'))
        account = session['username']
        if isAdmin(account):
            return render_template("EventForm.html", login='none', logout='block', account=account)
        else:
            return redirect(url_for('cant_find_link'))
    else:
        event_id = random.randint(100, 99999)
        event_title = request.form['Title']
        event_date = request.form['date_held']
        event_info = request.form['Information']
        event_reqP = request.form.get('require_payment')
        event_item = request.form['Item']
        event_amt = request.form['Amount']

        if event_amt == '' or event_amt is None:
            event_amt = 0
        if event_reqP is None:
            event_reqP = 'NO'
        event = Events(
            uid=event_id,
            title=event_title,
            date_held=event_date,
            info=event_info,
            required_payment=event_reqP,
            item=event_item,
            amount=event_amt
        )
        addEvent(event)
        return redirect(url_for("landing_page"))


@app.route("/event_removal/<uid>")
def removeEventPage(uid):
    if "username" in session:
        if isAdmin(session['username']):
            removeEvent(uid)
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))


@app.route("/PSITS@Logout")
def logout():
    session.clear()
    return redirect(url_for("landing_page"))


@app.route("/CannotFindLink")
def cant_find_link():
    return render_template("404Page.html", logout="none", login="none")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404Page.html", logout="none", login="none"), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
