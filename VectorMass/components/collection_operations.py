import numpy as np
from VectorMass.queries.queries import *
from VectorMass.config.configuration import ConfigurationManager
import ast

class Collection:
    def __init__(self, conn, cursor, collection_name):
        self.conn = conn
        self.cursor = cursor
        self.collection_name = collection_name

        print(self.conn, self.cursor, self.collection_name)

    def add(self, ids, embeddings, documents):
        for i in range(len(ids)):
            id = f"'{ids[i]}'"
            document = f"'{documents[i]}'"
            embedding = f"'{list(embeddings[i])}'"
            print(id, document, embedding)
            print(type(id), type(document), type(embedding))
            query = INSERT_RECORD.format(self.collection_name, id, document, embedding)
            print(query)
            self.cursor.execute(query)

        self.conn.commit()
        print("Data inserted.")

    def get(self, ids):
        result = {
            'ids': [],
            'documents': [],
            'embeddings': []
        }
        for i in range(len(ids)):
            id = f"'{ids[i]}'"
            query = GET_RECORD.format(self.collection_name, id)
            print(query)
            row = self.cursor.execute(query).fetchall()
            print(row[0][2])
            print(type(row[0][2]))
            
            item_id, item_document, item_embedding = row[0][0], row[0][1], ast.literal_eval(row[0][2])
            result['ids'].append(item_id)
            result['documents'].append(item_document)
            result['embeddings'].append(item_embedding)

        return result

