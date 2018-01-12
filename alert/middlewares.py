from flask import request

from alert.app import app

from common.models import Session, User
from common.utils import r
from common.log import logging

@app.before_request
def pre_request():
    funcs = [
        SessionBaseAuthenication,
        UnAuthorized
    ]
    for func in funcs:
        func()

def SessionBaseAuthenication():
    session = request.cookies.get('session', '')
    if session:
        session_info = Session.get(session_token=session)
        logging.info(session_info.toDict())
        userid = session_info.user_id
        if userid:
            user = User.get(id=userid)
            request.user = user

def UnAuthorized():
    if not hasattr(request, 'user'):
        request.user = None

@app.after_request
def post_request(response):
    funcs = [
        SetSession,
    ]
    for func in funcs:
        response = func(response)
    return response

def SetSession(response):
    session = request.cookies.get('session', '')
    if not session:
        session = r()
        Session.create(session_token=session)
        response.set_cookie('session', session)
    return response