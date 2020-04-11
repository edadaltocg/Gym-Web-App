'''
    Mongo db configuration
'''
import os
from flask_pymongo import PyMongo

MONGO_URI = os.environ.get('MONGO_URI')
mongo = PyMongo()
