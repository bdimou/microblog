"""
use a class to store configuration variables and keep it in a different module
"""

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"