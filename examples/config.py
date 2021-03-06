# config.py

# a bit hacky way of getting latest
# version without installing it
import sys
sys.path.append('..')

import cklass


class Root:
    _environ_prefix = 'SIMPLEWEBAPP'
    _config_filepath = ['./conf']
    _secret_filepath = ['./conf']


class Common(Root):
    NAME = 'Simple Web App'
    DEBUG = True
    DATE = ''

    BASE_DIR = '/app'
    SRC_DIR = './src'

    ALLOWED_HOSTS = []

    class Empty:
        NOT_SET_ANYWHERE = True

    class Secret:
        KEY = ''
        MAGIC = 0

    _config_filename = 'common.yaml'
    _secret_filename = 'common.json'


class Database(Root):
    ENGINE = 'sqlite3'
    HOST = 'localhost'
    NAME = 'simplewebapp_db'

    class Credentials:
        USER = 'readonly'
        PASS = 'readonly'

    _config_filename = 'database.yaml'
    _secret_filename = 'database.json'


cklass.load_config(Common)
cklass.load_config(Database)


print(f'''
cklass.__version__ = '{cklass.__version__}'

Common:
    NAME = '{Common.NAME}'
    DEBUG = {Common.DEBUG}
    DATE = '{Common.DATE}'

    BASE_DIR = '{Common.BASE_DIR}'
    SRC_DIR = '.{Common.SRC_DIR}'

    ALLOWED_HOSTS = {Common.ALLOWED_HOSTS}

    Empty:
        NOT_SET_ANYWHERE = {Common.Empty.NOT_SET_ANYWHERE}

    Secret:
        KEY = '{Common.Secret.KEY}'
        MAGIC = {Common.Secret.MAGIC}


Database:
    ENGINE = '{Database.ENGINE}'
    HOST = '{Database.HOST}'
    NAME = '{Database.NAME}'

    Credentials:
        USER = {Database.Credentials.USER}'
        PASS = '{Database.Credentials.PASS}'
''')
