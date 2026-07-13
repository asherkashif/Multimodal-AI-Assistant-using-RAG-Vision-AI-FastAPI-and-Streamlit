from fastapi import FastAPI
from app.api import upload

app =FastAPI()
app.include_router(upload.router)

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