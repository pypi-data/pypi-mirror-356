from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("frontend/build/index.html")

@app.get("/message")
def get_message():
    return JSONResponse(content={"message": "Hello from FastAPI!"})

# @app.get("/{full_path:path}")
# def catch_all(full_path: str):
#     return FileResponse("frontend/build/index.html")
