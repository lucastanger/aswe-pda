from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class MongoDB:
    """
    Creates a connection to the mongodb.
    """
    __instance = None

    def __init__(self):
        try:
            client = MongoClient(host='mongo', port=27017, serverSelectionTimeoutMS=1000)
            client.server_info()
        except ServerSelectionTimeoutError:
            client = MongoClient(host='localhost', port=27017, serverSelectionTimeoutMS=1000)
            client.server_info()
        self.db = client['aswe-pda']
        self.db.authenticate('dev', 'dev')

    @classmethod
    def instance(cls):
        """
        Returns a singleton instance of this class. Upon its first call, a new instance
        is being created. On all subsequent calls, the already created instance is returned.
        :return: Singleton instance of this class.
        """
        if cls.__instance:
            return cls.__instance
        else:
            cls.__instance = MongoDB()
            return cls.__instance
