import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not configured")

client = InferenceClient(
    api_key=HF_TOKEN
)


def generate_answer(context, question):

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question ONLY using the provided document context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided document."

Do not invent information.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(
        model="google/gemma-3-12b-it",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300,
        temperature=0.1
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    context = """
    Full-time employees receive 24 days of annual leave
    per calendar year.
    """

    question = "How many annual leave days do employees get?"

    answer = generate_answer(context, question)

    print("\n--- AI Answer ---")
    print(answer)