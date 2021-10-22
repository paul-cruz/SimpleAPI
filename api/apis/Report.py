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
propCol = db["reports"]
api = Namespace('reports', description='reports related operations')

report = api.model('Reports',{
    "description": fields.String(),
    "images":fields.List(fields.String()),
    "user":fields.Raw(example={
        "id":ObjectId()
    }),
})

@api.route('/')
@api.response(404, 'Report not inserted')
@api.response(500, 'Server Error')
class Reports(Resource):
    @api.doc('list_reports')
    def get(self):
        return list(propCol.find())

    @api.doc('post_report')
    @api.expect(report)
    @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
    def post(self):
        try:
            result_id = propCol.insert_one(api.payload).inserted_id
            if result_id:
                return{'msg': 'Inserted'}, 201
            raise ValueError('Report not found')
        except ValueError as ve:
            print('Report exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)
            



@api.route('/<id>')
@api.param('id', 'The report identifier')
@api.response(404, 'Report not found')
@api.response(500, 'Server Error')
class Report(Resource):
    @api.doc('get_report')
    def get(self, id):
        try:
            result = propCol.find_one({'_id': ObjectId(id)})
            if result:
                return dumps(result)
            raise ValueError('Report not found')
        except ValueError as ve:
            print('Report exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('put_report')
    @api.expect(report)
    def put(self, id):
        try:
            doc = api.payload
            result = propCol.find_one_and_update(
                {'_id': ObjectId(id)},
                {'$set': doc},
                return_document=ReturnDocument.AFTER
            )
            if result:
                return{'msg': 'Updated'}, 200
            raise ValueError('Report not found')
        except ValueError as ve:
            print('Report exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('delete_report')
    def delete(self, id):
        try:
            result = propCol.find_one_and_delete({'_id': ObjectId(id)})
            if result:
                return {'msg': 'Deleted'}, 200
            raise ValueError('Report not found')
        except ValueError as ve:
            print('Report exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

