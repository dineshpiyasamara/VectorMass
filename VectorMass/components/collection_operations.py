import numpy as np
from VectorMass.queries.queries import *
from VectorMass.config.configuration import ConfigurationManager
from sentence_transformers import SentenceTransformer
import ast

config_manager = ConfigurationManager()
config = config_manager.embedding_config()

model = SentenceTransformer(config.default_embedding_model)

class Collection:
    def __init__(self, conn, cursor, collection_name):
        self.conn = conn
        self.cursor = cursor
        self.collection_name = collection_name

        print(self.conn, self.cursor, self.collection_name)

    def add(self, ids, documents, embeddings=None):
        if embeddings == None:
            embeddings = model.encode(documents)

        for i in range(len(ids)):
            id = f"'{ids[i]}'"
            document = f"'{documents[i]}'"
            embedding = f"'{list(embeddings[i])}'"

            query_to_check_exist = CHECK_ID_EXIST.format(self.collection_name, id)
            check_exist = self.cursor.execute(query_to_check_exist).fetchone()[0]

            if check_exist > 0:
                print(f"{id} already exist")
            else:
                query = INSERT_RECORD.format(self.collection_name, id, document, embedding)
                print(query)
                self.cursor.execute(query)

        self.conn.commit()
        print("Done.")


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
    
    def get_one(self, id):
        result = dict()
        id = f"'{id}'"
        query = GET_RECORD.format(self.collection_name, id)
        row = self.cursor.execute(query).fetchall()

        item_id, item_document, item_embedding = row[0][0], row[0][1], ast.literal_eval(row[0][2])

        result['id'] = item_id
        result['document'] = item_document
        result['embedding'] = item_embedding

        return result
    
    def get_all(self):
        result = {
            'ids': [],
            'documents': [],
            'embeddings': []
        }

        query = GET_ALL_RECORDS.format(self.collection_name)
        print(query)
        rows = self.cursor.execute(query).fetchall()
        
        for row in rows:
            item_id, item_document, item_embedding = row[0], row[1], ast.literal_eval(row[2])
            result['ids'].append(item_id)
            result['documents'].append(item_document)
            result['embeddings'].append(item_embedding)

        return result
    
    def update(self, ids, documents, embeddings=None):
        if embeddings == None:
            embeddings = model.encode(documents)
            
        for i in range(len(ids)):
            id = f"'{ids[i]}'"
            document = f"'{documents[i]}'"
            embedding = f"'{list(embeddings[i])}'"

            query_to_check_exist = CHECK_ID_EXIST.format(self.collection_name, id)
            check_exist = self.cursor.execute(query_to_check_exist).fetchone()[0]

            if check_exist > 0:
                query = UPDATE_RECORD.format(self.collection_name, document, embedding, id)
                print(query)
                self.cursor.execute(query)
            else:
                print(f"Unable to find {id}")

        self.conn.commit()
        print("Done.")

    def delete(self, ids):
        for i in range(len(ids)):
            id = f"'{ids[i]}'"

            query_to_check_exist = CHECK_ID_EXIST.format(self.collection_name, id)
            check_exist = self.cursor.execute(query_to_check_exist).fetchone()[0]

            if check_exist > 0:
                query = DELETE_RECORD.format(self.collection_name, id)
                print(query)
                self.cursor.execute(query)
            else:
                print(f"Unable to find {id}")       

        self.conn.commit()
        print("Done.")