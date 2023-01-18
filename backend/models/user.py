from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime
from .appointments import AppointmentModel

class UserModel(BaseClass, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, fullname, email, password):
        now = datetime.now()
        self.registered_on = now.strftime("%Y-%m-%d %H:%M:%S")
        self.fullname = fullname
        self.email = email
        self.password = password
