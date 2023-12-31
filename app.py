import VectorMass
import numpy as np

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

# Create a VectorStore instance
vector_store = VectorMass.Client()


# =========================================================================

# Define your sentences
sentences = [
    "I eat mango",
    "mango is my favorite fruit",
    "mango, apple, oranges are fruits",
    "fruits are good for health",
]

# embeddings = model.encode(sentences)
# print(embeddings)
# print(type(embeddings[0]))

collection = vector_store.create_or_get_collection("collection_one")
print(collection.collection_name)

ids = ['id1', 'id2', 'id3', 'id4']
print(ids)
print(sentences)

collection.add(
    ids= ids,
    documents=sentences,
    embedding_model=model
)

# collection.update(
#     ids = ['id2'],
#     embeddings=[[0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]],
#     documents= ['i am dinesh']
# )


# ids = ['id2', 'id4']
# res = collection.get(ids)
# print(type(res['embeddings'][0]))
# print(res)

# res = collection.get_one('id2')
# print(res)

result = collection.get_all()
print(result)

# result = collection.delete(['id1', 'id3', 'id2', 'id4'])
# print(result)

# result = collection.get_all()
# print(result)

res = model.encode(['healthy foods', 'I eat mango'])

print("===========================")
result = collection.query(query_embeddings=res)
print(result)