question = st.text_input("Ask a question")

if st.button("Ask"):
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"question": question}
    )

    st.write(response.json()["answer"])