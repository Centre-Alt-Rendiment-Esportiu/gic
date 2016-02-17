# -*- coding: utf-8 -*-
"""
@author: dani.ruiz
"""
from flask import Blueprint, request, jsonify, make_response
from app.models import Post, UsersSchema
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app import app, db
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import text, create_engine

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
                user = Post(user_dict['nom'], user_dict['cognom1'], user_dict['cognom2'], user_dict['sexe'], user_dict['dni'] \
                , user_dict['passport'], user_dict['data_naix'], user_dict['telefon1'], user_dict['telefon2'] \
                , user_dict['email1'], user_dict['email2'], user_dict['actiu'], user_dict['foto'], '1234')
                user.add(user)
                query = Post.query.get(user.id)
                results = schema.dump(query).data                
                return results, 201
                
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
