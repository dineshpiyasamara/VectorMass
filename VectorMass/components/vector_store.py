import sqlite3
from sqlite3 import Error
import os
from .collection_operations import (Collection)
from VectorMass.config.configuration import ConfigurationManager
from VectorMass.queries.queries import *
from VectorMass.utils.common import create_directories
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
            logger.info(e)
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
            logger.info(f"Collection '{collection_name}' already exists.")
        else:
            # Create the collection if it doesn't exist
            self.cursor.execute(CREATE_COLLECTION, (collection_name,))
            logger.info(f"Collection '{collection_name}' created.")
        self.conn.commit()
        collection = Collection(conn=self.conn, cursor=self.cursor, collection_name=collection_name)
        return collection


    def drop_collection(self, collection_name):
        """
        Drop a collection

        Args:
            collection_name (str): Name of the collection
        """
        try:
            self.cursor.execute(CHECK_COLLECTION_EXIST, (collection_name,))
            collection_exists = self.cursor.fetchone()
            if collection_exists:
                self.cursor.execute(DROP_COLLECTION.format(collection_name))
                self.conn.commit()
                logger.info(f"Collection '{collection_name}' succesfully deleted.")
            else:
                logger.info(f"Collection '{collection_name}' not found.")
        except Exception as e:
            logger.error(e)
    
    def reset_vectorstore(self):
        """
        Reset vectorstore
        """
        try:
            self.cursor.execute(GET_ALL_COLLECTIONS)
            collections = self.cursor.fetchall()
            for collection in collections:
                collection_name = collection[0]
                self.cursor.execute(DROP_COLLECTION.format(collection_name))
            self.conn.commit()
            logger.info("Vector Store reset succesfull")
        except Exception as e:
            logger.error(e)
