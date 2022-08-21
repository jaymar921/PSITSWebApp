from flask import Flask, render_template, request, redirect, url_for, session
from Database import getAnnouncements, getAccount, getAccountByID, postAnnouncement, removeAnnouncement
from Util import hashData, isAdmin
import datetime

app = Flask(__name__)
app.secret_key = 'PSITS2022BYABEJAR'


@app.route("/PSITS")
def landing_page():
    if "username" in session:
        if isAdmin(session['username']):
            return render_template("Homepage.html", title="PSITS ANNOUNCEMENTS", ANNOUNCEMENTS=getAnnouncements(),
                               login="none", logout="block", account=session['username'], admin="block")
        else:
            return render_template("Homepage.html", title="PSITS ANNOUNCEMENTS", ANNOUNCEMENTS=getAnnouncements(),
                                   login="none", logout="block", account=session['username'], admin="none")
    return render_template("Homepage.html", title="PSITS ANNOUNCEMENTS", ANNOUNCEMENTS=getAnnouncements(), login="block",
                           logout="none", admin="none")


@app.route("/PSITS@Login")
def login_page():
    return render_template("Login.html", title="PSITS ANNOUNCEMENTS", ANNOUNCEMENTS=getAnnouncements(), login="none")


@app.route("/PSITS@announce", methods=['POST'])
def post_announcement():
    date_time = datetime.datetime.now()

    title: str = request.form['title']
    content: str = request.form['content']

    postAnnouncement(title, date_time.strftime("%Y-%m-%d"), content)

    return redirect(url_for("landing_page"))


@app.route("/announcement_removal/<uid>")
def remove_announcement(uid):
    removeAnnouncement(uid)
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
    return render_template("Login.html", title="PSITS ANNOUNCEMENTS", ANNOUNCEMENTS=getAnnouncements(),
                           login="none", logout="none", message=message)


@app.route("/PSITS@Logout")
def logout():
    session.clear()
    return redirect(url_for("landing_page"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
