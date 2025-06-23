from fastapi import FastAPI

app = FastAPI(title="AI Support Draft API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Support Draft Generator API!"}

