from fastapi import FastAPI
import pathlib
from src.routes import notes, tags, contacts

app = FastAPI()

# app.include_router(tags.router, prefix="/api")
# app.include_router(notes.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")

favicon_path = "favicon/favicon.ico"


@app.get("favicon.ico")
def get_favicon(file: pathlib.Path):
    with open(file):
        file.read_bytes()
    return {"message": "Hello World"}


@app.get("/")
def read_root():
    return {"message": "Hello World"}
