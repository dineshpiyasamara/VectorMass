import numpy as np
import sqlite3
from sqlite3 import Error
import os
from .collection_operations import (Collection)
from VectorMass.config.configuration import ConfigurationManager
from VectorMass.queries.queries import *
from VectorMass.utils.common import read_yaml, create_directories

config_manager = ConfigurationManager()
config = config_manager.database_config()

class Client:
    def __init__(self, db_path=''):
        self.vector_data = {}  # A dictionary to store vectors
        self.vector_index = {}  # An indexing structure for retrieval

        self.config = config
        self.conn = self._create_connection(db_path)
        self.cursor = self.conn.cursor()
        print(self.conn)

    def _create_connection(self, db_path):
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

    def create_or_get_collection(self, collection_name):
        # Check if the collection already exists
        self.cursor.execute(check_collection_exist, (collection_name,))
        collection_exists = self.cursor.fetchone()

        if collection_exists:
            print(f"Collection '{collection_name}' already exists.")
        else:
            # Create the collection if it doesn't exist
            self.cursor.execute(create_collection.format(collection_name))
            print(f"Collection '{collection_name}' created.")
        self.conn.commit()
        collection = Collection(conn=self.conn, cursor=self.cursor)
        return collection


    def add_vector(self, vector_id, vector):
        """
        Add a vector to the store.

        Args:
            vector_id (str or int): A unique identifier for the vector.
            vector (numpy.ndarray): The vector data to be stored.
        """
        self.vector_data[vector_id] = vector
        self._update_index(vector_id, vector)

    def get_vector(self, vector_id):
        """
        Retrieve a vector from the store.

        Args:
            vector_id (str or int): The identifier of the vector to retrieve.

        Returns:
            numpy.ndarray: The vector data if found, or None if not found.
        """
        return self.vector_data.get(vector_id)

    def _update_index(self, vector_id, vector):
        """
        Update the index with the new vector.

        Args:
            vector_id (str or int): The identifier of the vector.
            vector (numpy.ndarray): The vector data.
        """
        # In this simple example, we use brute-force cosine similarity for indexing
        for existing_id, existing_vector in self.vector_data.items():
            similarity = np.dot(vector, existing_vector) / (np.linalg.norm(vector) * np.linalg.norm(existing_vector))
            if existing_id not in self.vector_index:
                self.vector_index[existing_id] = {}
            self.vector_index[existing_id][vector_id] = similarity

    def find_similar_vectors(self, query_vector, num_results=5):
        """
        Find similar vectors to the query vector using brute-force search.

        Args:
            query_vector (numpy.ndarray): The query vector for similarity search.
            num_results (int): The number of similar vectors to return.

        Returns:
            list: A list of (vector_id, similarity_score) tuples for the most similar vectors.
        """
        results = []
        for vector_id, vector in self.vector_data.items():
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            results.append((vector_id, similarity))

        # Sort by similarity in descending order
        results.sort(key=lambda x: x[1], reverse=True)

        # Return the top N results
        return results[:num_results]
