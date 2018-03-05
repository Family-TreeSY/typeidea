# coding:utf-8

from .base import *  # NOQA

'''
NOQA:告诉PEP8检测工具，这里不需要检测
'''

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


