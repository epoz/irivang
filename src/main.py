from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import databases, os, json

DOMAIN = os.environ.get("DOMAIN")
if not DOMAIN:
    raise Exception("A DOMAIN env variable is mandatory")

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///logdb.sqlite")
database = databases.Database(DATABASE_URL)
DB_SCHEMA = "CREATE TABLE IF NOT EXISTS log(domain, uri, timestamp, headers)"

app = FastAPI()


@app.get("{uri:path}", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request, uri: str):
    headers = {}
    for k, v in request.headers.items():
        if v:
            headers[k] = v

    c = await database.execute(
        "INSERT INTO log VALUES (:domain, :uri, CURRENT_TIMESTAMP, :headers)",
        values={"domain": DOMAIN, "uri": uri, "headers": json.dumps(headers)},
    )
    html = f"""<div style="padding: 5vh">
    We are in the process of migrating <span style="font-size: 150%; font-weight: bold">{DOMAIN}</span> to a new infrastructure. Please bear with us while the process is taking place.
</div>
"""
    return HTMLResponse(html)


if __name__ == "__main__":
    import sqlite3

    db = sqlite3.connect(DATABASE_URL.replace("sqlite://", "."))
    db.executescript(DB_SCHEMA)
