from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from PIL import Image
import base64
import io


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


def process_image(file_path: str, user_prompt: str):

    # Open image
    image = Image.open(file_path)

    # Get image dimensions
    width, height = image.size

    # Convert image to base64
    buffer = io.BytesIO()
    image.save(buffer, format=image.format or "PNG")

    image_data = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    # User prompt + image information
    prompt = f"""
You are an AI vision assistant.

Image Dimensions:
Width: {width}
Height: {height}

User Question:
{user_prompt}

Answer only according to the user's question.
If the user asks for image description, describe it.
If the user asks for OCR, extract the text.
If there is no text, say:
'No text detected in the image.'
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