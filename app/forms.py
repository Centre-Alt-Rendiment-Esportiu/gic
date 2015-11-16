# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User, Post

class SignupForm(Form):
    nom = StringField("Nom", [validators.Required("Escriu el teu nom.")])
    cognom = StringField("Cognom", [validators.Required("Escriu el teu cognom.")])
    email = StringField("Email", [validators.Required("Escriu el teu correu electronic."), validators.Email("Escriu el teu correu electronic.")])
    password = PasswordField('Password', [validators.Required("Escriu un password.")])
    submit = SubmitField("Crear compte")
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("Correu ja utilitzat")
            return False
        else:
            return True
    
class SigninForm(Form):
    email = StringField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        elif not user:
            self.email.errors.append("Invalid e-mail")
            return False
        elif user and not user.check_password(self.password.data):
            self.email.errors.append("Invalid password")
            return False
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False
            
class Inici_Clients_Form(Form):
    email = StringField("Email", [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        user = Post.query.filter_by(email1 = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        elif not user:
            self.email.errors.append("Invalid e-mail")
            return False
        elif user and not user.check_password(self.password.data):
            self.email.errors.append("Invalid password")
            return False
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False

class emailForm(Form):
    email = StringField("Correu", [validators.Required("Entra una adreça de correu."), validators.Email("Entra una adreça de correu.")])
    submit = SubmitField("Envia")
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        user = Post.query.filter_by(email1 = self.email.data.lower()).first()
        if user:
            return True
        elif not user:
            self.email.errors.append("Invalid e-mail")
            return False

class email_adminForm(Form):
    email = StringField("Correu", [validators.Required("Entra una adreça de correu."), validators.Email("Entra una adreça de correu.")])
    submit = SubmitField("Envia")
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            return True
        elif not user:
            self.email.errors.append("Invalid e-mail")
            return False

class ContactForm(Form):
    name = StringField("Name",  [validators.Required("Please enter your name.")])
    email = StringField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = StringField("Subject",  [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")
    
