from __main__ import app
import os

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