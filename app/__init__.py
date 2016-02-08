import os
from flask import Flask, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from itsdangerous import URLSafeTimedSerializer

#Create an Instance of Flask
app = Flask(__name__)
#Include config from config.py


app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'app/static/img/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'csv'])
app.config['WTF_CSRF_SECRET_KEY'] = '1234'
app.config["MAIL_SERVER"] = "mail.car.loc"
app.config["MAIL_PORT"] = 25
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = None
app.config["MAIL_PASSWORD"] = None
app.secret_key = "1234"
app.config["SECURITY_PASSWORD_SALT"] = '1234'
app.config["POSTS_PER_PAGE"] = 10

#Create an instance of SQLAclhemy
db = SQLAlchemy(app)

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#class MyResponse(Response):
#     default_mimetype = 'application/xml'

#app.response_class = MyResponse

from app import models, forms, token

from app.views import add, editar, index, signup, cercar, esborrar, upload, perfil, signin, signout, f_password, add_ge_car, json, editar_gecar

# Blueprints   
from app.views.json import users
app.register_blueprint(users, url_prefix='/persones')
