import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def create_chunks(pages, chunk_size=500, chunk_overlap=50):

    chunks = []

    for page in pages:

        text = clean_text(page["text"])

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "page": page["page"]
            })

            start += chunk_size - chunk_overlap

    return chunks

if __name__ == "__main__":

    from pdf_reader import extract_text_from_pdf

    pages = extract_text_from_pdf("documents/sample.pdf")

    chunks = create_chunks(pages)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        print(f"\n--- Chunk {i + 1} ---")
        print(f"Page: {chunk['page']}")
        print(chunk["text"])