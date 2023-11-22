from fastapi import FastAPI
app=FastAPI()

@app.get("/home")
def home():
    return{"success": True, "message":"Hello World"}
