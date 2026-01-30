from flask_pymongo import PyMongo
from flask import g, current_app

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)

def get_db():
    if 'db' not in g:
        g.db = mongo.db
    return g.db
