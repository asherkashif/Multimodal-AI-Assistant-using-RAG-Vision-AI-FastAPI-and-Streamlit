from fastapi import FastAPI
from app.api import upload
from app.api import ask

app =FastAPI()
app.include_router(upload.router)
app.include_router(ask.router)

@app.get("/")
def home():
    return{
        "message":"welcome to my multimode assistant"
    
    }
@app.get("/health")
def home():
    return{
        "status":"ok"
    
    }