import numpy as np
from VectorMass.queries.queries import *
from VectorMass.config.configuration import ConfigurationManager
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import ast

config_manager = ConfigurationManager()
config = config_manager.embedding_config()

class Collection:
    def __init__(self, conn, cursor, collection_name):
        self.conn = conn
        self.cursor = cursor
        self.collection_name = collection_name

        print(self.conn, self.cursor, self.collection_name)

    def add(self, ids, documents, embeddings=None, embedding_model=None):
        if embeddings == None:
            if embedding_model == None:
                embedding_model = SentenceTransformer(config.default_embedding_model)
            embeddings = embedding_model.encode(documents)

        for i in range(len(ids)):
            id = f"'{ids[i]}'"
            document = f"'{documents[i]}'"
            embedding = f"'{list(embeddings[i])}'"

            query_to_check_exist = CHECK_ID_EXIST ,(self.collection_name, id, )
            print(query_to_check_exist)
            check_exist = self.cursor.execute(query_to_check_exist).fetchone()[0]

            if check_exist > 0:
                print(f"{id} already exist")
            else:
                query = INSERT_RECORD , (self.collection_name, id, document, embedding,)
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
            query = GET_RECORD, (self.collection_name, id,)
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
        query = GET_RECORD, (self.collection_name, id,)
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

        query = GET_ALL_RECORDS , (self.collection_name,)
        print(query)
        rows = self.cursor.execute(query).fetchall()
        
        for row in rows:
            item_id, item_document, item_embedding = row[0], row[1], ast.literal_eval(row[2])
            result['ids'].append(item_id)
            result['documents'].append(item_document)
            result['embeddings'].append(item_embedding)

        return result
    
    def update(self, ids, documents, embeddings=None, embedding_model=None):
        if embeddings == None:
            if embedding_model == None:
                embedding_model = SentenceTransformer(config.default_embedding_model)
            embeddings = embedding_model.encode(documents)

        for i in range(len(ids)):
            id = f"'{ids[i]}'"
            document = f"'{documents[i]}'"
            embedding = f"'{list(embeddings[i])}'"

            query_to_check_exist = CHECK_ID_EXIST ,(self.collection_name, id,)
            check_exist = self.cursor.execute(query_to_check_exist).fetchone()[0]

            if check_exist > 0:
                query = UPDATE_RECORD ,(self.collection_name, document, embedding, id,)
                print(query)
                self.cursor.execute(query)
            else:
                print(f"Unable to find {id}")

        self.conn.commit()
        print("Done.")


    def delete(self, ids):
        for i in range(len(ids)):
            id = f"'{ids[i]}'"

            query_to_check_exist = CHECK_ID_EXIST ,(self.collection_name, id,)
            check_exist = self.cursor.execute(query_to_check_exist).fetchone()[0]

            if check_exist > 0:
                query = DELETE_RECORD, (self.collection_name, id,)
                print(query)
                self.cursor.execute(query)
            else:
                print(f"Unable to find {id}")       

        self.conn.commit()
        print("Done.")


    def query(self, query_documents=None, query_embeddings=None, num_results=2):
        result = {
            'ids': [],
            'documents': [],
            'distances': [] 
        }
        if query_embeddings is not None:
            results = self.get_all()
            embeddings = results['embeddings']

            ids = results['ids']
            documents = results['documents']

            similarities_list = []
            for query_embedding in query_embeddings:
                similarities = [1 - cosine_similarity([query_embedding], [embedding]) for embedding in embeddings]
                similarities_list.append(similarities)
            
            for similarities in similarities_list:
                print(similarities)
                values = [arr[0][0] for arr in similarities]
                indices = np.argsort(values)[::1][:num_results]  # Indices of maximum two values in descending order

                temp_ids = []
                temp_documents = []
                temp_distances = []

                for i in indices:
                    temp_ids.append(ids[i])
                    temp_documents.append(documents[i])
                    temp_distances.append(similarities[i])
                
                result['ids'].append(temp_ids)
                result['documents'].append(temp_documents)
                result['distances'].append(temp_distances)
        return result



