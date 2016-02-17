"""
@dani.ruiz
"""
from werkzeug import generate_password_hash, check_password_hash
from app import db, app
import hashlib

from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

################## API JSON #############################

class CRUD():   
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()
    def update(self):
        return db.session.commit()
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()
        
class UsersSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)  
    nom = fields.String(validate=not_blank)
    cognom1 = fields.String(validate=not_blank)
    cognom2 = fields.String()
    sexe = fields.String(validate=not_blank)
    dni = fields.String(validate=not_blank)
    passport = fields.String()
    data_naix = fields.String(validate=not_blank)
    telefon1 = fields.String(validate=not_blank)
    telefon2 = fields.String()
    email1 = fields.String(validate=not_blank)
    email2 = fields.String()
    actiu = fields.String(validate=not_blank)
    foto = fields.String()
    pwdhash = fields.String()

     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}
    class Meta:
        type_ = 'users'
####################################################################

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

class Post(db.Model, CRUD):
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
    
class A_GE_CAR_PERSONA(db.Model,CRUD):
    """taula ge car"""
    __tablename__ = 'A_GE_CAR_PERSONA'
    identificador = db.Column(db.String(20), primary_key=True)
    foto = db.Column(db.String(30))
    dni = db.Column(db.String(9))
    passaport = db.Column(db.String(20))
    nom = db.Column(db.String(20))
    cognom1 = db.Column(db.String(20))
    cognom2 = db.Column(db.String(20))
    sexe = db.Column(db.Integer)
    ss = db.Column(db.String(20))
    tipus = db.Column(db.Integer)
    data_neix = db.Column(db.Date)
    lloc_neix = db.Column(db.String(30))
    provincia_neix = db.Column(db.Integer)
    comarca_neix = db.Column(db.Integer)
    auto_neix = db.Column(db.Integer)
    pais_neix = db.Column(db.Integer)
    direccio = db.Column(db.String(40))
    poblacio = db.Column(db.String(30))
    provincia = db.Column(db.Integer)
    cp = db.Column(db.String(15))
    comarca = db.Column(db.Integer)
    autonomia = db.Column(db.Integer)
    pais = db.Column(db.Integer)
    telefon1 = db.Column(db.String(20))
    telefon2 = db.Column(db.String(20))
    e_mail = db.Column(db.String(52))
    estudis_act = db.Column(db.String(30))
    nivel_academic = db.Column(db.Integer)
    tipus_centre = db.Column(db.Integer)
    nom_centre = db.Column(db.String(50))
    aceptacio = db.Column(db.Integer)
    revisiom = db.Column(db.Integer)
    revisiops = db.Column(db.Integer)
    fitxacomplerta = db.Column(db.Integer)
    vehicle = db.Column(db.String(30))
    matricula = db.Column(db.String(10))
    tutor1 = db.Column(db.String(30))
    contacto1 = db.Column(db.String(30))
    tutor2 = db.Column(db.String(30))
    contacto2 = db.Column(db.String(30))
    actiu = db.Column(db.Integer)
    identificador_ant = db.Column(db.String(15))
    id_med = db.Column(db.Integer)
    id_fis = db.Column(db.Integer)
    id_psi = db.Column(db.Integer)
    cip = db.Column(db.String(25))
    consentiment = db.Column(db.Integer)
    data_consentiment = db.Column(db.Date)
    data_revisiom = db.Column(db.Date)
    consentiment_dad = db.Column(db.Integer)
    consentiment_proinf = db.Column(db.Integer)
    pro_sal_es = db.Column(db.Integer)
    e_mail2 = db.Column(db.String(52))
    password = db.Column(db.String(128))
    salt = db.Column(db.String(20))
    def __init__(self, foto, dni, passaport, nom, cognom1, cognom2, sexe, ss, tipus, data_neix, lloc_neix \
    , provincia_neix, comarca_neix, auto_neix, pais_neix, direccio, poblacio, provincia, cp, comarca \
    , autonomia, pais, telefon1, telefon2, e_mail, estudis_act, nivel_academic, tipus_centre, nom_centre, aceptacio \
    , revisiom, revisiops, fitxacomplerta, vehicle, matricula, tutor1, contacto1, tutor2, contacto2, actiu \
    , identificador_ant, id_med, id_fis, id_psi, cip, consentiment, data_consentiment, data_revisiom \
    , consentiment_dad, consentiment_proinf, pro_sal_es, e_mail2, password, salt):
        self.foto = foto
        self.dni = dni
        self.passaport = passaport
        self.nom = nom
        self.cognom1 = cognom1
        self.cognom2 = cognom2
        self.sexe = sexe
        self.ss = ss
        self.tipus = tipus
        self.data_neix = data_neix
        self.lloc_neix = lloc_neix
        self.provincia_neix = provincia_neix
        self.comarca_neix = comarca_neix
        self.auto_neix = auto_neix
        self.pais_neix = pais_neix
        self.direccio = direccio
        self.poblacio = poblacio
        self.provincia = provincia
        self.cp = cp
        self.comarca = comarca
        self.autonomia = autonomia
        self.pais = pais
        self.telefon1 = telefon1
        self.telefon2 = telefon2
        self.e_mail = e_mail
        self.estudis_act = estudis_act
        self.nivel_academic = nivel_academic
        self.tipus_centre = tipus_centre
        self.nom_centre = nom_centre
        self.aceptacio = aceptacio
        self.revisiom = revisiom
        self.revisiops = revisiops
        self.fitxacomplerta = fitxacomplerta
        self.vehicle = vehicle
        self.matricula = matricula
        self.tutor1 = tutor1
        self.contacto1 = contacto1
        self.tutor2 = tutor2
        self.contacto2 = contacto2
        self.actiu = actiu
        self.identificador_ant = identificador_ant
        self.id_med = id_med
        self.id_fis = id_fis
        self.id_psi = id_psi
        self.cip = cip
        self.consentiment = consentiment
        self.data_consentiment = data_consentiment
        self.data_revisiom = data_revisiom
        self.consentiment_proinf = consentiment_proinf
        self.pro_sal_es = pro_sal_es
        self.e_mail2 = e_mail2
        self.set_password(password)
        self.salt = salt
    def set_password(self, password):
        self.password = hashlib.sha256('[B@3f13a310' + password).hexdigest()
    def check_password(self, password):
        if self.password == hashlib.sha256('[B@3f13a310' + password).hexdigest():
            return True
        else:
            return False
