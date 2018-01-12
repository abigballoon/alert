import random
import hashlib
import datetime

from common.models import Session

CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQUSRUVWXYZ0123456789!?#$%^*()-=_+'
SESSION_LIFE = datetime.timedelta(days=7)

def r(bit=2048):
    s = ''
    for _ in range(bit):
        s += random.choice(CHARACTERS)
    return hashlib.md5(s).hexdigest()

def login(user, session_token):
    userid = user.id
    try:
        session = Session.get(session_token=session_token)
    except Session.DoesNotExist:
        return
    session.user_id = userid
    session.save()

def logout(session_token):
    sessions = Session.get(session_token=session_token)
    sessions.user_id = None

