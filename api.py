import zipfile
import json
import sqlite3 as db
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles


INDEX_PATH = "index.json"
ARCHIVES_PATH = "./books"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
con = db.connect('books.db')


@app.middleware("http")
async def cors_handler(request: Request, call_next: Callable) -> Response:
    # Unfortunatly built-in CORS middleware doesn't work so a custom one
    # is needed. See https://github.com/tiangolo/fastapi/issues/1663
    response: Response = await call_next(request)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = request.headers.get(
        "access-control-request-headers", "*")
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS,GET"
    response.headers["Access-Control-Allow-Origin"] = request.headers.get(
        "origin", "*")
    return response


@app.get("/")
async def index():
    return Response(
        status_code=301,
        headers={"Location": "/static/index.html"}
    )


@app.options("/api/books")
@app.options("/api/books/{archive}/{file_name}")
async def books_options() -> Response:
    return Response(status_code=200)


@app.get("/api/books")
async def books(search: str = None):
    if search is None:
        return []

    search = search.strip()
    q = (
        "SELECT * "
        "FROM books "
        "WHERE "
        f"(lower(title) LIKE lower('%{search}%') "
        f"OR lower(authors) LIKE lower('%{search}%')) "
        "AND lang IN ('ru', 'en', 'fi')"
    )
    fields = ["authors", "title", "lang", "archive", "file_name"]
    return [
        dict(zip(fields, row))
        for row in con.execute(q).fetchall()
    ]


@app.get("/api/books/{archive}/{file_name}")
async def book(archive: str, file_name: str):
    file_name += ".fb2"
    with zipfile.ZipFile(f"{ARCHIVES_PATH}/{archive}.zip", 'r') as zip_ref:
        return Response(
            content=zip_ref.read(file_name),
            media_type="application/fb2",
            headers={
                "Content-Disposition": f'attachment; filename="{file_name}"'
            }
        )
