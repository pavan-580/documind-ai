from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Our document sentence
document_text = "Employees receive 24 days of annual leave per calendar year."

# Two questions
related_question = "How many annual leave days do employees get?"
unrelated_question = "What are the standard working hours?"

# Generate embeddings
document_embedding = model.encode([document_text])
related_embedding = model.encode([related_question])
unrelated_embedding = model.encode([unrelated_question])

# Calculate similarity
related_score = cosine_similarity(
    document_embedding,
    related_embedding
)[0][0]

unrelated_score = cosine_similarity(
    document_embedding,
    unrelated_embedding
)[0][0]

print("\n--- Semantic Similarity Test ---")

print("\nDocument:")
print(document_text)

print("\nRelated Question:")
print(related_question)
print("Similarity Score:", round(related_score, 4))

print("\nUnrelated Question:")
print(unrelated_question)
print("Similarity Score:", round(unrelated_score, 4))



# from sentence_transformers import SentenceTransformer

# # Load the local embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# text = "Employees receive 24 days of annual leave per calendar year."

# # Convert text into an embedding
# embedding = model.encode(text)

# print("Embedding generated successfully!")
# print("Vector length:", len(embedding))
# print("First 10 values:", embedding[:10])


# open ai once
# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# text = "Employees receive 24 days of annual leave per calendar year."

# response = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=text
# )

# embedding = response.data[0].embedding

# print("Embedding generated successfully!")
# print("Vector length:", len(embedding))
# print("First 10 values:", embedding[:10])