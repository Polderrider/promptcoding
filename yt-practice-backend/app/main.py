from fastapi import FastAPI
from app.db import get_connection

app = FastAPI(title="YouTube Language Practice API")


@app.get("/")
def root():
    return {"status": "ok", "app": "YouTube Language Practice API"}


@app.get("/health/db")
def db_health():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()

    return {"database": "ok", "result": result[0]}