import sys
from etc.conf import BASE_DIR
sys.path.insert(0, BASE_DIR)

from common.models import Session

s = Session.get(session_token="haha")