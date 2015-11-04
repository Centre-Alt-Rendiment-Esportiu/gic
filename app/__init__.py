import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask.ext.login import LoginManager
from werkzeug import secure_filename
from flask.ext.mail import Message, Mail

mail = Mail()

#Create an Instance of Flask
app = Flask(__name__)
#Include config from config.py
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'app/static/img/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['WTF_CSRF_SECRET_KEY'] = '1234'
app.config['LDAP_PROVIDER_URL'] = 'ldap://dc1.carsc.loc:389/'
app.config['LDAP_PROTOCOL_VERSION'] = 3
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'daniel.ruiz@car.edu'
app.config["MAIL_PASSWORD"] = 'davemackintosh6'

app.secret_key = '1234'
#Create an instance of SQLAclhemy
db = SQLAlchemy(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import models,forms

from app.views import add, editar, index, signup, cercar, esborrar, upload, contact, perfil, signin, signout
