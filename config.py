"""
use a class to store configuration variables and keep it in a different module
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
    LANGUAGES = ['en','es']
    DEEPL_AUTH_KEY = os.environ.get('DEEPL_AUTH_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    ELASTICSEARCH_UN = os.environ.get('ELASTICSEARCH_UN')
    ELASTICSEARCH_PW = os.environ.get('ELASTICSEARCH_PW')
    ELASTICSEARCH_CERT_PATH = os.environ.get('ELASTICSEARCH_CERT_PATH')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')[0]
    