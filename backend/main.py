from fastapi import FastAPI 

app = FastAPI()

@app.get("/my_router")
def get_res():
    return "Hello!!"