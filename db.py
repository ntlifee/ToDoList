from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, host="mongo", port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
