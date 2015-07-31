import ldap
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from app import db, app
class GIC_CFG_ROL(db.Model):
	id_rol = db.Column(db.Integer,primary_key=True)
	nom_rol = db.Column(db.String(30))
	template = db.Column(db.String(50))
	rols = db.relationship('GIC_ROL', backref='GIC_ROL.id_rol',primaryjoin='GIC_CFG_ROL.id_rol==GIC_ROL.id_rol', lazy='dynamic')	
	def __init__(self,nom_rol,template):
		self.nom_rol = nom_rol
		self.template = template
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nom = db.Column(db.String(50))
	cognom1	= db.Column(db.String(50))
	cognom2	= db.Column(db.String(50))
	sexe = db.Column(db.String(1))
	dni = db.Column(db.String(50))
	passport = db.Column(db.String(50))
	data_naix = db.Column(db.String(50))
	telefon1 = db.Column(db.String(50))
	telefon2 = db.Column(db.String(50))
	email1 = db.Column(db.String(50))
	email2 = db.Column(db.String(50))
	actiu = db.Column(db.String(1))
	foto = db.Column(db.String(50))
#	password = db.Column(db.String(50))
	def __init__(self, nom, cognom1,cognom2,sexe,dni,passport,data_naix,telefon1,telefon2,email1,email2,actiu,foto):#,password):
		self.nom = nom
		self.cognom1 = cognom1
		self.cognom2 = cognom2
		self.sexe = sexe
		self.dni = dni
		self.passport = passport
		self.data_naix = data_naix
		self.telefon1 = telefon1
		self.telefon2 = telefon2
		self.email1 = email1
		self.email2 = email2
		self.actiu = actiu
		self.foto = foto
#		self.password = password

class GIC_ROL(db.Model):
	id_persona = db.Column(db.Integer,db.ForeignKey(Post.id),primary_key=True)
	id_rol = db.Column(db.Integer,db.ForeignKey(GIC_CFG_ROL.id_rol),primary_key=True)
	inici = db.Column(db.Date)
	fi = db.Column(db.Date)

	persona = db.relationship('Post', foreign_keys='GIC_ROL.id_persona')
	rol = db.relationship('GIC_CFG_ROL', foreign_keys='GIC_ROL.id_rol')


def get_ldap_connection():
	conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
	print conn
	return conn
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100))
	def __init__(self,username,password):
		self.username = username
	@staticmethod
	def try_login(username,password):
		conn=get_ldap_connection()
		conn.simple_bind_s('cn=%s,dc=dc1,dc=carsc,dc=loc' %username,password)
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymous(self):
		return False
	def get_id(self):
		return unicode(self.id)

class LoginForm(Form):
	username = TextField('Username', [InputRequired()])
	password = PasswordField('Password', [InputRequired()])
