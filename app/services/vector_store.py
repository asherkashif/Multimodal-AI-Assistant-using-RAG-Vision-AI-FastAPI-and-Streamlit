from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS 

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def create_vector_store(chunks):
    vector_db = FAISS.from_texts(chunks, embeddings)
    
    vector_db.save_local("data/faiss_index")