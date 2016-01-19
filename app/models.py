"""
@dani.ruiz
"""
from werkzeug import generate_password_hash, check_password_hash
from app import db, app
import hashlib

class GIC_CFG_ROL(db.Model):
    """taula de rols"""
    __tablename__ = 'A_GIC_CFG_ROL'
    id_rol = db.Column(db.Integer, primary_key=True)
    nom_rol = db.Column(db.String(30))
    template = db.Column(db.String(50))
    actiu = db.Column(db.String(1))
    rols = db.relationship('GIC_ROL', backref='GIC_ROL.id_rol', \
    primaryjoin='GIC_CFG_ROL.id_rol==GIC_ROL.id_rol', lazy='dynamic')
    def __init__(self, nom_rol, template, actiu):
        self.nom_rol = nom_rol
        self.template = template
        self.actiu = actiu

class GIC_CFG_GRUP(db.Model):
    """taula de grups de permisos"""
    __tablename__ = 'A_GIC_CFG_GRUP'
    id_grup = db.Column(db.Integer, primary_key=True)
    nom_grup = db.Column(db.String(40))
    actiu = db.Column(db.String(1))
    grups = db.relationship('GIC_CFG_PERMIS', backref='GIC_CFG_PERMIS.grup', \
    primaryjoin='GIC_CFG_GRUP.id_grup==GIC_CFG_PERMIS.grup', lazy='dynamic')
    def __init__(self, nom_grup, actiu):
        self.nom_grup = nom_grup
        self.actiu = actiu

class GIC_CFG_PERMIS(db.Model):
    """taula de permisos"""
    __tablename__ = 'A_GIC_CFG_PERMIS'
    id_permis = db.Column(db.Integer, primary_key=True)
    nom_permis = db.Column(db.String(40))
    actiu = db.Column(db.String(1))
    grup = db.Column(db.Integer, db.ForeignKey(GIC_CFG_GRUP.id_grup))
    grupr = db.relationship('GIC_CFG_GRUP', foreign_keys='GIC_CFG_PERMIS.grup')
    permisos = db.relationship('GIC_PERMIS', backref='GIC_PERMIS.id_permis', \
    primaryjoin='GIC_CFG_PERMIS.id_permis==GIC_PERMIS.id_permis', lazy='dynamic')
    def __init__(self, nom_permis, actiu, grup):
        self.nom_permis = nom_permis
        self.actiu = actiu
        self.grup = grup

class Post(db.Model):
    """taula de persones"""
    __tablename__ = 'A_GIC_PERSONA'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    cognom1 = db.Column(db.String(50))
    cognom2 = db.Column(db.String(50))
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
    pwdhash = db.Column(db.String(200))
    def __init__(self, nom, cognom1, cognom2, sexe, dni, passport, data_naix, \
    telefon1, telefon2, email1, email2, actiu, foto, password):
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
        self.set_password(password)
    def set_password(self, password):
#        self.pwdhash = generate_password_hash(password)
        self.pwdhash = hashlib.sha256('[B@3f13a310' + password).hexdigest()
    def check_password(self, password):
#        return check_password_hash(self.pwdhash, password)
        if self.pwdhash == hashlib.sha256('[B@3f13a310' + password).hexdigest():
            return True
        else:
            return False

class User(db.Model):
    """taula d'usuaris administradors"""
#    __tablename__ = 'users'
    __tablename__ = 'A_GIC_ADMIN'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20))
    cognom = db.Column(db.String(20))
    email = db.Column(db.String(40), unique=True)
    pwdhash = db.Column(db.String(200))
    def __init__(self, nom, cognom, email, password):
        self.nom = nom.title()
        self.cognom = cognom.title()
        self.email = email.lower()
        self.set_password(password)
    def set_password(self, password):
#        self.pwdhash = generate_password_hash(password)
	self.pwdhash = hashlib.sha256('[B@3f13a310' + password).hexdigest()
    def check_password(self, password):
#        return check_password_hash(self.pwdhash, password)
        if self.pwdhash == hashlib.sha256('[B@3f13a310' + password).hexdigest():
            return True
        else:
            return False


class GIC_PERMIS(db.Model):
    """taula que relaciona permisos amb persones"""
    __tablename__ = 'A_GIC_PERMIS'
    id_persona = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
    id_permis = db.Column(db.Integer, db.ForeignKey(GIC_CFG_PERMIS.id_permis), primary_key=True)
    inici = db.Column(db.Date)
    fi = db.Column(db.Date)
    persona = db.relationship('Post', foreign_keys='GIC_PERMIS.id_persona')
    rol = db.relationship('GIC_CFG_PERMIS', foreign_keys='GIC_PERMIS.id_permis')
    def __init__(self, id_persona, id_permis, inici, fi):
        self.id_persona = id_persona
        self.id_permis = id_permis
        self.inici = inici
        self.fi = fi

class GIC_ROL(db.Model):
    """taula que relaciona rols amb persones"""
    __tablename__ = 'A_GIC_ROL'
    id_persona = db.Column(db.Integer, db.ForeignKey(Post.id), primary_key=True)
    id_rol = db.Column(db.Integer, db.ForeignKey(GIC_CFG_ROL.id_rol), primary_key=True)
    inici = db.Column(db.Date)
    fi = db.Column(db.Date)
    persona = db.relationship('Post', foreign_keys='GIC_ROL.id_persona')
    rol = db.relationship('GIC_CFG_ROL', foreign_keys='GIC_ROL.id_rol')
    def __init__(self, id_persona, id_rol, inici, fi):
        self.id_persona = id_persona
        self.id_rol = id_rol
        self.inici = inici
        self.fi = fi
