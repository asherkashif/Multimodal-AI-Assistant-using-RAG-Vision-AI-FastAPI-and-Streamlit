import streamlit as st
import requests

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Multimodal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================
# Session State
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = []


if "token" not in st.session_state:
    st.session_state.token = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================
# Sidebar
# ==========================
st.sidebar.title("🤖 Multimodal AI Assistant")

if st.session_state.logged_in:

    option = st.sidebar.selectbox(
        "Navigation",
        [
            "Home",
            "Chat",
            "Upload Documents",
            "Upload Images",
            "Generate Report",
        ]
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.token = None
        st.session_state.messages = []

        st.rerun()

else:

    option = st.sidebar.selectbox(
        "Navigation",
        [
            "Login",
            "Signup"
        ]
    )

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ==========================
# Home
# ==========================
if option == "Home":

    st.title("🤖 Multimodal AI Assistant")
    st.write(
        """
Welcome to your Multimodal AI Assistant.

Features:
- 💬 Chat with AI
- 📄 Upload PDF documents
- 🖼️ Analyze Images
- 📑 Generate PDF Reports
"""
    )

# ==========================
# Chat
# ==========================
elif option == "Chat":

    st.title("💬 Chat Assistant")

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask anything...")

    if question:

        # Save User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        try:

            with st.spinner("Thinking..."):

                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                    }

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    headers=headers,
                    json={
                        "question": question,
                        "messages": st.session_state.messages
                    }
                )

                response.raise_for_status()

                answer = response.json()["answer"]

        except requests.exceptions.RequestException as e:

            answer = f"❌ API Error:\n{e}"

        # Save Assistant Message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)

# ==========================
# Upload Documents
# ==========================
elif option == "Upload Documents":

    st.title("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Select PDF",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button("Upload PDF"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            try:

                with st.spinner("Uploading PDF..."):

                    headers = {
                            "Authorization": f"Bearer {st.session_state.token}"
                            }

                    response = requests.post(
                        "http://127.0.0.1:8000/upload",
                        headers=headers,
                        files=files
                    )

                    response.raise_for_status()

                    data = response.json()

                st.success(data["message"])

                st.success(
                    f"Vector Store Created ({data['chunks']} chunks)"
                )

            except requests.exceptions.RequestException as e:

                st.error(e)

# ==========================
# Upload Images
# ==========================
elif option == "Upload Images":

    st.title("🖼️ Upload Image")

    uploaded_file = st.file_uploader(
        "Select Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            caption=uploaded_file.name,
            use_container_width=True
        )

        if st.button("Upload Image"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            try:

                with st.spinner("Uploading Image..."):

                    headers = {
                            "Authorization": f"Bearer {st.session_state.token}"
                            }

                    response = requests.post(
                        "http://127.0.0.1:8000/upload",
                        headers=headers,
                        files=files
                    )

                    response.raise_for_status()

                    data = response.json()

                st.success(data["message"])

            except requests.exceptions.RequestException as e:

                st.error(e)

# ==========================
# Generate Report
# ==========================
elif option == "Generate Report":

    st.title("📑 Conversation Report")

    if len(st.session_state.messages) == 0:

        st.info("No conversation available.")

    else:

        if st.button("Generate PDF Report"):

            try:

                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                    }

                response = requests.post(
                    "http://127.0.0.1:8000/generate-report",
                    headers=headers,
                    json={
                        "messages": st.session_state.messages
                    }
                )
                response.raise_for_status()

                st.download_button(
                    "⬇ Download Report",
                    data=response.content,
                    file_name="conversation_report.pdf",
                    mime="application/pdf"
                )

            except requests.exceptions.RequestException as e:

                st.error(e)

elif option == "Signup":

    st.title("Create Account")

    username = st.text_input("Username")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Signup"):

        response = requests.post(
            "http://127.0.0.1:8000/signup",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:

            st.success("Account created successfully!")

        else:

            st.error(response.json()["detail"])

elif option == "Login":

    st.title("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(
            "http://127.0.0.1:8000/login",
            data={
                "username": email,
                "password": password
            }
        )

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state.token = token

            st.session_state.logged_in = True

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Email or Password")