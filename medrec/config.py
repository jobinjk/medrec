from uuid import uuid4
from datetime import timedelta
import os

base_dir = os.path.dirname(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'this is something that we usually give no importance'

    HOST = 'localhost'
    PORT = 27017
    DB = 'MEDREC'
    USERNAME = ''
    PASSWORD = ''

    JWT_ACCESS_TOKEN_EXPIRES = False

    MONGODB_SETTINGS = [{
        'db': DB,
        'host': HOST,
        'port': PORT
    }]

    # CELERY_BROKER_URL = 'redis://localhost:6379/1'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    ENABLE_SHARDING = False


# class Production(Config):
#     DEBUG = True
#     SECRET_KEY = 'this is something that we usually give no importance!'

#     HOST = 'mongodb://datahut:cGFzc21lMTIz@138.197.68.56:27017/QA?authSource=admin'
#     # PORT = 27045
#     # USERNAME = 'rootuser'
#     # PASSWORD = 'cGFzc21lMTIz'
#     # DB = 'QA'

#     JWT_ACCESS_TOKEN_EXPIRES = False

#     MONGODB_SETTINGS = [{
#         # 'db': DB,
#         'host': HOST,
#         # 'port': PORT,
#         # 'username': USERNAME,
#         # 'password': PASSWORD
#     }]

#     CELERY_BROKER_URL = 'redis://localhost:6379/1'
#     CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
#     ENABLE_SHARDING = True


class Developement(Config):
    DEBUG = True
    SECRET_KEY = 'this is something that we usually give no importance!'
    BASE_DIR = base_dir
    QR_DIR = os.path.join(BASE_DIR, 'qr_images')

    if not os.path.isdir(QR_DIR):
        os.mkdir(QR_DIR)

    HOST = 'localhost'
    PORT = 27017
    DB = 'MEDREC'
    USERNAME = ''
    PASSWORD = ''

    JWT_ACCESS_TOKEN_EXPIRES = False

    MONGODB_SETTINGS = [{
        'db': DB,
        'host': HOST,
        'port': PORT
    }]

    # CELERY_BROKER_URL = 'redis://localhost:6379/1'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    ENABLE_SHARDING = False


conf = {
    'developement': Developement,
    # 'production': Production,
    'default': Developement,
}
