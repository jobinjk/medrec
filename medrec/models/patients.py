from medrec.extensions import db, pwd_context
from datetime import datetime, timedelta
from .users import Users


class Patients(db.Document):
    '''Mongodb Model for Patients'''

    name = db.StringField(required=True)
    description = db.StringField(required=True)
    medication = db.ListField(required=True)
    added_by = db.ReferenceField(Users)
    created_on = db.DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': ['created_on']
    }
