'''
Django environment setting.
'''
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PttBoardsEntity',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'CHARSET': 'UTF8',
    }
}

INSTALLED_APPS = ('data',)

SECRET_KEY = 'REPLACE_ME'
