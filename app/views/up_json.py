# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import Blueprint, request, jsonify, make_response
from app.models import Post, UsersSchema, A_GE_CAR_PERSONA
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app import app, db
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import text, create_engine
import string
import random

def password_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

users = Blueprint('users', __name__)

schema = UsersSchema()
api = Api(users)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

class UsersList(Resource):
    def get(self):
        users_query = Post.query.all()
        results = schema.dump(users_query, many=True).data
        return jsonify(results)

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
                schema.validate(raw_dict)
                user_dict = raw_dict['data']['attributes']
                user = A_GE_CAR_PERSONA(user_dict['foto'], user_dict['dni'], \
                user_dict['passaport'], user_dict['nom'], user_dict['cognom1'], \
                user_dict['cognom2'], user_dict['sexe'], user_dict['ss'], \
                user_dict['tipus'], user_dict['data_neix'], user_dict['lloc_neix'], \
                user_dict['provincia_neix'], user_dict['comarca_neix'], user_dict['auto_neix'], \
                user_dict['pais_neix'], user_dict['direccio'], user_dict['poblacio'], \
                user_dict['provincia'], user_dict['cp'], user_dict['comarca'], \
                user_dict['autonomia'], user_dict['pais'], user_dict['telefon1'], \
                user_dict['telefon2'], user_dict['e_mail'], user_dict['estudis_act'], \
                user_dict['nivel_academic'], user_dict['tipus_centre'], user_dict['nom_centre'], \
                user_dict['aceptacio'], user_dict['revisiom'], user_dict['revisiops'], \
                user_dict['fitxacomplerta'], user_dict['vehicle'], user_dict['matricula'], \
                user_dict['tutor1'], user_dict['contacto1'], user_dict['tutor2'], \
                user_dict['contacto2'], user_dict['actiu'], user_dict['identificador_ant'], \
                user_dict['id_med'], user_dict['id_fis'], user_dict['id_psi'], \
                user_dict['cip'], user_dict['consentiment'], \
                user_dict['data_consentiment'], user_dict['data_revisiom'], \
                user_dict['consentiment_dad'], user_dict['consentiment_proinf'], \
                user_dict['pro_sal_es'], user_dict['e_mail2'], password_generator(), 'salt')
                user.add(user)
                query = A_GE_CAR_PERSONA.query.get(user.id)
                results = schema.dump(query).data                
                return results, 201
#                return 'okey', 201
                
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 403
                return resp
                
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 403
                return resp

class UsersUpdate(Resource):    
    def get(self, id):
        user_query = Post.query.get_or_404(id)
        result = schema.dump(user_query).data
        return result

    def patch(self, id):
        user = Post.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            user_dict = raw_dict['data']['attributes']
            for key, value in user_dict.items():        
                setattr(user, key, value)  
            user.update()            
            return self.get(id)    
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp                       
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp 

    def delete(self, id):
        user = Post.query.get_or_404(id)
        try:
            delete = user.delete(user)
            response = make_response()
            response.status_code = 204
            return response    
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp

api.add_resource(UsersList, '.json')
api.add_resource(UsersUpdate, '/<int:id>.json')
