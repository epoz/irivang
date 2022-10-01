from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import databases, os, json

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data/logdb.sqlite")
database = databases.Database(DATABASE_URL)
DB_SCHEMA = "CREATE TABLE IF NOT EXISTS log(timestamp, uri, headers)"

app = FastAPI()


@app.get("{uri:path}", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request, uri: str):

    headers = {}
    for k, v in request.headers.items():
        if v:
            headers[k] = v

    c = await database.execute(
        "INSERT INTO log VALUES (CURRENT_TIMESTAMP, :uri, :headers)",
        values={"uri": uri, "headers": json.dumps(headers)},
    )
    return HTMLResponse(
        f"""<div style="padding: 5vh">We are migrating to a new infrastructure.</div>"""
    )


if __name__ == "__main__":
    import sqlite3

    db = sqlite3.connect(DATABASE_URL.replace("sqlite:///", ""))
    db.executescript(DB_SCHEMA)
