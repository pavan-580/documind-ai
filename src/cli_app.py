from retriever import retrieve
from llm import generate_answer


def rewrite_question(question, conversation_history):

    if not conversation_history:
        return question

    previous_question = conversation_history[-1]["question"]

    follow_up_phrases = [
        "what about",
        "how many",
        "how much",
        "how long",
        "when",
        "where",
        "can",
        "does",
        "do",
        "is",
        "are",
        "carry",
        "carried"
    ]

    question_lower = question.lower().strip()

    # Only combine when it looks like a follow-up
    if any(
        question_lower.startswith(phrase)
        for phrase in follow_up_phrases
    ):

        return (
            f"{previous_question}. "
            f"Follow-up question: {question}"
        )

    return question

def main():

    print("\n===== RAG Q&A SYSTEM =====")
    print("Type 'exit' to quit.\n")

    conversation_history = []

    while True:

        question = input("Ask a question: ")

        if question.lower() == "exit":
            break

        # Rewrite question using previous conversation
        search_question = rewrite_question(
            question,
            conversation_history
        )

        # Retrieve relevant chunks
        results = retrieve(search_question)

        if not results:

            print("\n--- AI Answer ---")
            print(
                "I could not find the answer in the provided document."
            )

            print("\n--- Sources ---")
            print("No relevant source found.")

            continue

        # Create document context
        context = "\n\n".join(
            result["text"]
            for result in results
        )

        # Add recent conversation to LLM context
        history = "\n".join(
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}"
            for item in conversation_history[-3:]
        )

        full_context = f"""
CONVERSATION HISTORY:

{history}

DOCUMENT CONTEXT:

{context}
"""

        # Generate answer
        answer = generate_answer(
            full_context,
            question
        )

        print("\n--- AI Answer ---")
        print(answer)

        # Save conversation
        conversation_history.append({
            "question": question,
            "answer": answer
        })

        # Show sources
        print("\n--- Sources ---")

        pages = sorted(
            set(result["page"] for result in results)
        )

        for page in pages:
            print(f"Page {page}")

        print()


if __name__ == "__main__":
    main()


# from retriever import retrieve
# from llm import generate_answer


# def main():

#     print("\n===== RAG Q&A SYSTEM =====")
#     print("Type 'exit' to quit.\n")

#     conversation_history = []

#     while True:

#         question = input("Ask a question: ")

#         if question.lower() == "exit":
#             break

#         # Retrieve relevant document chunks
#         results = retrieve(question)

#         if not results:

#             print("\n--- AI Answer ---")
#             print("I could not find the answer in the provided document.")
#             print("\n--- Sources ---")
#             print("No relevant source found.")
#             continue

#         # Create document context
#         context = "\n\n".join(
#             result["text"]
#             for result in results
#         )

#         # Add previous conversation
#         history = "\n".join(
#             f"User: {item['question']}\n"
#             f"Assistant: {item['answer']}"
#             for item in conversation_history[-3:]
#         )

#         # Combine history + document context
#         full_context = f"""
# CONVERSATION HISTORY:

# {history}

# DOCUMENT CONTEXT:

# {context}
# """

#         # Generate answer
#         answer = generate_answer(
#             full_context,
#             question
#         )

#         print("\n--- AI Answer ---")
#         print(answer)

#         # Save conversation
#         conversation_history.append({
#             "question": question,
#             "answer": answer
#         })

#         # Show sources
#         print("\n--- Sources ---")

#         pages = sorted(
#             set(result["page"] for result in results)
#         )

#         for page in pages:
#             print(f"Page {page}")

#         print()


# if __name__ == "__main__":
#     main()



# from retriever import retrieve
# from llm import generate_answer


# def main():

#     print("\n===== RAG Q&A SYSTEM =====")
#     print("Type 'exit' to quit.\n")

#     conversation_history = []

#     while True:

#         question = input("Ask a question: ")

#         if question.lower() == "exit":
#             break

#         # Retrieve relevant chunks
#         results = retrieve(question)

#         # Create document context
#         context = "\n\n".join(
#             result["text"] for result in results
#         )

#         # Add previous conversation to the prompt
#         history = "\n".join(
#             f"User: {q}\nAssistant: {a}"
#             for q, a in conversation_history
#         )

#         if history:
#             enhanced_question = f"""
# Previous conversation:
# {history}

# Current question:
# {question}
# """
#         else:
#             enhanced_question = question

#         # Generate answer
#         answer = generate_answer(context, enhanced_question)

#         print("\n--- AI Answer ---")
#         print(answer)

        
#         # Show sources
#         print("\n--- Sources ---")

#         if results:

#             pages = sorted(set(result["page"] for result in results))

#             for page in pages:
#                 print(f"Page {page}")

#         else:

#             print("No relevant source found.")
#         # # Show sources
#         # print("\n--- Sources ---")

#         # pages = sorted(set(result["page"] for result in results))

#         # if pages:
#         #     for page in pages:
#         #         print(f"Page {page}")
#         # else:
#         #     print("No relevant source found.")

#         # Save conversation
#         conversation_history.append((question, answer))

#         print()


if __name__ == "__main__":
    main()



# from retriever import retrieve
# from llm import generate_answer


# def main():

#     print("\n===== RAG Q&A SYSTEM =====")
#     print("Type 'exit' to quit.\n")

#     while True:

#         question = input("Ask a question: ")

#         if question.lower() == "exit":
#             break

#         # Retrieve relevant chunks
#         results = retrieve(question)

#         # Create context for LLM
#         context = "\n\n".join(
#             result["text"] for result in results
#         )

#         # Generate answer
#         answer = generate_answer(context, question)

#         print("\n--- AI Answer ---")
#         print(answer)

#         # Show sources
#         print("\n--- Sources ---")

#         pages = sorted(set(result["page"] for result in results))

#         if pages:
#             for page in pages:
#                 print(f"Page {page}")
#         else:
#             print("No relevant source found.")
            
#         # pages = sorted(set(result["page"] for result in results))

#         # for page in pages:
#         #     print(f"Page {page}")

#         print()


# if __name__ == "__main__":
#     main()



# from retriever import retrieve
# from llm import generate_answer


# def main():

#     print("\n===== RAG Q&A SYSTEM =====")
#     print("Type 'exit' to quit.\n")

#     while True:

#         question = input("Ask a question: ")

#         if question.lower() == "exit":
#             break

#         context = retrieve(question)

#         answer = generate_answer(context, question)

#         print("\n--- AI Answer ---")
#         print(answer)
#         print()


# if __name__ == "__main__":
#     main()