from sentence_transformers import SentenceTransformer
import faiss

from pdf_reader import extract_text_from_pdf
from chunker import create_chunks


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Global variables
chunks = []
index = None


def rebuild_index(new_chunks):

    global chunks
    global index

    chunks = new_chunks

    # Get text from chunks
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # Generate embeddings
    embeddings = model.encode(texts)

    # FAISS requires float32
    embeddings = embeddings.astype("float32")

    # Create FAISS index
    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    # Add vectors
    index.add(embeddings)

    print(
        f"FAISS index rebuilt: {len(chunks)} chunks"
    )


def load_default_document():

    pages = extract_text_from_pdf(
        "documents/sample.pdf"
    )

    default_chunks = create_chunks(pages)

    rebuild_index(default_chunks)


def retrieve(question, top_k=3):

    if index is None or not chunks:

        return []

    # Question embedding
    question_embedding = model.encode(
        [question]
    ).astype("float32")

    # Search
    distances, indices = index.search(
        question_embedding,
        top_k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx < 0:
            continue

        results.append({
            "text": chunks[idx]["text"],
            "page": chunks[idx]["page"],
            "distance": float(distance)
        })

    return results


# Load sample PDF when application starts
load_default_document()


if __name__ == "__main__":

    question = "How many annual leave days do employees get?"

    results = retrieve(question)

    print("\n--- Retrieved Context ---")

    for i, result in enumerate(results):

        print(f"\nResult {i + 1}")
        print(f"Page: {result['page']}")
        print(
            f"Distance: {result['distance']:.4f}"
        )
        print(
            f"Text: {result['text']}"
        )

# from sentence_transformers import SentenceTransformer
# import faiss

# from pdf_reader import extract_text_from_pdf
# from chunker import create_chunks


# # Load embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")


# # Load document
# pages = extract_text_from_pdf("documents/sample.pdf")

# # Create chunks
# chunks = create_chunks(pages)

# # Generate embeddings
# texts = [chunk["text"] for chunk in chunks]

# embeddings = model.encode(
#     texts,
#     normalize_embeddings=True
# )

# embeddings = embeddings.astype("float32")


# # Create FAISS cosine-similarity index
# index = faiss.IndexFlatIP(embeddings.shape[1])

# index.add(embeddings)


# def retrieve(question, top_k=2, threshold=0.35):

#     # Convert question to embedding
#     question_embedding = model.encode(
#         [question],
#         normalize_embeddings=True
#     ).astype("float32")

#     # Search
#     scores, indices = index.search(
#         question_embedding,
#         top_k
#     )

#     results = []

#     for score, idx in zip(scores[0], indices[0]):

#         # Ignore irrelevant chunks
#         if score < threshold:
#             continue

#         results.append({
#             "text": chunks[idx]["text"],
#             "page": chunks[idx]["page"],
#             "score": float(score)
#         })

#     return results


# if __name__ == "__main__":

#     question = "How many annual leave days do employees get?"

#     results = retrieve(question)

#     print("\n--- Retrieved Context ---")

#     for i, result in enumerate(results):

#         print(f"\nResult {i + 1}")
#         print(f"Page: {result['page']}")
#         print(f"Similarity: {result['score']:.4f}")
#         print(f"Text: {result['text']}")


# from sentence_transformers import SentenceTransformer
# import faiss

# from pdf_reader import extract_text_from_pdf
# from chunker import create_chunks


# # Load embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")


# # Load document
# pages = extract_text_from_pdf("documents/sample.pdf")

# # Create chunks
# chunks = create_chunks(pages)


# # Generate embeddings for all chunks
# texts = [chunk["text"] for chunk in chunks]

# embeddings = model.encode(texts)

# # Convert to float32 for FAISS
# embeddings = embeddings.astype("float32")


# # Create FAISS index
# index = faiss.IndexFlatL2(embeddings.shape[1])

# index.add(embeddings)

# def retrieve(question, top_k=3, threshold=1.0):
# # def retrieve(question, top_k=3):

#     # Convert question into embedding
#     question_embedding = model.encode([question]).astype("float32")

#     # Search FAISS
#     distances, indices = index.search(
#         question_embedding,
#         top_k
#     )

#     results = []

#     for distance, idx in zip(distances[0], indices[0]):

#         if distance <= threshold:
#             results.append({
#                 "text": chunks[idx]["text"],
#                 "page": chunks[idx]["page"],
#                 "distance": float(distance)
#             })
#     # for distance, idx in zip(distances[0], indices[0]):

#     #     results.append({
#     #         "text": chunks[idx]["text"],
#     #         "page": chunks[idx]["page"],
#     #         "distance": float(distance)
#     #     })

#     return results


# if __name__ == "__main__":

#     question = "How many annual leave days do employees get?"

#     results = retrieve(question)

#     print("\n--- Retrieved Context ---")

#     for i, result in enumerate(results):

#         print(f"\nResult {i + 1}")
#         print(f"Page: {result['page']}")
#         print(f"Distance: {result['distance']:.4f}")
#         print(f"Text: {result['text']}")