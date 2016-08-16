# -*- coding: utf-8 -*-
'''
App Entry Point
'''
from __future__ import print_function

import atexit
import logging

from flask import Flask, request

from flask_restplus import Resource, cors

from mlab_api.data.data import Data
from mlab_api.data.table_config import read_table_configs



app = Flask(__name__) #pylint: disable=C0103
app.config.from_object('config')
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
app.config['RESTPLUS_VALIDATE'] = True



TABLE_CONFIGS = read_table_configs(app.config['BIGTABLE_CONFIG_DIR'])
DATA = Data(app.config, TABLE_CONFIGS)



def exit_handler():
    """
    Called at program exit
    """
    logging.info('Closing Connection')
    DATA.close()

# register exit handler
# TODO: may be a better Flask way to do this.
atexit.register(exit_handler)