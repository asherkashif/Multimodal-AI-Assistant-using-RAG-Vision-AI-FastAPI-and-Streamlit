import streamlit as st
import requests

st.set_page_config(page_title="Multimodal AI Assistant", 
                   page_icon=":smiley:", layout="wide")

st.title("Multimodal AI Assistant")

uploaded_file= st.file_uploader(
    "Upload a file", 
    type=["pdf", "jpeg", "jpg", "png"])
if uploaded_file is not None:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type,
        )
    }
   
st.write("Welcome to the Multimodal AI Assistant!")

st.sidebar.title("Navigation")
option =st.sidebar.selectbox(
    "Choose", 
    [
        "Home",
        "Chat",
        "Upload Documents",
        "Upload Images",
        "Generate report"
        ])
st.write("Selected:", option)

if st.button("upload"):
    response = requests.post(
        "http://127.0.0.1:8000/upload",
        files=files
    )
    data = response.json()
    if "text" in data:
        st.write("PDF processed successfully!")
        st.text_area(
            "Extracted Text",
            data["text"],
            height=400
        )
    
    else:
        st.success(data["message"])

question = st.text_input("Ask a question")

if st.button("Ask"):
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )
    
    print(response.json())

    st.write(response.json()["answer"])