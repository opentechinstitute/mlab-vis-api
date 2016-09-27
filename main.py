# -*- coding: utf-8 -*-
'''
App Entry Point
'''
from __future__ import print_function
import logging

from flask_restplus import cors

# Import Configured Flask App
from mlab_api.app import app

# Import namespaces
from mlab_api.endpoints.locations import locations_ns
from mlab_api.endpoints.debug import debug_ns
from mlab_api.endpoints.clients import client_asn_ns
from mlab_api.endpoints.servers import server_asn_ns

# API is defined here
from mlab_api.rest_api import api

root = logging.getLogger()
root.setLevel(logging.DEBUG)

# This appears to provide CORS for all API Requests
api.decorators = [cors.crossdomain(origin='*')]

# Add namespaces defined in endpoints module
api.add_namespace(locations_ns)
api.add_namespace(client_asn_ns)
api.add_namespace(server_asn_ns)

# init api with Flask App
api.init_app(app)

print(app.config['API_MODE'])
debug_flag = True

if app.config['API_MODE'] == 'PROD':
    debug_flag = False
    print('PRODUCTION MODE')
else:
    debug_flag = True
    api.add_namespace(debug_ns)
    print('DEBUG MODE')

if __name__ == '__main__':
    app.run(port=8080, debug=debug_flag)
