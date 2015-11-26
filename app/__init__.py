import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from itsdangerous import URLSafeTimedSerializer

#Create an Instance of Flask
app = Flask(__name__)
#Include config from config.py

app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'app/static/img/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
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

from app import models, forms, token

from app.views import add, editar, index, signup, cercar, esborrar, upload, perfil, signin, signout, f_password
