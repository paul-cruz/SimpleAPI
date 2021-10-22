import os
import pymongo
from flask import jsonify
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument
from flask_restplus import Namespace, Resource, fields

myclient = pymongo.MongoClient(os.getenv("BD_CONN"))
db = myclient[os.getenv("DB_NAME")]
propCol = db["properties"]
api = Namespace('properties', description='properties related operations')

apoiment = api.model('Apoiment', {
    "ref": fields.Integer(),
    "date": fields.Date()
})

property = api.model('Properties', {
    "tittle": fields.String(),
    "price": fields.Integer(),
    "features": fields.Raw(example={
        "land": 0.0,
        "built": 0.0,
        "rooms": 0,
        "bathrooms": 0,
        "kitchens": 0,
        "garage": 0
    }),
    "address": fields.Raw(example={
        "line1": "",
        "state": "",
        "zip": "",
        "city": ""
    }),
    "location": fields.Raw(example={
        "lat": 0.0,
        "long": 0.0
    }),
    "description": fields.String(),
    "type": fields.String(),
    "age": fields.Integer(),
    "floors": fields.Integer(),
    "contact": fields.Raw(example={
        "name": "",
        "phones": [""],
        "email": ""
    }),
    "apoiments": fields.List(fields.Nested(apoiment))
})


@api.route('/')
@api.response(404, 'Property not inserted')
@api.response(500, 'Server Error')
class Properties(Resource):
    @api.doc('list_properties')
    def get(self):
        return list(propCol.find())

    @api.doc('post_property')
    @api.expect(property)
    def post(self):
        try:
            result_id = propCol.insert_one(api.payload).inserted_id
            if result_id:
                return {'msg': 'Inserted'}, 201
            raise ValueError('Property not found')
        except ValueError as ve:
            print('Property exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)


@api.route('/<id>')
@api.param('id', 'The property identifier')
@api.response(404, 'Property not found')
@api.response(500, 'Server Error')
class Property(Resource):
    @api.doc('get_property')
    def get(self, id):
        try:
            result = propCol.find_one({'_id': ObjectId(id)})
            if result:
                return result
            raise ValueError('Property not found')
        except ValueError as ve:
            print('Property exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('put_property')
    @api.expect(property)
    def put(self, id):
        try:
            doc = api.payload
            result = propCol.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': doc},
                return_document=ReturnDocument.AFTER)
            if result:
                return {'msg': 'Updated'}, 200
            raise ValueError('Property not found')
        except ValueError as ve:
            print('Property exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('delete_property')
    def delete(self, id):
        try:
            result = propCol.find_one_and_delete({'_id': ObjectId(id)})
            if result:
                return {'msg': 'Deleted'}, 200
            raise ValueError('Property not found')
        except ValueError as ve:
            print('Property exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)
