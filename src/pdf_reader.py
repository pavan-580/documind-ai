import pymupdf

def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        pages.append({
            "page": page_number + 1,
            "text": text
        })

    document.close()

    return pages

if __name__ == "__main__":
    pages = extract_text_from_pdf("documents/sample.pdf")

    for page in pages:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"])

# import pymupdf

# pdf_path = "documents/sample.pdf"

# document = pymupdf.open(pdf_path)

# for page_number, page in enumerate(document):
#     text = page.get_text()

#     print(f"\n--- Page {page_number + 1} ---")
#     print(text)

# document.close()