# Jump Carbon Intensity Lookup

A simple web application to look up and track the UK's carbon intensity index for a given date.  
Built with FastAPI (Python), SQLite, SQLAlchemy, and React (Vite).

---

## Features

- Lookup carbon intensity index for any date using the [carbonintensity.org.uk API](https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v2-0-0).
- Store and display a history of all lookups.
- Simple, responsive frontend built with React and Vite.
- FastAPI backend with SQLite for persistent storage.

---

## Project Structure

```
jump/
├── app/
│   ├── main.py         # FastAPI app and endpoints
│   ├── models.py       # SQLAlchemy models (for future ORM use)
│   ├── schemas.py      # Pydantic schemas (for future use)
│   ├── database.py     # SQLAlchemy DB setup
│   └── __init__.py
├── jump_frontend/
│   └── jump-frontend/
│       ├── src/
│       │   ├── App.tsx     # Main React component
│       │   └── ...         # Other frontend files
│       └── ...
└── carbon.db           # SQLite database (created at runtime)
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js & npm

### Backend Setup

1. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. **Install dependencies:**
    ```bash
    pip install fastapi uvicorn httpx sqlalchemy
    ```

3. **Run the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload
    ```

   The API will be available at [http://localhost:8000](http://localhost:8000).

### Frontend Setup

1. **Install dependencies:**
    ```bash
    cd jump_frontend/jump-frontend
    npm install
    ```

2. **Run the React app:**
    ```bash
    npm run dev
    ```

   The frontend will be available at [http://localhost:5173](http://localhost:5173) (default Vite port).

---

## Usage

- Enter a date and click "Submit" to fetch and store the carbon intensity index for that date.
- The "history" table displays all previous lookups.

---

## Notes

- The backend uses both raw SQLite and SQLAlchemy setup, but currently only raw SQLite is used for DB operations.
- The database file is named `carbon.db` and is created automatically.
- CORS is enabled for all origins for development purposes.

---
