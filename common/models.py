from model.base import Model

class BaseMeta(object):
    db = "alertServer"

class Session(Model):
    class Meta(BaseMeta):
        collection = 'session'
    
    fields = [
        "session_token", "expired_by", "created_at", "user_id",
    ]

class User(Model):
    class Meta(BaseMeta):
        collection = "user"

    fields = [
        "username", "email", "name"
    ]