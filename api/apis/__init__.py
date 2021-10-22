from flask_restplus import Api
from .Property import api as nsProperties
from .User import api as nsUsers
from .Report import api as nsReports

api = Api(
    title='Trobify API',
    version='1.0',
    description='this is the trobify API',
    prefix='/api'
)

api.add_namespace(nsProperties, path='/property')
api.add_namespace(nsUsers, path='/user')
api.add_namespace(nsReports, path='/report')
