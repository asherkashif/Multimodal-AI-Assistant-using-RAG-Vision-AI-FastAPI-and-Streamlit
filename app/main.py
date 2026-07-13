from fastapi import FastAPI


app =FastAPI()

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