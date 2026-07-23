from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-001"
)

def load_vector_store():
    vector_db = FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_db


def similarity_search(query, vector_db, k=5):
    return vector_db.similarity_search(query, k=k)


def get_relevant_chunks(query, vector_db, k=5):
    results = similarity_search(query, vector_db, k)
    return [doc.page_content for doc in results]