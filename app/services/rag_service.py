from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful AI assistant.

Use only the following context to answer the user's question.

Context:
{context}

If the answer is not present in the context, say:
"I don't know."
"""
    ),
    (
        "human",
        "{question}"
    )
])

def generate_answer(context, question):
    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    response = model.invoke(messages)
    return response.content