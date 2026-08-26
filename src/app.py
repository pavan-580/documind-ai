import os

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from pdf_reader import extract_text_from_pdf
from chunker import create_chunks
from retriever import retrieve, rebuild_index
from llm import generate_answer


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

UPLOAD_FOLDER = "../documents"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

# Track whether a document has been loaded
document_loaded = False


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    global document_loaded

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Please select a PDF."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Only PDF files are allowed."
        }), 400

    filename = secure_filename(file.filename)

    base_dir = os.path.dirname(os.path.dirname(__file__))

    upload_folder = os.path.join(
        base_dir,
        "documents"
    )

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(
        upload_folder,
        filename
    )

    try:

        file.save(filepath)

        # Extract text
        pages = extract_text_from_pdf(filepath)

        if not pages:
            return jsonify({
                "success": False,
                "message": "Could not extract text from this PDF."
            }), 400

        # Create chunks
        chunks = create_chunks(pages)

        if not chunks:
            return jsonify({
                "success": False,
                "message": "No usable text was found in this PDF."
            }), 400

        # Replace the current FAISS index
        rebuild_index(chunks)

        document_loaded = True

        return jsonify({
            "success": True,
            "message": f"{filename} uploaded successfully.",
            "chunks": len(chunks)
        })

    except Exception as e:

        print("Upload error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to process the PDF."
        }), 500


@app.route("/ask", methods=["POST"])
def ask():

    if not document_loaded:

        return jsonify({
            "answer": "Please upload a PDF before asking a question.",
            "sources": []
        })

    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()

    if not question:

        return jsonify({
            "answer": "Please enter a question.",
            "sources": []
        })

    try:

        # Retrieve relevant chunks
        results = retrieve(question)

        # No relevant information
        if not results:

            return jsonify({
                "answer": "I could not find the answer in the provided document.",
                "sources": []
            })

        # Build context
        context = "\n\n".join(
            result["text"]
            for result in results
        )

        # Generate answer
        answer = generate_answer(
            context,
            question
        )

        # Sources
        sources = sorted(
            set(result["page"] for result in results)
        )

        return jsonify({
            "answer": answer,
            "sources": sources
        })

    except Exception as e:

        print("Question error:", e)

        return jsonify({
            "answer": "Something went wrong while processing your question.",
            "sources": []
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
