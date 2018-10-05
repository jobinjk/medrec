from medrec.extensions import db, pwd_context
from datetime import datetime, timedelta


class Users(db.Document):
    '''Mongodb Model for Users'''
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(max_length=255, required=True)
    created_on = db.DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

    def change_password(self, old, new):
        if self.check_password(old):
            self.set_password(new)
            return True
        else:
            return False

    meta = {
        'indexes': ['username', 'email', 'created_on'],
    }

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        return '(User : %s)' % self.username
