from flask_restplus import Api
from .ArpTable import api as nsArpTable

api = Api(
    title='Simple API',
    version='1.0',
    description='this is a simple API',
    prefix='/api'
)

api.add_namespace(nsArpTable, path='/arp_table')