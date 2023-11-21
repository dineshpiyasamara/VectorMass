import numpy as np
import sqlite3
from sqlite3 import Error
import os
from .collection_operations import (Collection)
from VectorMass.config.configuration import ConfigurationManager
from VectorMass.queries.queries import *
from VectorMass.utils.common import read_yaml, create_directories
from VectorMass.logging import logger

config_manager = ConfigurationManager()
config = config_manager.database_config()

class Client:
    def __init__(self, db_path=''):
        self.config = config
        self.conn = self._create_connection(db_path)
        self.cursor = self.conn.cursor()
        logger.info(self.conn)

    def _create_connection(self, db_path):
        """
        Create a database connection to a SQL database
        
        Args:
            db_path (str): Path to store database

        Returns:
            A connection object
        """
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

    def create_or_get_collection(self, collection_name):
        """
        Create or get collection

        Args:
            collection_name (str): Name of the collection

        Returns:
            Collection object
        """
        self.cursor.execute(CHECK_COLLECTION_EXIST, (collection_name,))
        collection_exists = self.cursor.fetchone()

        if collection_exists:
            print(f"Collection '{collection_name}' already exists.")
        else:
            # Create the collection if it doesn't exist
            self.cursor.execute(CREATE_COLLECTION, (collection_name,))
            print(f"Collection '{collection_name}' created.")
        self.conn.commit()
        collection = Collection(conn=self.conn, cursor=self.cursor, collection_name=collection_name)
        return collection
    

    def create_collection(self, collection_name):
        # Check if the collection already exists
        self.cursor.execute(CHECK_COLLECTION_EXIST, (collection_name,))
        collection_exists = self.cursor.fetchone()

        if collection_exists:
            print(f"Collection '{collection_name}' already exists.")
        else:
            # Create the collection if it doesn't exist
            self.cursor.execute(CREATE_COLLECTION, (collection_name,))
            print(f"Collection '{collection_name}' created.")
        
        self.conn.commit()


    def get_collection(self, collection_name):
        # Check if the collection already exists
        self.cursor.execute(CHECK_COLLECTION_EXIST, (collection_name,))
        collection_exists = self.cursor.fetchone()

        if collection_exists:
            print(f"Collection '{collection_name}' already exists.")
            collection = Collection(conn=self.conn, cursor=self.cursor, collection_name=collection_name)
            return collection
        else:
            print(f"Collection '{collection_name}' not found.")
            return None

