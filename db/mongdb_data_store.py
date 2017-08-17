from pymongo import MongoClient

from config import celery_config


class DBStore(object):
    mongdb_conn = None

    @staticmethod
    def _initialize():
        mongdb_conn = MongoClient(**celery_config.MONGODB_SETTINGS)

    @staticmethod
    def get_datastores():
        if DBStore.mongdb_conn is None:
            DBStore._initialize()
        return DBStore.mongdb_conn

