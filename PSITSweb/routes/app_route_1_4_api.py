from __main__ import app
import os

from flask import request, redirect, url_for, session, render_template
import json
import threading, time
import pandas as pd
import datetime


from Database import updateAnnouncement, SEARCHMerchOrder, SEARCHMerchandise, getAccountByID, UPDATEMerchOrder, getAccount, DELETEMerchOrder, updateAccount, databaseLog, GETAllMerchandise\
    ,getAllAccounts, getAccountWithPassword, GetAllPromo, getAnnouncement
# from EmailAPI import pushEmail
from Models import AccountOrders, MerchOrder, Merchandise, Account, ORDER_STATUS, AccountOrdersLW, Announcement
from Util import GetReference, isAdmin, ifKeyPermitted, hashData, GetPriceRef, contentVerifier
from webApp_utility import save_redirection, is_blocked_route, checkImageExist, renameFile


@app.route('/PSITS/api/announcement', methods=['PUT'])
def api_update_announcement():
    request_key = request.args.get('key')

    if not request_key:
        databaseLog(
            f'API[PUT] - Remote {request.remote_addr} - Tried to update announcement with no key')
        return {
            "status": 403,
            "message": "ACCESS DENIED: key must be provided at query string."
        }

    if not ifKeyPermitted(request_key):
        databaseLog(
            f'API[PUT] - Remote {request.remote_addr} - Tried to update announcement with invalid key')
        return {
            "status": 403,
            "message": f"ACCESS DENIED: invalid key -- {request_key}"
        }

    try:
        uid = request.get_json()['uid']
        title = request.get_json()['title']
        content = request.get_json()['content']
        user = request.get_json()['user']
        content = f"""{content.strip()} 

Updated by: {user} ({datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            """

        # Before we update the announcements, we should also link the images
        # from the old announcement title
        announcement_old: Announcement = getAnnouncement(uid)
        print(announcement_old.title)
        # Load the Photos if exist
        if checkImageExist(str(announcement_old.uid) + announcement_old.title + ".jpg"):
            renameFile(f"{str(announcement_old.uid) + announcement_old.title}.jpg", f"{str(announcement_old.uid) + title}.jpg")
        if checkImageExist(str(announcement_old.uid) + announcement_old.title + ".png"):
            renameFile(f"{str(announcement_old.uid) + announcement_old.title}.png", f"{str(announcement_old.uid) + title}.png")
        for num in range(1,100):
            if checkImageExist(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.png"):
                renameFile(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.png", f"{str(announcement_old.uid) + title + str(num)}.png")
        for num in range(1,100):
            if checkImageExist(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.jpg"):
                renameFile(f"{str(announcement_old.uid) + announcement_old.title + str(num)}.jpg", f"{str(announcement_old.uid) + title + str(num)}.jpg")
        updateAnnouncement(uid, title,datetime.datetime.now().strftime("%Y-%m-%d"),contentVerifier(content))
        databaseLog(f'API[PUT] - Remote {request.remote_addr} - Announcement [{title}] was updated by {user}')
    except Exception as e:
        print(e)
        return {
            "status": 500,
            "message": f"The server does not understand the request content provided"
        }
    
    response = app.response_class(
        response=json.dumps({"status":204}, indent=4,
                            sort_keys=False, default=str),
        status=200,
        mimetype='application/json'
    )
    return response