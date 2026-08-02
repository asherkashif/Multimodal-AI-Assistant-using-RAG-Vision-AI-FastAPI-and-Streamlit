from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Use the previous conversation to understand the context.

Answer ONLY from the provided document context.

Previous Conversation:
{history}

Document Context:
{context}

If the answer exists in the document, answer using the document.

If the user asks a follow-up question that depends on previous conversation, use the conversation history.

If the answer is not available in the document or previous conversation, reply exactly:

"I don't know."
"""
        ),
        (
            "human",
            "{question}"
        )
    ]
)


def generate_answer(
    context: list[str],
    question: str,
    messages: list
):

    context_text = "\n\n".join(context)

    history = ""

    for msg in messages[:-1]:
        role = msg["role"].capitalize()
        history += f"{role}: {msg['content']}\n"

    prompt_messages = prompt.invoke(
        {
            "history": history,
            "context": context_text,
            "question": question
        }
    )

    response = model.invoke(prompt_messages)

    return response.content