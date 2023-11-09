import sqlite3
from sqlite3 import Error
from VectorMass.entity import DatabaseConfig
import os
from VectorMass.utils.common import read_yaml, create_directories

class DatabaseConnection:
    def __init__(self, config:DatabaseConfig):
        self.config = config

    def create_connection(self, db_path=''):
        """ create a database connection to a SQLite database """
        conn = None

        try:
            if db_path != '' and not os.path.exists(db_path):
                create_directories([db_path])

            db_path = os.path.join(db_path, self.config.db_name)
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)
        finally:
            return conn
