from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS 
from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

def create_vector_store(chunks):
    vector_db = FAISS.from_texts(chunks, embeddings)
    
    vector_db.save_local("data/faiss_index")