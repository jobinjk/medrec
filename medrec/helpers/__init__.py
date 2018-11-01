from .paginator import paginate
from ..config import conf
import os


def loadconf():
    '''
    Load the server configuration
    '''
    env = os.getenv('MEDREC_CONFIG', 'default').lower()
    config = conf[env]
    return config
