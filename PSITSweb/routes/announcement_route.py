
import os
from __main__ import app
import datetime

from flask import request, session, render_template, redirect, url_for

from Database import getLatestAnnouncement, postAnnouncement, databaseLog, removeAnnouncement, getAccountByID
from Util import contentVerifier, isAdmin
from Models import Account
from webapp import ALLOWED_EXTENSION


@app.route("/PSITS@announce", methods=['POST'])
def post_announcement():
    date_time = datetime.datetime.now()

    title: str = contentVerifier(request.form['title'])
    content: str = request.form['content']

    

    if "username" in session:
        if isAdmin(session['username']):
            account: Account = getAccountByID(session['username'])
            content = f"""
                {content}

                Posted by: {account.firstname} {account.lastname} ({datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            """

            postAnnouncement(title, date_time.strftime("%Y-%m-%d"), contentVerifier(content))
            ID = getLatestAnnouncement()
            databaseLog(f"Account ID [{session['username']}] posted an announcement [{title}]")
            if 'file' in request.files:
                file = request.files['file']
                if file is not None:
                    if file.filename != '':
                        ext = file.filename.split(".")[1]
                        if ext in ALLOWED_EXTENSION:
                            file.filename = str(ID) + title + "." + ext
                            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                            file.save(path)
                            file.close()
                            databaseLog(f"Announcement [{title}] comes with an image")
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")

    return redirect(url_for("landing_page"))


@app.route("/announcement_removal/<uid>")
def remove_announcement(uid):
    if "username" in session:
        if isAdmin(session['username']):
            removeAnnouncement(uid)
            databaseLog(f"Removed announcement [{uid}]")
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))
