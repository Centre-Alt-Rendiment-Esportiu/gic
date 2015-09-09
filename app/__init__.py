import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask.ext.login import LoginManager
from werkzeug import secure_filename

#Create an Instance of Flask
app = Flask(__name__)
#Include config from config.py
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'app/static/img/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['WTF_CSRF_SECRET_KEY'] = '1234'
app.config['LDAP_PROVIDER_URL'] = 'ldap://dc1.carsc.loc:389/'
app.config['LDAP_PROTOCOL_VERSION'] = 3

app.secret_key = '1234'
#Create an instance of SQLAclhemy
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models
from app.views import auth
app.register_blueprint(auth)

