from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from PIL import Image
import base64
import io


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


def process_image(file_path: str):

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


    prompt = """
You are an AI assistant that processes images.

Analyze this image and provide:

1. Image description
2. Image dimensions
3. Suggested improvements or edits
4. Object detection (all visible objects)
5. Any visible text in the image
6. Important features or elements

If there is no text in the image, say:
"No text detected in the image."
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
                    "url": f"data:image/{image.format};base64,{image_data}"
                }
            }
        ]
    )


    response = model.invoke([message])


    return {
        "filename": file_path,
        "dimensions": f"{width}x{height}",
        "analysis": response.content
    }