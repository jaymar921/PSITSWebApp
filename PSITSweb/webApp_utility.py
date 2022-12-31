from __main__ import app
import os, json, datetime as dt

from flask import session

ROUTES_CONTROLLER: list = []

def has_redirection() -> bool:
    if 'redirect' in session:
        if session['redirect'] != '':
            return True
    return False


def save_redirection(url: str, *args):
    session['redirect'] = url
    for ar in args:
        session['redirect_extra'] = ar


def get_redirection() -> str:
    url = session['redirect']
    session['redirect'] = ''
    return str(url)


def get_redirection_extra():
    if 'redirect_extra' in session:
        return session['redirect_extra']
    return ''

def checkImageExist(name: str):
    return os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], name))

def renameFile(origin, newname):
    os.rename(os.path.join(app.config['UPLOAD_FOLDER'], origin),os.path.join(app.config['UPLOAD_FOLDER'], newname)) 


def block_route(route):
    ROUTES_CONTROLLER.append(route)


def is_blocked_route(route):
    return route in ROUTES_CONTROLLER


def unblock_route(route):
    if is_blocked_route(route):
        ROUTES_CONTROLLER.remove(route)

def saveToFile(filename, data):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w') as file:
        file.write(data)

def loadFromFile(filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as file:
        lines = file.readlines()
    outputStr = ''
    for line in lines:
        outputStr = outputStr + line
    return outputStr

def loadJSONFromFile(filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as file:
        lines = file.readlines()
    outputStr = ''
    for line in lines:
        outputStr = outputStr + line
    return json.loads(outputStr)

def deleteFile(filename):
    if os.path.exists(filename):
        os.remove(filename)

def getListOfFiles(directory):
    return os.listdir(directory)

def getFileDaysFromModified(filename):
    file_date = dt.datetime.fromtimestamp(os.path.getmtime(filename))
    if not file_date:
        file_date = dt.datetime.fromtimestamp(os.path.getctime(filename))
    d0 = dt.date(file_date.year, file_date.month, file_date.day)
    d1 = dt.datetime.now().date()
    d1 = dt.date(d1.year, d1.month, d1.day)
    delta = d1-d0
    return delta.days

#   print(loadJSONFromFile(app.config['UPLOAD_FOLDER']+f"Quiz\\Quiz_C.json"))
#   print(getListOfFiles(app.config['UPLOAD_FOLDER']+'Quiz\\'))