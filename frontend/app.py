import streamlit as st
import requests

st.set_page_config(
    page_title="Multimodal AI Assistant",
    page_icon="🤖",
    layout="wide"
)



# ---------------- Chat History ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- Sidebar ----------------
st.sidebar.title("Navigation")

option = st.sidebar.selectbox(
    "Choose",
    [
        "Home",
        "Chat",
        "Upload Documents",
        "Upload Images",
        "Generate Report"
    ]
)

st.write("Selected:", option)
if option == "Home":
    st.title("🤖 Multimodal AI Assistant")
    st.write("Welcome to the Multimodal AI Assistant!")

elif option == "Chat":
    # Chat UI
    pass

elif option == "Upload Documents":
    # PDF Upload
    pass

elif option == "Upload Images":
    # Image Upload
    pass

elif option == "Generate Report":
    # Report Generation
    st.header("Generate Conversation Report")

    if st.button("Generate PDF Report"):

        response = requests.post(
            "http://127.0.0.1:8000/generate-report",
            json={
                "messages": st.session_state.messages
            }
        )

        if response.status_code == 200:

            st.download_button(
                "Download PDF",
                data=response.content,
                file_name="conversation_report.pdf",
                mime="application/pdf"
            )

        else:
            st.error("Failed to generate report.")
# ---------------- Upload ----------------
uploaded_file = st.file_uploader(
    "Upload a file",
    type=["pdf", "jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type,
        )
    }

    if st.button("Upload"):

        with st.spinner("Uploading..."):

            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files
            )

        data = response.json()

        st.success(data["message"])

        # Image Preview
        if uploaded_file.type.startswith("image"):
            st.image(
                uploaded_file,
                caption=uploaded_file.name,
                use_container_width=True
            )

        # PDF Info
        elif uploaded_file.type == "application/pdf":
            st.success(
                f"Vector Store Created ({data['chunks']} chunks)"
            )

# ---------------- Chat ----------------
question = st.chat_input("Ask anything...")

if question:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Thinking..."):

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={
                "question": question
            }
        )

        answer = response.json()["answer"]

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.write(answer)