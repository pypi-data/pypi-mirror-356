from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from predicta_app_test import main

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("frontend/build/index.html")

@app.get("/message")
def get_message():
    inference = main.infer()
    print(inference)
    return JSONResponse(content=inference.to_dict(orient="records"))

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return FileResponse("frontend/build/index.html")
