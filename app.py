import os
from flask import Flask, flash, request, redirect, send_file, session, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from cmath import log
from flask import Flask
from db import db, mail
from config import DevelopmentConfig
from flask_cors import CORS 
from flask_jwt_extended import JWTManager

from backend.models import UserModel
from backend.models import AppointmentModel

from flask_restx import Api,fields
from routes.routes import api as usersReg
from routes.routes import api2 as authUser

from routes.routes import Register, Login, login_required
from flask import request

from utils.dto import UserDto

import boto3
from flask import Flask, render_template, request, redirect, send_file
# from s3_functions import list_files, upload_file, show_image
from werkzeug.utils import secure_filename

user = UserDto.user

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

CORS(app)

api = Api(app, version = "1.0", 
		  title = "Beauty Parlor", 
		  description = "Admin panel",
          doc="/docs")

# adding the namespaces
api.add_namespace(usersReg, path='/api')
api.add_namespace(authUser)

s3 = boto3.client('s3',
                    aws_access_key_id='AKIARKSJ3WF3JY6MCM6Q',
                    aws_secret_access_key= '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',
                    region_name='us-west-2'
                     )
BUCKET = "washwashbucket"

# def show_image(bucket):
#     s3_client = boto3.client('s3')
#     public_urls = []
#     try:
#         for item in s3_client.list_objects(Bucket=bucket)['Contents']:
#             presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
#             public_urls.append(presigned_url)
#     except Exception as e:
#         pass
#     return public_urls

def show_image():
    response = s3.list_objects_v2(
    Bucket= BUCKET,
    Prefix='applicationCVs/'
    )
    public_urls = []
    for content in response.get('Contents', []):
        print(content['Key'])
        presigned_url = s3.generate_presigned_url('get_object', Params = {'Bucket': BUCKET, 'Key': content['Key'], 'ResponseContentType': 'application/pdf'},  ExpiresIn = 72000)
        public_urls.append(presigned_url)

    return public_urls
    # print(public_urls)

def show_hair():
    response = s3.list_objects_v2(
    Bucket= BUCKET,
    Prefix='TrendingHairStyles/'
    )
    public_urls = []
    for content in response.get('Contents', []):
        print(content['Key'])
        presigned_url = s3.generate_presigned_url('get_object', Params = {'Bucket': BUCKET, 'Key': content['Key'], 'ResponseContentType': 'image/png'},  ExpiresIn = 72000)
        public_urls.append(presigned_url)

    return public_urls

def show_manicure():
    response = s3.list_objects_v2(
    Bucket= BUCKET,
    Prefix='Manicure/'
    )
    public_urls = []
    for content in response.get('Contents', []):
        print(content['Key'])
        presigned_url = s3.generate_presigned_url('get_object', Params = {'Bucket': BUCKET, 'Key': content['Key'], 'ResponseContentType': 'image/png'},  ExpiresIn = 72000)
        public_urls.append(presigned_url)

    return public_urls

def show_pedicure():
    response = s3.list_objects_v2(
    Bucket= BUCKET,
    Prefix='pedicure/'
    )
    public_urls = []
    for content in response.get('Contents', []):
        print(content['Key'])
        presigned_url = s3.generate_presigned_url('get_object', Params = {'Bucket': BUCKET, 'Key': content['Key'], 'ResponseContentType': 'image/png'},  ExpiresIn = 72000)
        public_urls.append(presigned_url)

    return public_urls


@app.route("/files")
def list():
    contents = show_image()
    return { "message":"success", "data":contents }

@app.route("/trending/hair")
def list_hair():
    contents = show_hair()
    return { "message":"success", "data":contents }

@app.route("/manicure")
def list_manicure():
    contents = show_manicure()
    return { "message":"success", "data":contents }

@app.route("/pedicure")
def list_pedicure():
    contents = show_pedicure()
    return { "message":"success", "data":contents }

def upload_file(file_name, bucket):
    object_name = file_name
    # s3_client = boto3.client(s3)
    response = s3.upload_file(file_name, bucket, object_name)
    return response

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        UPLOAD_FOLDER = 'applicationCVs'

        img = request.files['file']
        print("working========")
        img.save(os.path.join(UPLOAD_FOLDER, secure_filename(img.filename)))
        print("works-------")
        upload_file(f"applicationCVs/{img.filename}", BUCKET)
                
        return { "message": "successfully uploaded cv"}

@app.route("/upload/trending/hairstyles", methods=['POST'])
def upload_trending_style():
    if request.method == "POST":
        UPLOAD_FOLDER = 'TrendingHairStyles'

        img = request.files['file']
        print("working========")
        img.save(os.path.join(UPLOAD_FOLDER, secure_filename(img.filename)))
        upload_file(f"TrendingHairStyles/{img.filename}", BUCKET)
                
        return { "message": "successfully uploaded trending hair style"}

@app.route("/upload/sample/manicure", methods=['POST'])
def upload_sample_manicure():
    if request.method == "POST":
        UPLOAD_FOLDER = 'Manicure'

        img = request.files['file']
        print("working========")
        img.save(os.path.join(UPLOAD_FOLDER, secure_filename(img.filename)))
        upload_file(f"Manicure/{img.filename}", BUCKET)
                
        return { "message": "successfully uploaded manicure works"}

@app.route("/upload/sample/pedicure", methods=['POST'])
def upload_sample_pedicure():
    if request.method == "POST":
        UPLOAD_FOLDER = 'Pedicure'

        img = request.files['file']
        print("working========")
        img.save(os.path.join(UPLOAD_FOLDER, secure_filename(img.filename)))
        upload_file(f"pedicure/{img.filename}", BUCKET)
                
        return { "message": "successfully uploaded pedicure works"}

if __name__ == '__main__':    
    app.run()
