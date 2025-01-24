from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, host="localhost", port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        try:
            self.connection = MongoClient(self.host, self.port)
            return self.connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
