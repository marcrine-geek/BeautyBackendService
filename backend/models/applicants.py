from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class ApplicantsModel(BaseClass, db.Model):
    __tablename__ = "applicants"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    jobtype = db.Column(db.String(255))
    resume = db.Column(db.LargeBinary(length=(2**32)-1))
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, fullname, email, jobtype, resume):
        now = datetime.now()
        self.timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        self.fullname = fullname
        self.email = email
        self.jobtype = jobtype
        self.resume = resume
