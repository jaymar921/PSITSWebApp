from __main__ import app
import os

from flask import session

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