import os
import pymongo
from flask import jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from pymongo.collection import ReturnDocument
from flask_restplus import Namespace, Resource, fields
from flask_cors import cross_origin

myclient = pymongo.MongoClient(os.getenv("BD_CONN"))
db = myclient[os.getenv("DB_NAME")]
propCol = db["users"]
api = Namespace('users', description='users related operations')

user = api.model('Users', {
    "first_name": fields.String(),
    "last_name": fields.String(),
    "email": fields.String(),
    "password": fields.String(),
    "favorites": fields.List(fields.Raw(example={
        "id": ObjectId()
    })),
})

login = api.model('Logins',{
    "email": fields.String(),
    "password": fields.String(),
})


@api.route('/')
@api.response(404, 'User not inserted')
@api.response(500, 'Server Error')
class Users(Resource):
    @api.doc('list_users')
    def get(self):
        return list(propCol.find())

    @api.doc('post_user')
    @api.expect(user)
    @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
    def post(self):
        try:
            result_id = propCol.insert_one(api.payload).inserted_id
            if result_id:
                return{'msg': 'Inserted'}, 201
            raise ValueError('User not found')
        except ValueError as ve:
            print('User exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)
            



@api.route('/<id>')
@api.param('id', 'The user identifier')
@api.response(404, 'User not found')
@api.response(500, 'Server Error')
class User(Resource):
    @api.doc('get_user')
    def get(self, id):
        try:
            result = propCol.find_one({'_id': ObjectId(id)})
            if result:
                return result
            raise ValueError('User not found')
        except ValueError as ve:
            print('User exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('put_user')
    @api.expect(user)
    def put(self, id):
        try:
            doc = api.payload
            print(doc, id)
            result = propCol.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': doc},
                return_document=ReturnDocument.AFTER
            )
            if result:
                return{'msg': 'Updated'}, 200
            raise ValueError('User not found')
        except ValueError as ve:
            print('User exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('delete_user')
    def delete(self, id):
        try:
            result = propCol.find_one_and_delete({'_id': ObjectId(id)})
            if result:
                return {'msg': 'Deleted'}, 200
            raise ValueError('User not found')
        except ValueError as ve:
            print('User exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)


@api.route('/login')
@api.response(404, 'User not found')
@api.response(500, 'Server Error')
class UserLogin(Resource):
    @api.doc('login_user')
    @api.expect(login)
    def post(self):
        try:
            log = api.payload
            print(log)
            user = propCol.find_one({'email' : log['email']})
            if user:
                if user['password'] == log['password']:
                    return {'msg': 'Logged', 'id': user['_id']}, 200
                raise ValueError('Invalid password')
            raise ValueError('User not found')
        except ValueError as ve:
            print('User exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)