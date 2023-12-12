import os
from pymongo import MongoClient
from logger.logger_base import log

class CreatePlantModel:
    def __init__(self):
        self.client = None
        self.db = None

    def connect_to_database(self):
        mongodb_user = "admin"
        mongodb_pass = "pas123"
        mongodb_host = "localhost"

        required_variables = {'MONGODB_USER': mongodb_user, 'MONGODB_PASS': mongodb_pass, 'MONGODB_HOST': mongodb_host}

        for var, val in required_variables.items():
            if not val:
                log.critical(f'{var} variable not found')
                raise ValueError(f'Set {var} variable')

        try:
            self.client = MongoClient(
                host=mongodb_host,
                port=27017,
                username=mongodb_user,
                password=mongodb_pass,
                authSource='admin',
                authMechanism='SCRAM-SHA-256'
            )
            self.db = self.client['LeafLove']
        except Exception as e:
            log.critical(f'Failed to connect to the database: {e}')
            raise

    def close_connection(self):
        if self.client:
            self.client.close()