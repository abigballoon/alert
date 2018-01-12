import sys
from etc.conf import BASE_DIR
sys.path.insert(0, BASE_DIR)

from common.models import User, Session

u = User.get()

sessions = Session.filter()

for session in sessions.result:
    session.user_id = u.pk
    session.save()
