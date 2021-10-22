import os
import pymongo
from flask import jsonify
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument
from flask_restplus import Namespace, Resource, fields

myclient = pymongo.MongoClient(os.getenv("BD_CONN"))
db = myclient[os.getenv("DB_NAME")]
propCol = db["properties"]
api = Namespace('arp_table', description='arp table related operations')

arp_table = api.model('ARP_TABLE', {
    "interface": fields.String(readonly=True, description='Interface of the device'),
    "mac": fields.String(),
    "ip": fields.String(),
    "age": fields.Float(),
})


@api.route('/')
@api.response(404, 'arp_table not inserted')
@api.response(500, 'Server Error')
class Properties(Resource):
    @api.doc('list_properties')
    def get(self):
        return list(propCol.find())

    @api.doc('post_arp_table')
    @api.expect(arp_table)
    def post(self):
        try:
            result_id = propCol.insert_one(api.payload).inserted_id
            if result_id:
                return {'msg': 'Inserted'}, 201
            raise ValueError('arp_table not found')
        except ValueError as ve:
            print('arp_table exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)


@api.route('/<id>')
@api.param('id', 'The arp_table identifier')
@api.response(404, 'arp_table not found')
@api.response(500, 'Server Error')
class arp_table(Resource):
    @api.doc('get_arp_table')
    def get(self, id):
        try:
            result = propCol.find_one({'_id': ObjectId(id)})
            if result:
                return result
            raise ValueError('arp_table not found')
        except ValueError as ve:
            print('arp_table exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('put_arp_table')
    @api.expect(arp_table)
    def put(self, id):
        try:
            doc = api.payload
            result = propCol.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': doc},
                return_document=ReturnDocument.AFTER)
            if result:
                return {'msg': 'Updated'}, 200
            raise ValueError('arp_table not found')
        except ValueError as ve:
            print('arp_table exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('delete_arp_table')
    def delete(self, id):
        try:
            result = propCol.find_one_and_delete({'_id': ObjectId(id)})
            if result:
                return {'msg': 'Deleted'}, 200
            raise ValueError('arp_table not found')
        except ValueError as ve:
            print('arp_table exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)
