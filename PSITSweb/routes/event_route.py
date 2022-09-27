import os
from __main__ import app

import flask
from flask import session, redirect, url_for, render_template, request

from PSITSWebApp.PSITSweb.Database import CREATEEvent, databaseLog, SEARCHEvent, UPDATEEvent, getAccountByID, \
    removeEvent, DELETEEvent
from PSITSWebApp.PSITSweb.Models import Event
from PSITSWebApp.PSITSweb.Util import isAdmin, contentVerifier
from PSITSWebApp.PSITSweb.webapp import ALLOWED_EXTENSION


@app.route("/PSITS@NewEvent", methods=['GET', 'POST'])
def EventHandlerPSITS():
    if flask.request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('cant_find_link'))
        account = session['username']
        if isAdmin(account):
            return render_template("NewEventForm.html", login='none', logout='block', account=account, account_data=getAccountByID(account))
        else:
            return redirect(url_for('cant_find_link'))
    else:
        event_title = contentVerifier(request.form["Title"])
        event_date = request.form["date_held"]
        event_info = contentVerifier(request.form["Information"])
        event = Event(
            None,
            event_title,
            event_date,
            event_info,
            "-"
        )
        CREATEEvent(event)
        databaseLog(f"Event [{event.title}] added")
        event = SEARCHEvent(event_title)[0]
        if 'event_image' in request.files:
            file = request.files['event_image']
            if file is not None:
                if file.filename != '':
                    ext = file.filename.split(".")[1]
                    if ext in ALLOWED_EXTENSION:
                        file.filename = "event" + str(event.uid) + "." + ext
                        event.image_file = "event" + str(event.uid) + "." + ext
                        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(path)
                        file.close()
                        databaseLog(f"Event [{event.title}] comes with an image")
        UPDATEEvent(event)
        return redirect(url_for("landing_page"))

@app.route("/event_removal/<uid>")
def removeEventPage(uid):
    if "username" in session:
        if isAdmin(session['username']):
            removeEvent(uid)
            databaseLog(f"Removed Event ID [{uid}]")
        else:
            return render_template("404Page.html", logout="none", login="none",
                                   message="Don't try to break the page :<")
    return redirect(url_for("landing_page"))


@app.route("/PSITS@Events", methods=['POST', 'GET'])
def psits_events_list():
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))

    if request.method == 'GET':
        # Get the search
        search: str = flask.request.values.get('search')
        return render_template("EventList.html",
                               logout='block', login='none', account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS EVENTS LIST', events=SEARCHEvent(search))
    else:
        search: str = flask.request.values.get('search')
        event: Event = Event(
            request.form['idnum'],
            request.form['title'],
            request.form['date_published'],
            request.form['information'],
            request.form['image_file']
        )
        UPDATEEvent(event)
        # if request.form['open'] == 'YES':
        # Email Request
        #    orders: list = getOrder(event.uid, 'RESERVED')
        #    for order in orders:
        #        user_message = f"Hello {getAccountByID(order.account_uid).firstname}!\n\n" \
        #                       f"Our {event.title} is now available for an order! The {event.item} is " \
        #                       f"priced at P{event.amount}. Login to PSITS page to order now!"
        #        if getAccountByID(order.account_uid).email is not None or "":
        #            pushEmail(Email("PSITS - " + event.title, getAccountByID(order.account_uid).email, user_message))
        # updateEvent(event)
        databaseLog(f"Updated event ID [{event.uid}] by [{session['username']}] -- {event.title}")
        return render_template("EventList.html",
                               logout='block', login='none', account_data=getAccountByID(session['username']),
                               admin='block', title='PSITS EVENTS LIST', events=SEARCHEvent(search))


@app.route("/PSITS@EventRemove/<uid>")
def psits_remove_event(uid):
    if 'username' not in session:
        return render_template("404Page.html", logout="none", login="none",
                               message="Only administrators can access this page!")
    if not isAdmin(session['username']):
        return redirect(url_for('cant_find_link'))
    DELETEEvent(uid)
    databaseLog(f"Removed event ID [{uid}]")
    return redirect(url_for("psits_events_list"))
