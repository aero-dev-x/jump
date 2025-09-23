from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
from sqlalchemy.orm import Session
import sqlite3
from . import models, schemas, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_file = "carbon.db"

def init_db():
    conn = sqlite3.connect(DB_file)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS carbon_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        index_text INTEGER,
        index_value INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()   
    conn.close()

init_db()

MAP= {
    "very low": 1,
    "low": 25,
    "moderate": 50,
    "high": 75, 
    "very high": 100
}


def get_db():
    db = sqlite3.connect(DB_file, check_same_thread=False)
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello FastAPI with SQLite!"}

@app.get("/carbon/{date}")
async def get_carbon(date:str, db: sqlite3.Connection = Depends(get_db)):
    url = f"https://api.carbonintensity.org.uk/intensity/{date}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        
        if "data" not in data or not data["data"]:
            return {"error": "No data found for the given date"}
        
        index_text = data["data"][0]["intensity"]["index"].lower()
        index_value = MAP.get(index_text, 0)

        c = db.cursor()
        c.execute("INSERT INTO carbon_history (date, index_text, index_value) VALUES (?, ?, ?)", (date, index_text, index_value))
        db.commit()
        c.close()
        return {"date": date, "index_text": index_text, "index_value": index_value}

@app.get("/history")
def get_history(db: sqlite3.Connection = Depends(get_db)):
    c = db.cursor()
    c.execute("SELECT date, index_text, index_value, created_at FROM carbon_history ORDER BY created_at DESC")
    rows = c.fetchall()
    c.close()
    return [{"date": row[0], "index_text": row[1], "index_value": row[2], "created_at": row[3]} for row in rows]

models.Base.metadata.create_all(bind=database.engine)
