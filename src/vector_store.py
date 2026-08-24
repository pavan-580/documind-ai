import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from chunker import create_chunks
from pdf_reader import extract_text_from_pdf


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store(chunks):
    """
    Convert document chunks into embeddings
    and store them in FAISS.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_documents(question, index, chunks, top_k=3):
    """
    Search FAISS for chunks relevant to the question.
    """

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(
        question_embedding,
        top_k
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        results.append({
            "text": chunks[idx]["text"],
            "page": chunks[idx]["page"],
            "distance": float(distance)
        })

    return results


if __name__ == "__main__":

    pages = extract_text_from_pdf(
        "documents/sample.pdf"
    )

    chunks = create_chunks(pages)

    print(f"Total chunks: {len(chunks)}")

    index = build_vector_store(chunks)

    print(f"Vectors stored in FAISS: {index.ntotal}")

    question = "How many annual leave days do employees get?"

    results = search_documents(
        question,
        index,
        chunks,
        top_k=3
    )

    print("\n--- Search Results ---")

    for i, result in enumerate(results):

        print(f"\nResult {i + 1}")
        print(f"Page: {result['page']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Text: {result['text']}")


# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# from chunker import create_chunks
# from pdf_reader import extract_text_from_pdf


# # --------------------------------
# # 1. Load PDF and create chunks
# # --------------------------------

# pages = extract_text_from_pdf("documents/sample.pdf")

# chunks = create_chunks(
#     pages,
#     chunk_size=500,
#     chunk_overlap=50
# )

# print("Total chunks:", len(chunks))


# # --------------------------------
# # 2. Load embedding model
# # --------------------------------

# model = SentenceTransformer("all-MiniLM-L6-v2")


# # --------------------------------
# # 3. Create embeddings
# # --------------------------------

# texts = [chunk["text"] for chunk in chunks]

# embeddings = model.encode(
#     texts,
#     convert_to_numpy=True
# )

# print("Embedding shape:", embeddings.shape)


# # --------------------------------
# # 4. Create FAISS index
# # --------------------------------

# dimension = embeddings.shape[1]

# index = faiss.IndexFlatL2(dimension)

# index.add(embeddings.astype("float32"))

# print("Vectors stored in FAISS:", index.ntotal)


# # --------------------------------
# # 5. Ask a question
# # --------------------------------

# question = "How many annual leave days do employees receive?"

# question_embedding = model.encode(
#     [question],
#     convert_to_numpy=True
# )

# question_embedding = question_embedding.astype("float32")


# # --------------------------------
# # 6. Search FAISS
# # --------------------------------

# k = 3

# distances, indices = index.search(
#     question_embedding,
#     k
# )


# # --------------------------------
# # 7. Display results
# # --------------------------------

# print("\n--- Search Results ---")

# for rank, (distance, index_id) in enumerate(
#     zip(distances[0], indices[0]),
#     start=1
# ):

#     chunk = chunks[index_id]

#     print(f"\nResult {rank}")
#     print("Page:", chunk["page"])
#     print("Distance:", round(float(distance), 4))
#     print("Text:")
#     print(chunk["text"])