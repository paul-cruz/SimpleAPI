import psycopg2
from flask_restplus import Namespace, Resource, fields

try:
    conexion1 = psycopg2.connect(
        "postgresql://maqkdosvkohfxz:2c8f3f1893ffbdcf513a5fb614c7119ff409377f4858e82c3449b4b73e179285@ec2-52-3-239-135.compute-1.amazonaws.com:5432/db0d4m6v47f411")
    print(conexion1)
except Exception as e:
    print(e)

api = Namespace('arp_table_sql',
                description='arp table related operations using SQL')

arp_table = api.model('ARP_TABLE', {
    "interface": fields.String(description='Interface of the device'),
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
        cursor1 = conexion1.cursor()
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
            print(data["interface"])
            cursor1 = conexion1.cursor()
            sql = "INSERT INTO arp(interface, mac, ip, age) VALUES(%s, %s, %s, %s)"
            datos = (data["interface"], data["mac"], data["ip"], data["age"])
            cursor1.execute(sql, datos)
            conexion1.commit()
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
            cursor1 = conexion1.cursor()
            cursor1.execute("SELECT * FROM arp WHERE mac = '" + id + "'")
            rows = []
            for fila in cursor1:
                print(fila)
                rows.append(fila)
            if rows:
                return rows

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
            cursor1 = conexion1.cursor()
            sql = "UPDATE arp SET interface = %s, ip = %s, age=%s WHERE mac = %s"
            datos = (data["interface"], data["ip"], data["age"], id)
            cursor1.execute(sql, datos)
            conexion1.commit()
            return True

        except ValueError as ve:
            print('arp_table exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)

    @api.doc('delete_arp_table')
    def delete(self, id):
        try:
            cursor1 = conexion1.cursor()
            sql = "DELETE FROM arp WHERE mac = '" + id + "'"
            cursor1.execute(sql)
            conexion1.commit()
            return True

        except ValueError as ve:
            print('arp_table exception', ve)
            api.abort(404)
        except Exception as e:
            print('Server Error', e)
            api.abort(500)
