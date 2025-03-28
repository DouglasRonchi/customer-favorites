import mongoengine

from app.settings import settings
from app.utils.conflog import logger
from app.utils.singleton import SingletonMeta


class MongoDBConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.mongodb_host = settings.MONGO_URI
        self.client = None
        self._set_connection()

    def _set_connection(self):
        try:

            logger.info("Connecting to MongoDB...")
            get_connection = self.get_existing_connection()
            if not get_connection:
                self.client = mongoengine.connect(host=self.mongodb_host)
            logger.info("Connected to MongoDB.")
        except Exception as error:
            logger.error("MongoDB connection error: %s", error)
            raise mongoengine.ConnectionFailure(
                "Mongoengine Connection Error"
            ) from error

    def get_existing_connection(self):
        try:
            if mongoengine.connection.get_connection() is None:
                logger.info("No existing connection found.")
                return False
            logger.info("Existing connection found.")
            return True
        except mongoengine.ConnectionFailure:
            logger.info("No existing connection found.")
            return False
