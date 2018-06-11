# conding: encoding=utf-8
import time
from datetime import datetime

from app.foundation import db


class EnrolInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(32))
    id_number = db.Column(db.String(18))
    gender = db.Column(db.String(12))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(
        db.Integer, default=time.time, onupdate=time.time)
