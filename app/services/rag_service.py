from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful AI assistant.

Answer ONLY from the provided context.

Context:
{context}

If the answer is not in the context, reply exactly:
"I don't know."
"""
    ),
    (
        "human",
        "{question}"
    )
])


def generate_answer(context: list[str], question: str):
    """
    Generate answer using retrieved context.
    """

    # Convert list of chunks into one string
    context_text = "\n\n".join(context)

    messages = prompt.invoke({
        "context": context_text,
        "question": question
    })

    response = model.invoke(messages)

    return response.content