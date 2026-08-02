from fastapi import FastAPI
from app.api import upload
from app.api import ask
from app.api import report

app =FastAPI()

app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(report.router)

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