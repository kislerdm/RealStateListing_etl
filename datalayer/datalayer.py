import psycopg2
import logging

logger = logging.getLogger(__name__)

class databaseConnection(object):
    """
    Class to create connection to the postgres database
    """
    _instance = None
    def __new__(cls,db_config):
        """
        function to initialize the database connection
        :param db_config: db parameter read from config.txt
        :return: returns singleton instance of the class
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                logger.info('Connecting to database.')
                databaseConnection._instance.connection = psycopg2.connect(**db_config)
                databaseConnection._instance.cursor = databaseConnection._instance.connection.cursor()

            except Exception as e:
                logger.error('Connection not established {}'.format(e))
                databaseConnection._instance = None
                raise
            else:
                logger.info('connection established')

        return cls._instance

    def __init__(self, db_config):
        """
        Initialize the parameter with the class variable
        :param db_config: not used
        """
        self._db_connection =  self._instance.connection
        self._db_cur = self._instance.cursor

    def query(self, query, params):
        """

        :param query: query to be executed on database
        :param params: dictionary containing bind parameters.
        :return: result of execute.
        """
        return self._db_cur.execute(query, params)

    def __del__(self):
        logger.info("Closing the connection")
        self._db_connection.close()

if __name__ == "__main__":
    db_config = {'dbname': '', 'host': '',
                 'password': '', 'port': "" , 'user': ''}
    db = databaseConnection(db_config)
