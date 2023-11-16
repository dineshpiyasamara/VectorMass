import VectorMass
import numpy as np

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

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

collection = vector_store.create_or_get_collection("coll_name")
print(collection.collection_name)

ids = ['id1', 'id2', 'id3', 'id4']
print(ids)
print(sentences)

collection.add(
    ids= ids,
    documents=sentences
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

# result = collection.delete(['id1', 'id3'])
# print(result)

# result = collection.get_all()
# print(result)

# # Storing in VectorStore
# for sentence, vector in sentence_vectors.items():
#     vector_store.add_vector(sentence, vector)

# # Searching for Similarity
# query_sentence = "Mango is the best fruit"
# query_vector = np.zeros(len(vocabulary))
# query_tokens = query_sentence.lower().split()
# for token in query_tokens:
#     if token in word_to_index:
#         query_vector[word_to_index[token]] += 1

# similar_sentences = vector_store.find_similar_vectors(query_vector, num_results=2)

# # Print similar sentences
# print("Query Sentence:", query_sentence)
# print("Similar Sentences:")
# for sentence, similarity in similar_sentences:
#     print(f"{sentence}: Similarity = {similarity:.4f}")