'''
Django environment setting.
'''
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = ('data',)

SECRET_KEY = 'REPLACE_ME'

from pysite.pysite.local_settings import DATABASES
