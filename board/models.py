from model.base import Model
from common.models import BaseMeta

class Board(Model):
    class Meta(BaseMeta):
        collection = 'board'

    fields = [
        "name", "message_ids", "users"
    ]


class Token(Model):
    class Meta(BaseMeta):
        collection = 'token'
    
    fields = [
        "token", "user_id", "borad_id"
    ]