from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from PIL import Image
import base64
import io


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


def process_image(
    file_path: str,
    user_prompt: str,
    messages: list
):

    image = Image.open(file_path)

    width, height = image.size

    buffer = io.BytesIO()
    image.save(buffer, format=image.format or "PNG")

    image_data = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    history = ""

    for msg in messages[:-1]:
        role = msg["role"].capitalize()
        history += f"{role}: {msg['content']}\n"

    prompt = f"""
You are an AI vision assistant.

Use the previous conversation to understand follow-up questions.

Previous Conversation:
{history}

Image Information:
Width: {width}
Height: {height}

Current User Question:
{user_prompt}

Instructions:
- Answer based on the uploaded image.
- Use previous conversation if the current question is a follow-up.
- If the user asks for an image description, describe the image.
- If the user asks for OCR, extract all visible text.
- If no text exists, reply:
  'No text detected in the image.'
- Do not make up details that are not visible in the image.
"""

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/{image.format or 'png'};base64,{image_data}"
                }
            }
        ]
    )

    response = model.invoke([message])

    return response.content

    