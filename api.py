import re
import zipfile
from typing import Callable

import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles


INDEX_PATH = "index.json.zip"
ARCHIVES_PATH = "./books"
df = (
    pd
    .read_json(INDEX_PATH, orient="records")
    .dropna(subset=["authors"])
    .query("lang in ['ru', 'en', 'fi']")
    [["authors", "title", "lang", "archive", "file_name"]]
)
df['authors'] = df['authors'].apply(", ".join)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


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

    mask = np.column_stack([
        df[col].str.contains(re.compile(
            search.strip(),
            flags=re.IGNORECASE
        ), na=False)
        for col in ["authors", "title"]
    ])
    return df.loc[mask.any(axis=1)].to_dict(orient="records")


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
