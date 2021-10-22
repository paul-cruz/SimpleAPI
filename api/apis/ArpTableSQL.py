import os
import psycopg2
from flask import jsonify
from bson.objectid import ObjectId
from flask_restplus import Namespace, Resource, fields
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData

db_string = "postgresql://sample:MyPassw0rd@localhost:5432/networks_project"

db = create_engine(db_string)

with db.connect() as conn:
  print("hola", conn)

try:
    #conexion1 = psycopg2.connect(host="0.0.0.0", port="5430", dbname="networks_project", connect_timeout="10", user="sample", password="MyPassw0rd")
    print("Accepted")
except Exception as e:
    print(e)

api = Namespace('arp_table_sql', description='arp table related operations using SQL')

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
      cursor1=conexion1.cursor()
      cursor1.execute("SELECT * FROM arp")
      rows = []
      for fila in cursor1:
        print(fila)
        rows.append(fila)
      return rows 

    @api.doc('post_arp_table')
    @api.expect(arp_table)
    def post(self):
        try:
          data = api.payload
          print(data)
          cursor1=conexion1.cursor()
          sql = "INSERT INTO arp(interface, mac, ip, age) VALUES(%s, %s, %s, %s)"
          datos=("naranjas", 23.50)
          cursor1.execute(sql, datos)
          #conexion1.commit()
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
            cursor1=conexion1.cursor()
            cursor1.execute("SELECT * FROM arp WHERE id = " + id)
            rows = []
            for fila in cursor1:
              print(fila)
              rows.append(fila)
            if rows:
              return rows 
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
            data = api.payload
            print(data)
            cursor1=conexion1.cursor()
            sql = "UPDATE arp SET interface = %s, ip = %s, age=%s WHERE mac = %s"
            datos=("naranjas", 23.50)
            cursor1.execute(sql, datos)
            #conexion1.commit()
            return True
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
            data = api.payload
            print(data)
            cursor1=conexion1.cursor()
            sql = "DELETE FROM arp WHERE mac = %s"
            datos=("naranjas")
            cursor1.execute(sql, datos)
            #conexion1.commit()
            return True
            raise ValueError('arp_table not found')
        except ValueError as ve:
            print('arp_table exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)
