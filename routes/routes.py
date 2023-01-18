from tkinter.messagebox import NO
from backend.models import UserModel
from backend.models import AppointmentModel
from backend.models import ApplicantsModel
from flask_restx import Resource, abort
from flask import request, session
import jwt

import re
import datetime
import functools
from flask import make_response, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
import config
from time import gmtime, strftime
from db import db
from flask import current_app as app

from utils.dto import UserDto
from utils.dto import AuthDto
import json

api = UserDto.api
user = UserDto.user

def login_required(method):
    @functools.wraps(method)
    def wrapper(self):
        header = request.headers.get('Authorization')
        _, token = header.split()
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except jwt.DecodeError:
            return {'message':'Token is not valid.', 'status':400}
        except jwt.ExpiredSignatureError:
            return {'message':'Token is expired.', 'status': 400}
        email = decoded['email']
        if len(UserModel.query.filter_by(email = email).all()) == 0:
            return {'message':'User is not found.', 'status':400}
        user = UserModel.query.filter_by(email = email).all()[0]
        return method(self, user)
    return wrapper


@api.route('/register')
class Register(Resource):
    
    @api.doc('register a user')
    @api.expect(user, validate=True)
    def post(self):
        email = request.json['email']
        password = request.json['password']
        fullname = request.json['fullname']

        user = UserModel.query.filter_by(email = email).all()
        if not user:
            if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email):
                return {'message':'email is not valid.','status':400}
            if len(password) < 6:
                return {'message':'password is too short.','status':400}

            if len(UserModel.query.filter_by(email = email).all()) != 0:
                return {'message':'email is already used.', 'status':400}
            else:
                user = UserModel(email= email, password =generate_password_hash(password), fullname=fullname)
                db.session.add(user)
                db.session.commit()

            return {'email': email,'message':'user registered successfully','status':200}
        else:
            return {"message":"User already exists", "status":400}


api2 = AuthDto.api
auth = AuthDto.auth

@api.route('/login')
class Login(Resource):
    @api.doc('Login a user')
    @api.expect(auth, validate=True)
    def post(self):
        email = request.json['email']
        password = request.json['password']
        
        user = UserModel.query.filter_by(email = email).first()
        if user:
            if not check_password_hash(user.password, password):
                return {'message':'Password is incorrect.', 'status':400}

            exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
            encoded = jwt.encode({'email': email,'userid':user.id, 'exp': exp}, app.config['SECRET_KEY'], algorithm='HS256')

            # if email == 'admin@gmail.com':
            #     return { 'message': 'admin logged in successfully', 'email': email, 'token': encoded,'status':200 }

            return { 'message':'successful login', 'email': email, 'token': encoded,'status':200}
        else:
            return {"message":"Unauthorized user", "status":400}

# get user details and update
@api.route('/employee/details')
class UserDetails(Resource):
    @login_required
    def get(self, user):
        user = UserModel.query.filter_by(id=user.id).all()
        print(user)
        if user is None:
            return {"message":"user not authorized"}, 400
        else:
            cols = ['firstname', 'lastname', 'username', 'email']
            
            result = [{col: getattr(d, col) for col in cols} for d in user]
            
            return jsonify(data=result)

# Make appointments
# completed
@api.route('/make/appointment')
class AddPosts(Resource):
    def post(self):
        fullname = request.json['fullname']
        email = request.json['email']
        message = request.json['message']

        print(fullname, email, message)
        record = AppointmentModel(fullname=fullname, email=email, message=message)
        
        db.session.add(record) 
        db.session.commit() 
    
        return {"message":"Message sent successfully"}, 200

# all employees
# complete
@api.route('/all/employees')
class Employees(Resource):
    # @login_required
    def get(self):
        data = db.session.query(UserModel).all()
        
        if data is None:
            return {'message':'No employees'} 

        else:
            cols = ['id', 'fullname', 'email']
            
            result = [{col: getattr(d, col) for col in cols} for d in data]
            
            return jsonify(data=result)

# all appointments
# complete
@api.route('/all/appointments')
class Appointments(Resource):
    # @login_required
    def get(self):
        data = db.session.query(AppointmentModel).all()
        
        if data is None:
            return {'message':'No appointments'} 

        else:
            cols = ['id', 'fullname', 'email', 'message']
            
            result = [{col: getattr(d, col) for col in cols} for d in data]
            
            return jsonify(data=result)

@api.route('/job/application')
class AddApplication(Resource):
    def post(self):
        fullname = request.json['fullname']
        email = request.json['email']
        jobtype = request.json['jobtype']
        resume = request.files['file']


        print(fullname, email, jobtype)
        record = ApplicantsModel(fullname=fullname, email=email, jobtype=jobtype, resume=resume)
        
        db.session.add(record) 
        db.session.commit() 
    
        return {"message":"Application sent successfully"}, 200 
