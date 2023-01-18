from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class AppointmentModel(BaseClass, db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    message = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, fullname, email, message):
        now = datetime.now()
        self.timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        self.fullname = fullname
        self.email = email
        self.message = message
