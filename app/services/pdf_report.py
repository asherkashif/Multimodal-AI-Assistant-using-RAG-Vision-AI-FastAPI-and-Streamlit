from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_chat_report(messages):

    os.makedirs("reports", exist_ok=True)

    output_path = "reports/conversation_report.pdf"

    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Multimodal AI Assistant Report",
            styles["Title"]
        )
    )

    for msg in messages:

        story.append(
            Paragraph(
                f"<b>{msg['role'].capitalize()}:</b> {msg['content']}",
                styles["BodyText"]
            )
        )

    doc.build(story)

    return output_path