from pymongo import MongoClient
import logging
import os


def connect():
    mongoUrl = os.environ.get('MONGO_URL', 'mongodb://mongo:27017')
    logging.info('mongo URL : ' + mongoUrl)
    client = MongoClient(mongoUrl)
    return client.happy
