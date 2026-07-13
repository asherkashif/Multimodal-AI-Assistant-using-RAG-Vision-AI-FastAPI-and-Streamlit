import streamlit as st
import requests

st.set_page_config(page_title="Multimodal AI Assistant", 
                   page_icon=":smiley:", layout="wide")

st.title("Multimodal AI Assistant")

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

try:
    response = requests.get("http://localhost:8000/")
    data = response.json()
    st.success(data["message"])
except requests.RequestException as e:
    st.error(f"Error fetching data from backend: {e}")